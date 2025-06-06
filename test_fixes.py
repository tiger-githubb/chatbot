#!/usr/bin/env python3
"""
Script de test pour valider les corrections appliquées
"""
import boto3
import json
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_dynamodb_table_structure():
    """Teste si la table DynamoDB a les index requis"""
    try:
        # Utiliser les variables d'environnement pour la région
        region = os.getenv('AWS_REGION', 'eu-west-3')
        
        # Créer le client DynamoDB
        dynamodb = boto3.client('dynamodb', region_name=region)
        
        # Nom de la table (remplacez par votre nom de table actual)
        table_name = f"chatbot-dbtable-master"  # Ajustez selon votre environnement
        
        print(f"🔍 Testing DynamoDB table: {table_name}")
        
        # Décrire la table
        response = dynamodb.describe_table(TableName=table_name)
        table_info = response['Table']
        
        print(f"✅ Table Status: {table_info['TableStatus']}")
        print(f"✅ Table Name: {table_info['TableName']}")
        
        # Vérifier les index
        gsi_list = table_info.get('GlobalSecondaryIndexes', [])
        print(f"📊 Global Secondary Indexes found: {len(gsi_list)}")
        
        required_indexes = [
            'conversation_id-timestamp-index',
            'user_id-timestamp-index'
        ]
        
        found_indexes = [gsi['IndexName'] for gsi in gsi_list]
        
        for required_index in required_indexes:
            if required_index in found_indexes:
                print(f"✅ Index '{required_index}' found")
            else:
                print(f"❌ Index '{required_index}' MISSING")
        
        return len(found_indexes) >= 2
        
    except Exception as e:
        print(f"❌ Error testing DynamoDB: {str(e)}")
        return False

def test_lambda_configuration():
    """Teste la configuration de la fonction Lambda"""
    try:
        region = os.getenv('AWS_REGION', 'eu-west-3')
        lambda_client = boto3.client('lambda', region_name=region)
        
        function_name = "chatbot-lambda-master"  # Ajustez selon votre environnement
        
        print(f"🔍 Testing Lambda function: {function_name}")
        
        response = lambda_client.get_function_configuration(FunctionName=function_name)
        
        memory_size = response['MemorySize']
        timeout = response['Timeout']
        runtime = response['Runtime']
        
        print(f"💾 Memory Size: {memory_size} MB")
        print(f"⏱️ Timeout: {timeout} seconds")
        print(f"🐍 Runtime: {runtime}")
        
        # Vérifier les améliorations
        if memory_size >= 512:
            print("✅ Memory size is adequate (≥512MB)")
        else:
            print("❌ Memory size is too low (<512MB)")
            
        if timeout >= 30:
            print("✅ Timeout is adequate (≥30s)")
        else:
            print("❌ Timeout is too low (<30s)")
            
        return memory_size >= 512 and timeout >= 30
        
    except Exception as e:
        print(f"❌ Error testing Lambda: {str(e)}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Testing AWS Infrastructure Fixes...")
    print("=" * 50)
    
    dynamodb_ok = test_dynamodb_table_structure()
    print()
    
    lambda_ok = test_lambda_configuration()
    print()
    
    print("=" * 50)
    if dynamodb_ok and lambda_ok:
        print("🎉 ALL TESTS PASSED! Infrastructure is ready.")
    else:
        print("⚠️ Some tests failed. Please redeploy the infrastructure.")
    
    return dynamodb_ok and lambda_ok

if __name__ == "__main__":
    main()
