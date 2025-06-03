#!/usr/bin/env python3
"""
Test script to verify the Telegram webhook functionality
"""
import json
import requests

# Test webhook endpoint
webhook_url = "http://localhost:8001/telegram/webhook"

# Test message simulating a /start command
test_update = {
    "update_id": 123456789,
    "message": {
        "message_id": 1,
        "from": {
            "id": 987654321,
            "is_bot": False,
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser"
        },
        "chat": {
            "id": 987654321,
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "type": "private"
        },
        "date": 1638360000,
        "text": "/start",
        "entities": [
            {
                "offset": 0,
                "length": 6,
                "type": "bot_command"
            }
        ]
    }
}

def test_webhook():
    """Test the webhook with a /start command"""
    try:
        print("Testing webhook with /start command...")
        response = requests.post(webhook_url, json=test_update, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook test successful!")
            return True
        else:
            print("❌ Webhook test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing webhook: {str(e)}")
        return False

def test_regular_message():
    """Test the webhook with a regular message"""
    regular_update = test_update.copy()
    regular_update["message"]["text"] = "Hello, bot!"
    regular_update["message"]["entities"] = []
    
    try:
        print("\nTesting webhook with regular message...")
        response = requests.post(webhook_url, json=regular_update, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Regular message test successful!")
            return True
        else:
            print("❌ Regular message test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing regular message: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Telegram Webhook Final Test ===")
    
    # Test both scenarios
    start_success = test_webhook()
    message_success = test_regular_message()
    
    print(f"\n=== Test Results ===")
    print(f"/start command: {'✅ PASS' if start_success else '❌ FAIL'}")
    print(f"Regular message: {'✅ PASS' if message_success else '❌ FAIL'}")
    
    if start_success and message_success:
        print("\n🎉 All tests passed! The webhook is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the server logs for details.")
