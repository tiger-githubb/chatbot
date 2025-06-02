#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration du MVP Telegram Bot
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path pour l'import
src_dir = Path(__file__).parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

def test_config():
    """Test de la configuration"""
    print("🔧 Test de la configuration...")
    try:
        from config import settings
        print(f"✅ Configuration chargée")
        print(f"   - ENV_NAME: {settings.ENV_NAME}")
        print(f"   - AWS_REGION: {settings.AWS_REGION}")
        print(f"   - DYNAMO_TABLE: {settings.DYNAMO_TABLE}")
        print(f"   - MISTRAL_API_KEY: {'✅ Configuré' if settings.MISTRAL_API_KEY else '❌ Manquant'}")
        print(f"   - TELEGRAM_BOT_TOKEN: {'✅ Configuré' if settings.TELEGRAM_BOT_TOKEN else '❌ Manquant'}")
        print(f"   - TELEGRAM_WEBHOOK_PATH: {settings.TELEGRAM_WEBHOOK_PATH}")
        return True
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        return False

def test_imports():
    """Test des imports essentiels"""
    print("\n📦 Test des imports...")
    
    # Test FastAPI
    try:
        import fastapi
        print("✅ FastAPI disponible")
    except ImportError:
        print("❌ FastAPI manquant - pip install fastapi")
        return False
    
    # Test python-telegram-bot
    try:
        import telegram
        print("✅ python-telegram-bot disponible")
    except ImportError:
        print("❌ python-telegram-bot manquant - pip install python-telegram-bot")
        return False
    
    # Test Mistral AI
    try:
        import mistralai
        print("✅ mistralai disponible")
    except ImportError:
        print("❌ mistralai manquant - pip install mistralai")
        return False
    
    # Test boto3
    try:
        import boto3
        print("✅ boto3 disponible")
    except ImportError:
        print("❌ boto3 manquant - pip install boto3")
        return False
    
    return True

def test_api_startup():
    """Test du démarrage de l'API"""
    print("\n🚀 Test du démarrage de l'API...")
    try:
        from main import app
        print("✅ API FastAPI initialisée")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du démarrage de l'API: {e}")
        return False

def test_telegram_bot():
    """Test du bot Telegram"""
    print("\n🤖 Test du bot Telegram...")
    try:
        from telegram_bot import telegram_bot
        print("✅ Bot Telegram initialisé")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation du bot: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🎯 Test du MVP Chatbot Telegram")
    print("=" * 50)
    
    # Vérifier si .env existe
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        print("⚠️  Fichier .env manquant!")
        print("   Copiez .env.example vers .env et configurez vos variables.")
        print("   cp .env.example .env")
        return False
    
    tests = [
        test_config,
        test_imports,
        test_api_startup,
        test_telegram_bot
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    if all(results):
        print("🎉 Tous les tests sont passés !")
        print("📋 Prochaines étapes :")
        print("   1. Configurez vos vraies clés API dans .env")
        print("   2. Testez localement: python src/main.py")
        print("   3. Déployez sur AWS avec: make deploy")
        return True
    else:
        print("❌ Certains tests ont échoué.")
        print("🔧 Installez les dépendances manquantes:")
        print("   pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
