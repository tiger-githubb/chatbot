#!/usr/bin/env python3
"""
Script de test complet pour vérifier que le chatbot fonctionne
"""

import requests
import json
import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import settings

def test_api_health():
    """Test que l'API FastAPI répond"""
    try:
        response = requests.get(f"{settings.API_URL}/docs")
        print(f"✅ API FastAPI: Status {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ API FastAPI: Erreur - {e}")
        return False

def test_webhook_endpoint():
    """Test l'endpoint webhook"""
    try:
        # Créer un faux message Telegram pour le test
        test_message = {
            "update_id": 12345,
            "message": {
                "message_id": 1,
                "date": 1625097600,
                "chat": {
                    "id": 123456789,
                    "type": "private"
                },
                "from": {
                    "id": 123456789,
                    "is_bot": False,
                    "first_name": "Test",
                    "username": "testuser"
                },
                "text": "/start"
            }
        }
        
        response = requests.post(
            f"{settings.API_URL}{settings.TELEGRAM_WEBHOOK_PATH}",
            json=test_message,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Webhook Telegram: Status {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Webhook Telegram: Erreur - {e}")
        return False

def test_telegram_webhook_config():
    """Test la configuration du webhook Telegram"""
    try:
        bot_token = settings.TELEGRAM_BOT_TOKEN
        response = requests.get(f"https://api.telegram.org/bot{bot_token}/getWebhookInfo")
        
        if response.status_code == 200:
            webhook_info = response.json()
            current_url = webhook_info.get("result", {}).get("url", "")
            expected_url = f"{settings.TELEGRAM_WEBHOOK_URL}{settings.TELEGRAM_WEBHOOK_PATH}"
            
            if current_url == expected_url:
                print(f"✅ Configuration Webhook: {current_url}")
                return True
            else:
                print(f"⚠️ Webhook mal configuré: {current_url} != {expected_url}")
                return False
        else:
            print(f"❌ Erreur lors de la vérification du webhook: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Configuration Webhook: Erreur - {e}")
        return False

def test_mistral_api():
    """Test la connexion à l'API Mistral"""
    try:
        from mistralai.client import MistralClient
        client = MistralClient(api_key=settings.MISTRAL_API_KEY)
        
        # Test simple avec Mistral
        response = client.chat(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        if response and response.choices:
            print("✅ API Mistral: Connexion réussie")
            return True
        else:
            print("❌ API Mistral: Pas de réponse")
            return False
    except Exception as e:
        print(f"❌ API Mistral: Erreur - {e}")
        return False

def main():
    """Exécute tous les tests"""
    print("🚀 Test complet du système chatbot")
    print("=" * 50)
    
    tests = [
        ("API FastAPI", test_api_health),
        ("Endpoint Webhook", test_webhook_endpoint),
        ("Configuration Telegram", test_telegram_webhook_config),
        ("API Mistral", test_mistral_api)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Test: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}: Exception - {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS DES TESTS")
    print("=" * 50)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result for _, result in results)
    if all_passed:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
        print("💬 Votre chatbot est prêt à recevoir des messages!")
        print(f"🔗 URL Webhook: {settings.TELEGRAM_WEBHOOK_URL}{settings.TELEGRAM_WEBHOOK_PATH}")
        print(f"📱 Testez en envoyant un message à votre bot Telegram")
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez la configuration dans le fichier .env")

if __name__ == "__main__":
    main()
