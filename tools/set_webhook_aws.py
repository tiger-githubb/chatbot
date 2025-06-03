#!/usr/bin/env python3
"""
Configuration du webhook Telegram pour le déploiement AWS
"""

import requests
import os
from pathlib import Path
import sys

# Ajouter le répertoire src au path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

def set_webhook_aws():
    """Configure le webhook Telegram avec l'URL AWS"""
    
    # URL AWS Lambda
    aws_base_url = "https://hky4t9y1fh.execute-api.eu-west-3.amazonaws.com"
    webhook_path = "/telegram/webhook"
    webhook_url = aws_base_url + webhook_path
    
    # Token du bot (à injecter via les variables d'environnement Jenkins)
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN non trouvé dans les variables d'environnement")
        return False
    
    # Configuration du webhook
    telegram_api_url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    
    payload = {
        "url": webhook_url,
        "allowed_updates": ["message", "callback_query"]
    }
    
    print(f"🔧 Configuration du webhook Telegram...")
    print(f"   URL: {webhook_url}")
    
    try:
        response = requests.post(telegram_api_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("ok"):
                print("✅ Webhook configuré avec succès !")
                print(f"   Description: {result.get('description', 'N/A')}")
                return True
            else:
                print(f"❌ Erreur API Telegram: {result.get('description', 'Erreur inconnue')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la configuration: {e}")
        return False

def get_webhook_info():
    """Récupère les informations actuelles du webhook"""
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN non trouvé")
        return False
    
    telegram_api_url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    
    try:
        response = requests.get(telegram_api_url, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("ok"):
                webhook_info = result.get("result", {})
                print("📋 Informations du webhook actuel:")
                print(f"   URL: {webhook_info.get('url', 'Non configuré')}")
                print(f"   Dernière erreur: {webhook_info.get('last_error_message', 'Aucune')}")
                print(f"   Nombre d'erreurs en attente: {webhook_info.get('pending_update_count', 0)}")
                return True
            else:
                print(f"❌ Erreur API: {result.get('description')}")
                return False
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Configuration du webhook Telegram pour AWS")
    print("=" * 50)
    
    # Afficher les infos actuelles
    print("\n1. État actuel du webhook:")
    get_webhook_info()
    
    # Configurer le nouveau webhook
    print("\n2. Configuration du nouveau webhook:")
    success = set_webhook_aws()
    
    if success:
        print("\n3. Vérification de la nouvelle configuration:")
        get_webhook_info()
        print("\n✅ Configuration terminée avec succès !")
    else:
        print("\n❌ Échec de la configuration")
        sys.exit(1)
