#!/usr/bin/env python3
"""
Script d'assistance pour configurer AWS et DynamoDB
Recommandations personnalisées pour le chatbot Telegram
"""

import os
import subprocess
import sys
from pathlib import Path

def print_header(title):
    """Affiche un titre formaté"""
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def print_step(step_num, title):
    """Affiche une étape numérotée"""
    print(f"\n📋 ÉTAPE {step_num}: {title}")
    print("-" * 50)

def check_aws_cli():
    """Vérifie si AWS CLI est installé"""
    try:
        result = subprocess.run(["aws", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✅ AWS CLI installé: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ AWS CLI n'est pas installé")
        return False

def install_aws_cli():
    """Guide pour installer AWS CLI"""
    print("\n🔧 INSTALLATION AWS CLI")
    print("\nOption 1 - Téléchargement manuel (RECOMMANDÉ):")
    print("1. Allez sur: https://aws.amazon.com/cli/")
    print("2. Téléchargez AWS CLI v2 pour Windows (MSI)")
    print("3. Exécutez le fichier téléchargé")
    print("4. Redémarrez ce terminal")
    
    print("\nOption 2 - PowerShell:")
    print("Invoke-WebRequest -Uri 'https://awscli.amazonaws.com/AWSCLIV2.msi' -OutFile 'AWSCLIV2.msi'")
    print("Start-Process msiexec.exe -Wait -ArgumentList '/I AWSCLIV2.msi /quiet'")

def show_iam_setup_guide():
    """Guide pour configurer IAM"""
    print("\n👤 CONFIGURATION IAM - ÉTAPES DÉTAILLÉES")
    
    print("\n1. 🌐 Accéder à la console IAM:")
    print("   https://console.aws.amazon.com/iam/")
    
    print("\n2. 📝 Créer un utilisateur:")
    print("   • Cliquez sur 'Users' → 'Add user'")
    print("   • Nom d'utilisateur: 'chatbot-telegram-user'")
    print("   • Access type: 'Programmatic access'")
    
    print("\n3. 🔐 Attacher les permissions:")
    print("   • 'Attach existing policies directly'")
    print("   • Rechercher et sélectionner: 'AmazonDynamoDBFullAccess'")
    print("   • (Pour la production, créer une policy plus restrictive)")
    
    print("\n4. 🔑 Récupérer les clés:")
    print("   • Copier 'Access Key ID'")
    print("   • Copier 'Secret Access Key'")
    print("   • ⚠️  ATTENTION: La Secret Key n'est visible qu'une seule fois!")

def show_aws_configure_guide():
    """Guide pour configurer AWS CLI"""
    print("\n⚙️  CONFIGURATION AWS CLI")
    print("\nExécutez cette commande et remplissez avec vos clés:")
    print("aws configure")
    print("\nInformations à fournir:")
    print("• AWS Access Key ID: [Votre Access Key]")
    print("• AWS Secret Access Key: [Votre Secret Key]")
    print("• Default region name: eu-north-1")
    print("• Default output format: json")

def show_dynamodb_setup():
    """Guide pour créer la table DynamoDB"""
    print("\n🗄️  CRÉATION TABLE DYNAMODB")
    print("\nOption 1 - Ligne de commande (AWS CLI):")
    print("""
aws dynamodb create-table \\
    --table-name chatbot-conversations \\
    --attribute-definitions \\
        AttributeName=conversation_id,AttributeType=S \\
        AttributeName=timestamp,AttributeType=N \\
    --key-schema \\
        AttributeName=conversation_id,KeyType=HASH \\
        AttributeName=timestamp,KeyType=RANGE \\
    --billing-mode PAY_PER_REQUEST \\
    --region eu-north-1
    """)
    
    print("\nOption 2 - Console Web:")
    print("1. Allez sur: https://eu-north-1.console.aws.amazon.com/dynamodb/")
    print("2. Cliquez 'Create table'")
    print("3. Table name: 'chatbot-conversations'")
    print("4. Partition key: 'conversation_id' (String)")
    print("5. Sort key: 'timestamp' (Number)")
    print("6. Settings: 'Default settings'")
    print("7. Cliquez 'Create table'")

def test_aws_connection():
    """Teste la connexion AWS"""
    print("\n🧪 TEST DE LA CONNEXION")
    print("\nPour tester votre configuration, exécutez:")
    print("aws sts get-caller-identity")
    print("\nSi ça fonctionne, vous verrez votre identité AWS")

def update_env_file():
    """Guide pour mettre à jour le fichier .env"""
    print("\n📄 MISE À JOUR DU FICHIER .ENV")
    print("\nAjoutez ces lignes à votre fichier .env:")
    print("AWS_REGION=eu-north-1")
    print("DYNAMO_TABLE=chatbot-conversations")
    print("AWS_PROFILE=default")
    print("\n⚠️  Les credentials sont dans ~/.aws/credentials (créé par 'aws configure')")

def main():
    """Fonction principale"""
    print_header("CONFIGURATION AWS + DYNAMODB POUR CHATBOT TELEGRAM")
    
    print("\n🎯 VOTRE CAS D'USAGE: 'Local code'")
    print("✅ Développement local Windows")
    print("✅ Bot en localhost avec ngrok") 
    print("✅ Accès DynamoDB depuis Python")
    
    # Étape 1: Vérifier AWS CLI
    print_step(1, "VÉRIFICATION AWS CLI")
    if not check_aws_cli():
        install_aws_cli()
        print("\n⏸️  Installer AWS CLI puis relancer ce script")
        return
    
    # Étape 2: Configuration IAM
    print_step(2, "CONFIGURATION IAM")
    show_iam_setup_guide()
    
    # Étape 3: Configuration AWS CLI
    print_step(3, "CONFIGURATION AWS CLI")
    show_aws_configure_guide()
    
    # Étape 4: Création DynamoDB
    print_step(4, "CRÉATION TABLE DYNAMODB")
    show_dynamodb_setup()
    
    # Étape 5: Tests
    print_step(5, "TESTS")
    test_aws_connection()
    
    # Étape 6: Mise à jour .env
    print_step(6, "CONFIGURATION FINALE")
    update_env_file()
    
    print_header("RÉCAPITULATIF")
    print("1. ✅ Installer AWS CLI")
    print("2. 👤 Créer utilisateur IAM avec permissions DynamoDB")
    print("3. ⚙️  Configurer AWS CLI avec 'aws configure'")
    print("4. 🗄️  Créer table DynamoDB 'chatbot-conversations'")
    print("5. 🧪 Tester avec 'aws sts get-caller-identity'")
    print("6. 📄 Mettre à jour le fichier .env")
    
    print(f"\n🎉 Votre bot pourra alors utiliser DynamoDB pour stocker les conversations!")

if __name__ == "__main__":
    main()
