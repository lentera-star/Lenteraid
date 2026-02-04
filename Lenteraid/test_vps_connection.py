#!/usr/bin/env python3
"""
Quick VPS Backend Health Check
Tests if backend is responding correctly
"""
import requests
import json

VPS_IP = "84.247.150.83"
BASE_URL = f"http://{VPS_IP}:8000"

def test_health():
    """Test /health endpoint"""
    try:
        print(f"\n🔍 Testing {BASE_URL}/health...")
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Health Check PASSED!")
            print(f"   Status: {data.get('status')}")
            print(f"   Services: {data.get('services', {})}")
            return True
        else:
            print(f"\n❌ Health Check FAILED! Status: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - VPS may be down")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - Cannot reach VPS")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat():
    """Test /api/chat endpoint"""
    try:
        print(f"\n🔍 Testing {BASE_URL}/api/chat...")
        
        payload = {
            "message": "Halo, apa kabar?",
            "user_id": "test_user",
            "conversation_id": "test_conv"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Chat API WORKS!")
            print(f"   AI Response: {data.get('message', 'N/A')[:100]}...")
            return True
        else:
            print(f"\n❌ Chat API FAILED! Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🚀 LENTERA VPS Backend Test")
    print("="*60)
    print(f"VPS IP: {VPS_IP}")
    print(f"Backend URL: {BASE_URL}")
    print("="*60)
    
    # Test health
    health_ok = test_health()
    
    # Test chat if health is OK
    if health_ok:
        chat_ok = test_chat()
        
        if chat_ok:
            print("\n" + "="*60)
            print("🎉 ALL TESTS PASSED! Backend is ready!")
            print("="*60)
            print("\n✅ You can now run Flutter app:")
            print("   flutter run")
            print("\nThe app will connect to production VPS automatically!")
        else:
            print("\n⚠️ Health OK but Chat API has issues")
    else:
        print("\n❌ Health check failed - VPS may need restart")
        print("\n💡 Try these:")
        print("   1. Check if VPS is running in Contabo panel")
        print("   2. SSH into VPS and check Docker: docker-compose ps")
        print("   3. Check backend logs: docker-compose logs backend")
