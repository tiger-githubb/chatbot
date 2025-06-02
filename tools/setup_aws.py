#!/usr/bin/env python3
"""
Script pour configurer AWS et créer une table DynamoDB pour le chatbot
"""

import boto3
import os
import sys
from pathlib import Path

# Ajouter le répertoire src au path pour l'import
src_dir = Path(__file__).parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

def check_aws_credentials():
    """Vérifier si les credentials AWS sont configurés"""
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials is None:
            print("❌ Aucune credential AWS trouvée")
            return False
        print(f"✅ Credentials AWS trouvées pour la région : {session.region_name}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des credentials : {e}")
        return False

def setup_aws_profile():
    """Configuration interactive des credentials AWS"""
    print("🔧 Configuration des credentials AWS...")
    print("\nVous devez obtenir ces informations depuis la console AWS :")
    print("1. Allez dans IAM > Users > Votre utilisateur > Security credentials")
    print("2. Créez un 'Access Key' si vous n'en avez pas")
    print("3. Notez l'Access Key ID et le Secret Access Key\n")
    
    access_key = input("🔑 AWS Access Key ID : ").strip()
    secret_key = input("🔒 AWS Secret Access Key : ").strip()
    region = input("🌍 AWS Region (défaut: eu-north-1) : ").strip() or "eu-north-1"
    
    # Créer le répertoire .aws s'il n'existe pas
    aws_dir = Path.home() / ".aws"
    aws_dir.mkdir(exist_ok=True)
    
    # Écrire les credentials
    credentials_file = aws_dir / "credentials"
    config_file = aws_dir / "config"
    
    credentials_content = f"""[default]
aws_access_key_id = {access_key}
aws_secret_access_key = {secret_key}
"""
    
    config_content = f"""[default]
region = {region}
output = json
"""
    
    credentials_file.write_text(credentials_content)
    config_file.write_text(config_content)
    
    print(f"✅ Credentials sauvegardées dans {aws_dir}")
    return region

def create_dynamodb_table(table_name="chatbot-conversations", region="eu-north-1"):
    """Créer une table DynamoDB pour le chatbot"""
    try:
        # Configuration du client DynamoDB
        dynamodb = boto3.resource('dynamodb', region_name=region)
        
        print(f"🔧 Création de la table DynamoDB '{table_name}'...")
        
        # Définition de la table
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'conversation_id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'conversation_id',
                    'AttributeType': 'S'  # String
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'N'  # Number
                }
            ],
            BillingMode='PAY_PER_REQUEST'  # Mode serverless
        )
        
        # Attendre que la table soit créée
        print("⏳ Attente de la création de la table...")
        table.wait_until_exists()
        
        print(f"✅ Table '{table_name}' créée avec succès!")
        print(f"📊 ARN de la table : {table.table_arn}")
        
        return table_name
        
    except Exception as e:
        if "ResourceInUseException" in str(e):
            print(f"✅ La table '{table_name}' existe déjà")
            return table_name
        else:
            print(f"❌ Erreur lors de la création de la table : {e}")
            return None

def test_dynamodb_connection(table_name, region="eu-north-1"):
    """Tester la connexion à DynamoDB"""
    try:
        dynamodb = boto3.resource('dynamodb', region_name=region)
        table = dynamodb.Table(table_name)
        
        # Test d'écriture
        test_item = {
            'conversation_id': 'test-connection',
            'timestamp': 1748856000,
            'message': 'Test de connexion',
            'user_id': 'test-user'
        }
        
        table.put_item(Item=test_item)
        print("✅ Test d'écriture DynamoDB réussi")
        
        # Test de lecture
        response = table.get_item(
            Key={
                'conversation_id': 'test-connection',
                'timestamp': 1748856000
            }
        )
        
        if 'Item' in response:
            print("✅ Test de lecture DynamoDB réussi")
            
            # Supprimer l'item de test
            table.delete_item(
                Key={
                    'conversation_id': 'test-connection',
                    'timestamp': 1748856000
                }
            )
            print("✅ Nettoyage effectué")
            return True
        else:
            print("❌ Échec du test de lecture")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test DynamoDB : {e}")
        return False

def update_env_file(table_name, region):
    """Mettre à jour le fichier .env avec les informations DynamoDB"""
    try:
        env_file = Path(__file__).parent.parent / ".env"
        
        if env_file.exists():
            content = env_file.read_text()
            
            # Mettre à jour les variables DynamoDB
            lines = content.split('\n')
            updated_lines = []
            
            for line in lines:
                if line.startswith('DYNAMO_TABLE='):
                    updated_lines.append(f'DYNAMO_TABLE={table_name}')
                elif line.startswith('AWS_REGION='):
                    updated_lines.append(f'AWS_REGION={region}')
                else:
                    updated_lines.append(line)
            
            env_file.write_text('\n'.join(updated_lines))
            print(f"✅ Fichier .env mis à jour avec la table : {table_name}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour du .env : {e}")

def main():
    """Fonction principale"""
    print("🚀 Configuration AWS et DynamoDB pour le Chatbot Telegram")
    print("=" * 60)
    
    # Étape 1 : Vérifier les credentials
    if not check_aws_credentials():
        print("\n📝 Configuration des credentials AWS requise...")
        region = setup_aws_profile()
        
        # Revérifier après configuration
        if not check_aws_credentials():
            print("❌ Échec de la configuration des credentials")
            sys.exit(1)
    else:
        session = boto3.Session()
        region = session.region_name or "eu-north-1"
    
    print(f"\n🌍 Région utilisée : {region}")
    
    # Étape 2 : Créer la table DynamoDB
    table_name = f"chatbot-dbtable-aristidekarbou"
    created_table = create_dynamodb_table(table_name, region)
    
    if created_table:
        # Étape 3 : Tester la connexion
        print(f"\n🧪 Test de la connexion à DynamoDB...")
        if test_dynamodb_connection(created_table, region):
            print("✅ Configuration DynamoDB terminée avec succès!")
            
            # Étape 4 : Mettre à jour le .env
            update_env_file(created_table, region)
            
            print("\n🎉 Configuration complète !")
            print(f"📊 Table DynamoDB : {created_table}")
            print(f"🌍 Région : {region}")
            print("💡 Votre chatbot peut maintenant utiliser DynamoDB pour stocker les conversations")
            
        else:
            print("❌ Échec des tests DynamoDB")
    else:
        print("❌ Échec de la création de la table DynamoDB")

if __name__ == "__main__":
    main()
