import requests
import json

def test_fast_mode_proxy():
    # Supabase Proxy URL
    url = "https://ghtjooqihifvbmdaojpp.supabase.co/functions/v1/proxy_ai"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdodGpvb3FpaGlmdmJtZGFvanBwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUzNzM4NzQsImV4cCI6MjA4MDk0OTg3NH0.4lxPJ8kFkkJySRTapNXf5JDkVMkjt0uuT-u0xWZPQos"
    }
    
    payload = {
        "messages": [
            {"role": "user", "content": "Halo, ini tes untuk Fast Mode VPS. Apakah kamu online?"}
        ],
        "model_mode": "fast" # Memaksa proxy ke VPS
    }
    
    print("Testing LENTERA Fast Mode (VPS via Supabase Proxy)...")
    print("=" * 50)
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"Status: {response.statusCode if hasattr(response, 'statusCode') else response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ BERHASIL! Respon dari VPS:")
            print(f"---\n{data.get('message', 'No message content')}\n---")
        else:
            print(f"❌ GAGAL! Status: {response.status_code}")
            print(f"Respon: {response.text}")
    except Exception as e:
        print(f"❌ Error koneksi: {e}")

if __name__ == "__main__":
    test_fast_mode_proxy()
