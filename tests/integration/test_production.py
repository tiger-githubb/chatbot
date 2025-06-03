#!/usr/bin/env python3
"""
Script de test en production pour le webhook Telegram
Surveille les logs et teste les fonctionnalités
"""

import time
import requests
import json
from datetime import datetime

def test_production_webhook():
    """Test du webhook en production"""
    
    print("🚀 TEST DE PRODUCTION - WEBHOOK TELEGRAM")
    print("=" * 50)
    print(f"⏰ Heure: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # URLs de production
    ngrok_url = "https://1d8c-102-64-172-180.ngrok-free.app"
    webhook_url = f"{ngrok_url}/telegram/webhook"
    chat_url = f"{ngrok_url}/chat"
    
    print("🌐 URLs de Production:")
    print(f"   Webhook: {webhook_url}")
    print(f"   Chat API: {chat_url}")
    print()
    
    # Test 1: Vérifier que l'API est accessible publiquement
    print("🧪 Test 1: Accessibilité publique de l'API...")
    try:
        response = requests.get(f"{ngrok_url}/docs", timeout=10)
        if response.status_code == 200:
            print("   ✅ API accessible publiquement")
        else:
            print(f"   ❌ Erreur d'accès: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur de connexion: {e}")
    
    # Test 2: Tester l'endpoint chat en public
    print("\n💬 Test 2: Endpoint Chat public...")
    try:
        response = requests.get(f"{chat_url}?question=Hello from production!", timeout=15)
        if response.status_code == 200:
            data = response.json()
            answer = data.get('answer', {}).get('S', 'No answer')[:100]
            print(f"   ✅ Chat API fonctionne: {answer}...")
        else:
            print(f"   ❌ Erreur chat: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur chat: {e}")
    
    # Test 3: Simuler un webhook Telegram
    print("\n🔗 Test 3: Simulation webhook Telegram...")
    test_message = {
        "update_id": 999999999,
        "message": {
            "message_id": 1,
            "from": {
                "id": 123456789,
                "is_bot": False,
                "first_name": "Production",
                "username": "test_prod",
                "language_code": "fr"
            },
            "chat": {
                "id": 123456789,
                "first_name": "Production", 
                "username": "test_prod",
                "type": "private"
            },
            "date": int(time.time()),
            "text": "/start"
        }
    }
    
    try:
        response = requests.post(
            webhook_url, 
            json=test_message, 
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print(f"   ✅ Webhook répond: {response.text}")
        else:
            print(f"   ❌ Erreur webhook: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur webhook: {e}")
    
    print("\n" + "=" * 50)
    print("📱 MAINTENANT, TESTEZ AVEC DE VRAIS MESSAGES TELEGRAM !")
    print("   1. Ouvrez Telegram")
    print("   2. Cherchez votre bot")
    print("   3. Envoyez /start")
    print("   4. Envoyez des messages")
    print("=" * 50)

if __name__ == "__main__":
    test_production_webhook()
