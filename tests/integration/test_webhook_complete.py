#!/usr/bin/env python3
"""
Test du webhook Telegram pour diagnostiquer les problèmes
"""

import requests
import json
import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
src_dir = Path(__file__).parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

def test_webhook_endpoint():
    """Test direct de l'endpoint webhook"""
    print("🧪 Test de l'endpoint webhook Telegram...")
    
    # Données de test qui simulent un update Telegram (format exact de Telegram)
    test_update = {
        "update_id": 123456789,
        "message": {
            "message_id": 1,
            "from": {
                "id": 123456789,
                "is_bot": False,
                "first_name": "Test",
                "username": "test_user",
                "language_code": "fr"
            },
            "chat": {
                "id": 123456789,
                "first_name": "Test",
                "username": "test_user",
                "type": "private"
            },
            "date": 1640995200,
            "text": "Hello bot!"
        }
    }
    
    try:
        # Test de l'endpoint webhook
        response = requests.post(
            "http://localhost:8001/telegram/webhook",
            json=test_update,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📝 Response: {response.text}")
        
        if response.status_code == 200:
            try:
                json_response = response.json()
                if json_response.get("status") == "ok":
                    print("✅ Webhook endpoint fonctionne correctement!")
                    return True
                else:
                    print(f"⚠️ Réponse inattendue: {json_response}")
                    return False
            except json.JSONDecodeError:
                print("⚠️ Réponse non-JSON reçue")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API")
        print("💡 Assurez-vous que l'API est démarrée avec:")
        print("   cd src && python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_config():
    """Test de la configuration"""
    print("\n🔧 Test de la configuration...")
    
    try:
        from config import settings
        print("✅ Configuration chargée")
        print(f"   - ENV_NAME: {settings.ENV_NAME}")
        print(f"   - TELEGRAM_BOT_TOKEN: {'✅ Configuré' if settings.TELEGRAM_BOT_TOKEN else '❌ Manquant'}")
        print(f"   - TELEGRAM_WEBHOOK_PATH: {settings.TELEGRAM_WEBHOOK_PATH}")
        print(f"   - API_URL: {settings.API_URL}")
        print(f"   - MISTRAL_API_KEY: {'✅ Configuré' if settings.MISTRAL_API_KEY else '❌ Manquant'}")
        return bool(settings.TELEGRAM_BOT_TOKEN and settings.MISTRAL_API_KEY)
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        return False

def test_telegram_bot_import():
    """Test de l'import du bot Telegram"""
    print("\n📦 Test de l'import TelegramBot...")
    
    try:
        from telegram_bot import telegram_bot
        print("✅ TelegramBot importé avec succès")
        print(f"   - Application type: {type(telegram_bot.application).__name__}")
        print(f"   - Handlers count: {len(telegram_bot.application.handlers)}")
        return True
    except Exception as e:
        print(f"❌ Erreur d'import TelegramBot: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_running():
    """Test si l'API FastAPI est en cours d'exécution"""
    print("\n🚀 Test de l'API FastAPI...")
    
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        if response.status_code in [200, 307]:  # 307 = redirect vers /docs
            print("✅ API FastAPI en cours d'exécution")
            
            # Test de l'endpoint docs
            docs_response = requests.get("http://localhost:8001/docs", timeout=5)
            if docs_response.status_code == 200:
                print("✅ Documentation Swagger accessible")
            
            return True
        else:
            print(f"❌ API répond avec status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API non accessible")
        return False
    except Exception as e:
        print(f"❌ Erreur API: {e}")
        return False

def test_chat_endpoint():
    """Test de l'endpoint /chat"""
    print("\n💬 Test de l'endpoint /chat...")
    
    try:
        response = requests.get(
            "http://localhost:8001/chat",
            params={"question": "Hello, test question"},
            timeout=15
        )
        
        if response.status_code == 200:
            print("✅ Endpoint /chat accessible")
            data = response.json()
            if "answer" in data:
                print("✅ Mistral AI répond correctement")
                return True
            else:
                print("⚠️ Réponse sans champ 'answer'")
                return False
        else:
            print(f"❌ Endpoint /chat erreur: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur endpoint /chat: {e}")
        return False

def main():
    """Test principal"""
    print("🔍 Diagnostic complet du webhook Telegram")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: API running
    if test_api_running():
        tests_passed += 1
    
    # Test 2: Configuration
    if test_config():
        tests_passed += 1
    
    # Test 3: TelegramBot import
    if test_telegram_bot_import():
        tests_passed += 1
    
    # Test 4: Chat endpoint
    if test_chat_endpoint():
        tests_passed += 1
    
    # Test 5: Webhook endpoint
    if test_webhook_endpoint():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 Tous les tests sont passés! Le webhook devrait fonctionner.")
        print("\n💡 Pour utiliser le webhook:")
        print("1. Installez ngrok: https://ngrok.com/download")
        print("2. Exposez l'API: ngrok http 8001")
        print("3. Configurez le webhook: python tools/set_webhook.py set --url https://YOUR_NGROK_URL.ngrok.io/telegram/webhook")
    else:
        print("❌ Certains tests ont échoué. Corrigez les problèmes avant d'utiliser le webhook.")
        
        if tests_passed == 0:
            print("\n🚨 Problèmes critiques détectés:")
            print("   - Vérifiez que l'API est démarrée")
            print("   - Vérifiez le fichier .env")
            print("   - Vérifiez les dépendances installées")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
