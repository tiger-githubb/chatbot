#!/usr/bin/env python3
"""
Script de test pour vérifier la connexion DynamoDB
"""

import sys
import os
from pathlib import Path
import boto3
from datetime import datetime
import json

# Ajouter le répertoire src au path pour l'import
src_dir = Path(__file__).parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from config import settings

def test_aws_credentials():
    """Test des credentials AWS"""
    print("🔑 Test des credentials AWS...")
    
    try:
        # Configuration du client avec les credentials du .env
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            client = boto3.client(
                'sts',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
        else:
            # Utiliser les credentials par défaut (profil AWS)
            client = boto3.client('sts', region_name=settings.AWS_REGION)
        
        # Test avec get_caller_identity
        response = client.get_caller_identity()
        print(f"✅ Credentials AWS validés")
        print(f"   User ID: {response['UserId']}")
        print(f"   Account: {response['Account']}")
        print(f"   ARN: {response['Arn']}")
        assert True
        
    except Exception as e:
        print(f"❌ Erreur avec les credentials AWS: {e}")
        assert False, f"Erreur d'authentification AWS: {e}"

def test_dynamodb_access():
    """Test de l'accès à la table DynamoDB"""
    print(f"\n📊 Test d'accès à la table DynamoDB '{settings.DYNAMO_TABLE}'...")
    
    try:
        # Configuration du client DynamoDB
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            dynamodb = boto3.client(
                'dynamodb',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
        else:
            dynamodb = boto3.client('dynamodb', region_name=settings.AWS_REGION)
        
        # Décrire la table
        response = dynamodb.describe_table(TableName=settings.DYNAMO_TABLE)
        table_status = response['Table']['TableStatus']
        
        print(f"✅ Table trouvée et accessible")
        print(f"   Statut: {table_status}")
        print(f"   Nom: {response['Table']['TableName']}")
        print(f"   Clé primaire: {response['Table']['KeySchema']}")
        
        assert True
        
    except Exception as e:
        print(f"❌ Erreur d'accès à la table DynamoDB: {e}")
        assert False, f"Erreur d'accès à la table DynamoDB: {e}"

def test_dynamodb_write_read():
    """Test d'écriture et lecture dans DynamoDB"""
    print(f"\n📝 Test d'écriture/lecture dans DynamoDB...")
    
    try:
        # Configuration du client DynamoDB
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            dynamodb = boto3.client(
                'dynamodb',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
        else:
            dynamodb = boto3.client('dynamodb', region_name=settings.AWS_REGION)
        
        # Test d'écriture
        test_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_item = {
            'id': {'S': test_id},
            'conversation_id': {'S': 'test_conversation'},
            'user_id': {'S': 'test_user'},
            'user_message': {'S': 'Test message from connection script'},
            'bot_response': {'S': 'Test response from connection script'},
            'timestamp': {'S': datetime.now().isoformat()},
            'created_date': {'S': datetime.now().strftime('%Y-%m-%d')},
            'source': {'S': 'test'}
        }
        
        dynamodb.put_item(
            TableName=settings.DYNAMO_TABLE,
            Item=test_item
        )
        print(f"✅ Écriture réussie - ID: {test_id}")
        
        # Test de lecture
        response = dynamodb.get_item(
            TableName=settings.DYNAMO_TABLE,
            Key={'id': {'S': test_id}}
        )
        
        if 'Item' in response:
            print(f"✅ Lecture réussie")
            print(f"   Message: {response['Item']['user_message']['S']}")
            
            # Nettoyage - supprimer l'item de test
            dynamodb.delete_item(
                TableName=settings.DYNAMO_TABLE,
                Key={'id': {'S': test_id}}
            )
            print(f"✅ Item de test nettoyé")
            assert True
        else:
            assert False, "Item non trouvé dans DynamoDB"
        
    except Exception as e:
        print(f"❌ Erreur lors du test d'écriture/lecture: {e}")
        assert False, f"Erreur lors du test d'écriture/lecture: {e}"

if __name__ == "__main__":
    """Fonction principale de test"""
    print("🧪 TEST DE CONNEXION DYNAMODB")
    print("=" * 50)
    print(f"⚙️  Configuration:")
    print(f"   AWS_REGION: {settings.AWS_REGION}")
    print(f"   DYNAMO_TABLE: {settings.DYNAMO_TABLE}")
    print(f"   AWS_ACCESS_KEY_ID: {'✅ Configuré' if settings.AWS_ACCESS_KEY_ID else '❌ Manquant'}")
    print("=" * 50)
    
    # Exécuter les tests
    test_aws_credentials()
    test_dynamodb_access()
    test_dynamodb_write_read()
    
    print("=" * 50)
    print("✅ Tous les tests ont réussi!")
