#!/usr/bin/env python3

import subprocess
import sys
import time
import requests
from threading import Thread

def start_server():
    """FastAPI sunucusunu başlat"""
    print("🚀 FastAPI Sunucusu Başlatılıyor...")
    
    # Sunucuyu başlat
    uvicorn_command = [
        sys.executable, "-m", "uvicorn", 
        "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"
    ]
    
    process = subprocess.Popen(
        uvicorn_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    return process

def wait_for_server(max_attempts=30):
    """Sunucunun hazır olmasını bekle"""
    print("⏳ Sunucu başlatılıyor...")
    
    for i in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/docs", timeout=2)
            if response.status_code == 200:
                print("✅ Sunucu hazır!")
                return True
        except:
            pass
        
        time.sleep(1)
        print(f"   Bekleniyor... ({i+1}/{max_attempts})")
    
    print("❌ Sunucu başlatılamadı")
    return False

def run_endpoint_tests():
    """Endpoint testlerini çalıştır"""
    print("\n🧪 Endpoint Testleri Başlatılıyor...")
    
    try:
        # Test script'ini çalıştır
        test_command = [sys.executable, "test_endpoints.py"]
        result = subprocess.run(test_command, capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.stderr:
            print("Hata çıktısı:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        return False

def main():
    """Ana fonksiyon"""
    print("🎯 CampusPulse Backend Test")
    print("=" * 50)
    
    # Sunucuyu başlat
    server_process = start_server()
    
    try:
        # Sunucunun hazır olmasını bekle
        if wait_for_server():
            # Testleri çalıştır
            success = run_endpoint_tests()
            
            if success:
                print("\n🎉 Tüm Testler Başarılı!")
                print("✅ Backend hazır!")
                print("🚀 Muhammet frontend'i bağlayabilir!")
            else:
                print("\n❌ Bazı testler başarısız oldu")
        else:
            print("❌ Sunucu başlatılamadı")
    
    except KeyboardInterrupt:
        print("\n⏹️ Durduruldu...")
    
    finally:
        # Sunucuyu kapat
        if server_process:
            print("\n🛑 Sunucu kapatılıyor...")
            server_process.terminate()
            server_process.wait()
            print("✅ Sunucu kapatıldı")

if __name__ == "__main__":
    main()
