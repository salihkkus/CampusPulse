import subprocess
import sys

print("🔍 Teşhis Motoru Testi Başlatılıyor...")

# Komutu çalıştır
command = [sys.executable, "simple_diagnosis_test.py"]

try:
    result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    
    print("Çıktı:")
    print(result.stdout)
    
    if result.stderr:
        print("Hata:")
        print(result.stderr)
    
    print(f"Return Code: {result.returncode}")
    
except subprocess.TimeoutExpired:
    print("❌ Test zaman aşımına uğradı")
except Exception as e:
    print(f"❌ Hata: {e}")
