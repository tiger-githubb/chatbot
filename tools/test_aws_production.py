#!/usr/bin/env python3
"""
Script pour tester la configuration AWS Lambda et DynamoDB
"""

import boto3
import requests
import json
from dotenv import load_dotenv
import os

# Charger les variables d'environnement de production
load_dotenv('.env.production')

def test_dynamodb_connection():
    """Test de la connexion à DynamoDB"""
    print("🔍 Test de la connexion DynamoDB...")
    
    try:
        # Configuration du client DynamoDB
        dynamodb = boto3.client(
            'dynamodb',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        
        # Test de connexion - liste des tables
        tables = dynamodb.list_tables()
        table_name = os.getenv('DYNAMO_TABLE')
        
        if table_name in tables['TableNames']:
            print(f"✅ Table DynamoDB '{table_name}' trouvée")
            
            # Test d'écriture
            test_item = {
                'id': {'S': 'test_connection'},
                'user_id': {'S': 'test_user'},
                'user_message': {'S': 'Test de connexion'},
                'bot_response': {'S': 'Réponse de test'},
                'timestamp': {'S': '2025-06-03T10:00:00'},
                'created_date': {'S': '2025-06-03'},
                'source': {'S': 'test'}
            }
            
            dynamodb.put_item(
                TableName=table_name,
                Item=test_item
            )
            print("✅ Test d'écriture DynamoDB réussi")
            
            # Nettoyer le test
            dynamodb.delete_item(
                TableName=table_name,
                Key={'id': {'S': 'test_connection'}}
            )
            print("✅ Nettoyage du test effectué")
            
            return True
        else:
            print(f"❌ Table '{table_name}' non trouvée")
            print(f"📋 Tables disponibles: {tables['TableNames']}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur DynamoDB: {e}")
        return False

def test_api_endpoint():
    """Test de l'endpoint API AWS Lambda"""
    print("\n🔍 Test de l'endpoint API...")
    
    api_url = os.getenv('API_URL')
    
    try:
        # Test du endpoint /chat
        chat_url = f"{api_url}/chat"
        params = {"question": "Test de connexion AWS Lambda"}
        
        response = requests.get(chat_url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint /chat accessible")
            print(f"📋 Réponse reçue: {data.get('answer', {}).get('S', 'N/A')[:50]}...")
            return True
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            print(f"📋 Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur API: {e}")
        return False

def test_mistral_api():
    """Test de l'API Mistral"""
    print("\n🔍 Test de l'API Mistral...")
    
    try:
        from mistralai.client import MistralClient
        
        api_key = os.getenv('MISTRAL_API_KEY')
        if not api_key:
            print("❌ MISTRAL_API_KEY manquant")
            return False
        
        client = MistralClient(api_key=api_key)
        
        # Test simple
        response = client.chat(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": "Hello"}]
        )
        
        if hasattr(response, 'choices') and response.choices:
            print("✅ API Mistral fonctionnelle")
            return True
        else:
            print("❌ Réponse Mistral invalide")
            return False
            
    except Exception as e:
        print(f"❌ Erreur Mistral: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Test de la configuration AWS Lambda")
    print("=" * 50)
    
    # Variables d'environnement
    print(f"📋 ENV_NAME: {os.getenv('ENV_NAME')}")
    print(f"📋 AWS_REGION: {os.getenv('AWS_REGION')}")
    print(f"📋 DYNAMO_TABLE: {os.getenv('DYNAMO_TABLE')}")
    print(f"📋 API_URL: {os.getenv('API_URL')}")
    
    # Tests
    tests = [
        ("DynamoDB", test_dynamodb_connection),
        ("API Endpoint", test_api_endpoint),
        ("Mistral API", test_mistral_api)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🚀 Tous les tests sont passés! Configuration AWS Lambda OK")
    else:
        print("\n⚠️  Certains tests ont échoué. Vérifiez la configuration.")
