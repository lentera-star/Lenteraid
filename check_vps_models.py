import requests
import json

def check_ollama_vps():
    vps_ip = "84.247.150.83"
    ollama_url = f"http://{vps_ip}:11434/api/tags"
    
    print(f"🔍 Mengecek model di Ollama VPS ({vps_ip})...")
    print("=" * 50)
    
    try:
        response = requests.get(ollama_url, timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            if not models:
                print("⚠️  Ollama jalan, tapi BELUM ADA model yang terinstall.")
            else:
                print(f"✅ Ditemukan {len(models)} model di VPS:")
                for m in models:
                    name = m.get('name')
                    size = m.get('size', 0) / (1024**3) # Convert to GB
                    modified = m.get('modified_at')
                    print(f"   - 🤖 {name} ({size:.2f} GB) - Update: {modified}")
        else:
            print(f"❌ Ollama gagal merespon (Status: {response.status_code})")
            print("   Mungkin port 11434 belum dibuka atau Ollama mati.")
    except Exception as e:
        print(f"❌ Error saat koneksi: {e}")
        print("   Pastikan VPS nyala dan port 11434 bisa diakses public.")

if __name__ == "__main__":
    check_ollama_vps()
