#!/usr/bin/env python3
"""
Test script to verify WhatsApp webhook functionality
"""
import requests
import sys
import json

def test_webhook_verification(base_url, verify_token):
    """Test webhook verification with proper parameters"""
    
    print("=" * 60)
    print("WhatsApp Webhook Testing Tool")
    print("=" * 60)
    
    # Test 1: Correct verification
    print("\n🔍 Test 1: Correct Verification")
    print("-" * 40)
    
    params = {
        'hub.mode': 'subscribe',
        'hub.verify_token': verify_token,
        'hub.challenge': 'test_challenge_12345'
    }
    
    try:
        response = requests.get(f"{base_url}/webhook/", params=params, timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response Headers: {dict(response.headers)}")
        print(f"✅ Response Body: '{response.text}'")
        print(f"✅ Response Length: {len(response.text)}")
        
        if response.status_code == 200 and response.text == 'test_challenge_12345':
            print("🎉 Verification SUCCESSFUL!")
        else:
            print("❌ Verification FAILED!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Wrong token
    print("\n🔍 Test 2: Wrong Token")
    print("-" * 40)
    
    params['hub.verify_token'] = 'wrong_token'
    
    try:
        response = requests.get(f"{base_url}/webhook/", params=params, timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response: '{response.text}'")
        
        if response.status_code == 403:
            print("🎉 Wrong token correctly rejected!")
        else:
            print("❌ Wrong token not properly rejected!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Missing parameters
    print("\n🔍 Test 3: Missing Parameters")
    print("-" * 40)
    
    params = {'hub.mode': 'subscribe'}
    
    try:
        response = requests.get(f"{base_url}/webhook/", params=params, timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response: '{response.text}'")
        
        if response.status_code == 400:
            print("🎉 Missing parameters correctly handled!")
        else:
            print("❌ Missing parameters not properly handled!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: POST request (webhook data)
    print("\n🔍 Test 4: POST Request (Webhook Data)")
    print("-" * 40)
    
    webhook_data = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "1234567890",
                        "type": "text",
                        "text": {"body": "help"}
                    }]
                }
            }]
        }]
    }
    
    try:
        response = requests.post(
            f"{base_url}/webhook/", 
            json=webhook_data, 
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response: '{response.text}'")
        
        if response.status_code == 200:
            print("🎉 Webhook POST request successful!")
        else:
            print("❌ Webhook POST request failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)

def main():
    if len(sys.argv) != 3:
        print("Usage: python test_webhook.py <base_url> <verify_token>")
        print("Example: python test_webhook.py https://abc123.ngrok.io fitblendz_whatsapp_verify_7c2f4b1e")
        print("\nNote: Make sure your Django server is running and accessible at the base_url")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    verify_token = sys.argv[2]
    
    print(f"🌐 Testing webhook at: {base_url}")
    print(f"🔑 Verify token: {verify_token}")
    
    test_webhook_verification(base_url, verify_token)
    
    print("\n📋 Next Steps:")
    print("1. If all tests pass, your webhook is working correctly!")
    print("2. Configure WhatsApp Business with:")
    print(f"   - Callback URL: {base_url}/webhook/")
    print(f"   - Verify Token: {verify_token}")
    print("3. Test with real WhatsApp messages")

if __name__ == "__main__":
    main()
