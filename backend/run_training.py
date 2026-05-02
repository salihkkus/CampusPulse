import subprocess
import sys

print("🤖 AI Model Eğitimi Başlatılıyor...")

# Komutu çalıştır
command = [sys.executable, "simple_train.py"]

try:
    result = subprocess.run(command, capture_output=True, text=True, timeout=300)
    
    print("Çıktı:")
    print(result.stdout)
    
    if result.stderr:
        print("Hata:")
        print(result.stderr)
    
    print(f"Return Code: {result.returncode}")
    
except subprocess.TimeoutExpired:
    print("❌ Eğitim zaman aşımına uğradı")
except Exception as e:
    print(f"❌ Hata: {e}")
