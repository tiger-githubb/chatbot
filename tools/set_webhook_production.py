#!/usr/bin/env python3
"""
Script pour configurer le webhook Telegram avec l'URL AWS Lambda
"""

import requests
import sys
from dotenv import load_dotenv
import os

# Charger les variables d'environnement de production
load_dotenv('.env.production')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = f"{os.getenv('TELEGRAM_WEBHOOK_URL')}{os.getenv('TELEGRAM_WEBHOOK_PATH')}"

def set_webhook():
    """Configure le webhook Telegram pour AWS Lambda"""
    
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN manquant")
        return False
    
    if not WEBHOOK_URL or 'localhost' in WEBHOOK_URL:
        print("❌ URL de webhook invalide pour la production")
        return False
    
    print(f"🔧 Configuration du webhook Telegram...")
    print(f"📡 URL: {WEBHOOK_URL}")
    
    # URL de l'API Telegram
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    
    # Paramètres du webhook
    payload = {
        'url': WEBHOOK_URL,
        'drop_pending_updates': True  # Supprimer les mises à jour en attente
    }
    
    try:
        response = requests.post(api_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                print("✅ Webhook configuré avec succès!")
                print(f"📋 Détails: {result.get('description', 'N/A')}")
                return True
            else:
                print(f"❌ Erreur Telegram: {result.get('description', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            print(f"📋 Réponse: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def get_webhook_info():
    """Récupère les informations du webhook actuel"""
    
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getWebhookInfo"
    
    try:
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                webhook_info = result.get('result', {})
                print("📋 Informations du webhook actuel:")
                print(f"   URL: {webhook_info.get('url', 'Aucune')}")
                print(f"   Pending updates: {webhook_info.get('pending_update_count', 0)}")
                print(f"   Last error: {webhook_info.get('last_error_message', 'Aucune')}")
                return webhook_info
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération des infos: {e}")
    
    return None

if __name__ == "__main__":
    print("🤖 Configuration du webhook Telegram pour AWS Lambda")
    print("=" * 50)
    
    # Afficher les informations actuelles
    print("\n📋 Informations actuelles:")
    get_webhook_info()
    
    # Configurer le nouveau webhook
    print("\n🔧 Configuration du nouveau webhook:")
    success = set_webhook()
    
    if success:
        print("\n✅ Configuration terminée!")
        print("\n📋 Vérification finale:")
        get_webhook_info()
        print("\n🚀 Votre bot Telegram devrait maintenant fonctionner avec AWS Lambda!")
    else:
        print("\n❌ Échec de la configuration")
        sys.exit(1)
