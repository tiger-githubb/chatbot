#!/usr/bin/env python3
"""
Test script for Telegram bot DynamoDB integration
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import insert_chat_message
import logging

logging.basicConfig(level=logging.INFO)

def test_integration():
    """Test the complete DynamoDB integration"""
    try:
        print("🧪 Testing Telegram bot DynamoDB integration...")
        
        # Test data
        test_user_id = "test_telegram_user_123"
        test_message = "Hello, this is a test message from Telegram integration"
        test_response = "Hello! This is a test response from the bot."
        test_source = "telegram"
        test_mistral_id = "test_mistral_response_id"
        
        # Insert test data
        success = insert_chat_message(
            user_id=test_user_id,
            user_message=test_message,
            bot_response=test_response,
            source=test_source,
            mistral_id=test_mistral_id
        )
        
        assert success, "Échec de l'insertion du message dans DynamoDB"
        
        print("✅ Telegram bot DynamoDB integration test PASSED!")
        print(f"   - User ID: {test_user_id}")
        print(f"   - Source: {test_source}")
        print(f"   - Message saved successfully to DynamoDB")
            
    except Exception as e:
        print(f"❌ Integration test failed with error: {e}")
        assert False, f"Exception lors du test d'intégration: {e}"

if __name__ == "__main__":
    test_integration()
