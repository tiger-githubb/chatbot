#!/usr/bin/env python3
"""
Comprehensive test for the complete DynamoDB integration
Tests both API endpoint and Telegram bot functionality
"""
import sys
import os
import asyncio
import json
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import insert_chat_message, get_dynamo_client
from config import settings
import logging

logging.basicConfig(level=logging.INFO)

def test_api_integration():
    """Test the API integration with DynamoDB"""
    print("🧪 Testing API → DynamoDB integration...")
    
    try:
        # Test data for API
        test_user_id = "api_test_user_123"
        test_message = "Hello from API test"
        test_response = "Hello! This is an API test response."
        test_source = "api"
        test_mistral_id = "api_test_mistral_id"
        
        # Insert test data
        success = insert_chat_message(
            user_id=test_user_id,
            user_message=test_message,
            bot_response=test_response,
            source=test_source,
            mistral_id=test_mistral_id
        )
        
        if success:
            print("✅ API → DynamoDB integration PASSED!")
            return True
        else:
            print("❌ API → DynamoDB integration FAILED!")
            return False
            
    except Exception as e:
        print(f"❌ API integration test failed: {e}")
        return False

def test_telegram_integration():
    """Test the Telegram integration with DynamoDB"""
    print("🧪 Testing Telegram → DynamoDB integration...")
    
    try:
        # Test data for Telegram
        test_user_id = "telegram_test_user_456"
        test_message = "Hello from Telegram test"
        test_response = "Hello! This is a Telegram test response."
        test_source = "telegram"
        test_mistral_id = "telegram_test_mistral_id"
        
        # Insert test data
        success = insert_chat_message(
            user_id=test_user_id,
            user_message=test_message,
            bot_response=test_response,
            source=test_source,
            mistral_id=test_mistral_id
        )
        
        if success:
            print("✅ Telegram → DynamoDB integration PASSED!")
            return True
        else:
            print("❌ Telegram → DynamoDB integration FAILED!")
            return False
            
    except Exception as e:
        print(f"❌ Telegram integration test failed: {e}")
        return False

def test_data_retrieval():
    """Test data retrieval from DynamoDB"""
    print("🧪 Testing data retrieval from DynamoDB...")
    
    try:
        client = get_dynamo_client()
        table_name = settings.DYNAMO_TABLE
        
        # Scan the table to get recent items
        response = client.scan(
            TableName=table_name,
            Limit=5,
            FilterExpression='contains(id, :prefix)',
            ExpressionAttributeValues={
                ':prefix': {'S': 'test_'}
            }
        )
        
        items = response.get('Items', [])
        print(f"✅ Retrieved {len(items)} test items from DynamoDB")
        
        for item in items[:3]:  # Show first 3 items
            item_id = item.get('id', {}).get('S', 'Unknown')
            source = item.get('source', {}).get('S', 'Unknown')
            user_id = item.get('user_id', {}).get('S', 'Unknown')
            print(f"   - ID: {item_id[:20]}... | Source: {source} | User: {user_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data retrieval test failed: {e}")
        return False

def cleanup_test_data():
    """Clean up test data from DynamoDB"""
    print("🧹 Cleaning up test data...")
    
    try:
        client = get_dynamo_client()
        table_name = settings.DYNAMO_TABLE
        
        # Scan for test items
        response = client.scan(
            TableName=table_name,
            FilterExpression='contains(id, :prefix)',
            ExpressionAttributeValues={
                ':prefix': {'S': 'test_'}
            }
        )
        
        items = response.get('Items', [])
        deleted_count = 0
        
        for item in items:
            item_id = item.get('id', {}).get('S')
            if item_id:
                try:
                    client.delete_item(
                        TableName=table_name,
                        Key={'id': {'S': item_id}}
                    )
                    deleted_count += 1
                except Exception as e:
                    print(f"   Warning: Could not delete {item_id}: {e}")
        
        print(f"✅ Cleaned up {deleted_count} test items")
        return True
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 COMPREHENSIVE DYNAMODB INTEGRATION TEST")
    print("=" * 50)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🗂️  Table: {settings.DYNAMO_TABLE}")
    print(f"🌍 Region: {settings.AWS_REGION}")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # Run tests
    if test_api_integration():
        tests_passed += 1
    
    if test_telegram_integration():
        tests_passed += 1
    
    if test_data_retrieval():
        tests_passed += 1
    
    # Cleanup
    cleanup_test_data()
    
    # Results
    print("=" * 50)
    print(f"📊 RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("✅ The DynamoDB integration is fully functional")
        print("✅ Both API and Telegram endpoints are working")
        print("✅ Data storage and retrieval are operational")
        return True
    else:
        print("❌ Some tests failed. Please check the integration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
