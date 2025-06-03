#!/usr/bin/env python3
"""
Script de test avancé pour le webhook Telegram dans le projet chatbot
"""

import sys
import os
import json
import requests
from pathlib import Path

# Ajouter le répertoire src au path pour l'import
src_dir = Path(__file__).parent / "chatbot" / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

def test_webhook_endpoint():
    """Test de l'endpoint webhook"""
    print("🔧 Test de l'endpoint webhook...")
    
    # Données de test d'un message Telegram
    test_update = {
        "update_id": 123456789,
        "message": {
            "message_id": 1,
            "from": {
                "id": 987654321,
                "is_bot": False,
                "first_name": "Test",
                "username": "testuser"
            },
            "chat": {
                "id": 987654321,
                "first_name": "Test",
                "username": "testuser",
                "type": "private"
            },
            "date": 1234567890,
            "text": "Hello bot!"
        }
    }
    
    try:
        # Test de l'endpoint webhook
        response = requests.post(
            "http://localhost:8001/telegram/webhook",
            json=test_update,
            timeout=10
        )
        
        print(f"✅ Statut HTTP: {response.status_code}")
        print(f"✅ Réponse: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook fonctionne correctement!")
            return True
        else:
            print(f"❌ Webhook a échoué avec le statut: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur FastAPI")
        print("   Vérifiez que le serveur est démarré avec: uvicorn src.main:app --host 0.0.0.0 --port 8001")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test webhook: {e}")
        return False

def test_api_availability():
    """Test de disponibilité de l'API"""
    print("🌐 Test de l'API...")
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        if response.status_code == 200:
            print("✅ API disponible")
            return True
        else:
            print(f"❌ API répond avec le statut: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API non disponible: {e}")
        return False

def show_webhook_debug_info():
    """Affiche les informations de debug pour le webhook"""
    print("\n🔍 Informations de debug:")
    print("=" * 50)
    
    try:
        from config import settings
        print(f"TELEGRAM_BOT_TOKEN: {'✅ Configuré' if settings.TELEGRAM_BOT_TOKEN else '❌ Manquant'}")
        print(f"TELEGRAM_WEBHOOK_PATH: {settings.TELEGRAM_WEBHOOK_PATH}")
        print(f"TELEGRAM_WEBHOOK_URL: {settings.TELEGRAM_WEBHOOK_URL or 'Non configuré'}")
        print(f"API_URL: {settings.API_URL}")
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de la config: {e}")

def main():
    print("🤖 Test complet du webhook Telegram\n")
    
    # Test 1: Disponibilité de l'API
    if not test_api_availability():
        print("\n❌ Tests arrêtés - API non disponible")
        return
    
    # Test 2: Endpoint webhook
    webhook_ok = test_webhook_endpoint()
    
    # Affichage des infos de debug
    show_webhook_debug_info()
    
    print("\n" + "=" * 50)
    if webhook_ok:
        print("✅ SUCCÈS: Le webhook fonctionne!")
        print("\n🚀 Prochaines étapes:")
        print("1. Configurer ngrok ou un tunnel pour exposer le webhook")
        print("2. Utiliser tools/set_webhook.py pour configurer Telegram")
        print("3. Tester avec de vrais messages Telegram")
    else:
        print("❌ ÉCHEC: Le webhook ne fonctionne pas")
        print("\n🔧 Actions recommandées:")
        print("1. Vérifiez que FastAPI est démarré: uvicorn src.main:app --host 0.0.0.0 --port 8001")
        print("2. Vérifiez la configuration dans .env")
        print("3. Examinez les logs d'erreur")

if __name__ == "__main__":
    main()
