#!/usr/bin/env python3
"""
Script pour configurer le webhook Telegram dans le projet chatbot
Adapté depuis chatbot-alvin avec améliorations
"""

import os
import sys
import argparse
import requests
from pathlib import Path

# Ajouter le répertoire src au path pour l'import
src_dir = Path(__file__).parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

def setup_webhook(webhook_url):
    """
    Configure le webhook Telegram pour le bot.
    
    Args:
        webhook_url (str): L'URL complète du webhook (https://...)
    """
    try:
        from config import settings
        
        bot_token = settings.TELEGRAM_BOT_TOKEN
        if not bot_token:
            print("❌ Erreur: TELEGRAM_BOT_TOKEN non défini dans .env")
            sys.exit(1)

        if not webhook_url.startswith('https://'):
            print("❌ Erreur: L'URL du webhook doit commencer par https://")
            print("   Exemple: https://abc123.ngrok.io/telegram/webhook")
            sys.exit(1)

        # URL de l'API Telegram pour configurer le webhook
        api_url = f"https://api.telegram.org/bot{bot_token}/setWebhook"

        print(f"🔧 Configuration du webhook Telegram...")
        print(f"   Bot Token: {bot_token[:10]}...")
        print(f"   Webhook URL: {webhook_url}")

        # Vérifier d'abord le webhook actuel
        print("📋 Vérification du webhook actuel...")
        info_response = requests.get(
            f"https://api.telegram.org/bot{bot_token}/getWebhookInfo",
            timeout=10
        )
        info_response.raise_for_status()
        current_webhook = info_response.json()
        
        if 'result' in current_webhook and 'url' in current_webhook['result']:
            current_url = current_webhook['result']['url']
            if current_url == webhook_url:
                print(f"✅ Le webhook est déjà configuré sur {webhook_url}")
                return
            if current_url:
                print(f"🔄 Modification du webhook: {current_url} → {webhook_url}")
            else:
                print(f"🆕 Configuration initiale du webhook sur {webhook_url}")
        else:
            print(f"🆕 Configuration initiale du webhook sur {webhook_url}")

        # Configurer le nouveau webhook
        print("🚀 Configuration en cours...")
        response = requests.post(
            api_url,
            json={
                'url': webhook_url,
                'allowed_updates': ['message', 'callback_query'],
                'drop_pending_updates': True
            },
            timeout=10
        )
        response.raise_for_status()
        
        result = response.json()
        if result.get('ok'):
            print("✅ Webhook configuré avec succès!")
            print("\n📝 Informations:")
            print(f"   - URL: {webhook_url}")
            print(f"   - Mises à jour autorisées: message, callback_query")
            print(f"   - Mises à jour en attente supprimées: Oui")
            
            # Vérifier la configuration
            print("\n🔍 Vérification de la configuration...")
            verify_response = requests.get(
                f"https://api.telegram.org/bot{bot_token}/getWebhookInfo",
                timeout=10
            )
            if verify_response.status_code == 200:
                webhook_info = verify_response.json()['result']
                print(f"   - URL configurée: {webhook_info.get('url', 'Non définie')}")
                print(f"   - Dernière erreur: {webhook_info.get('last_error_message', 'Aucune')}")
        else:
            print(f"❌ Erreur: {result.get('description', 'Erreur inconnue')}")
            sys.exit(1)

    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("   Vérifiez que vous êtes dans le bon répertoire et que les dépendances sont installées")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la configuration du webhook: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur inattendue: {str(e)}")
        sys.exit(1)

def remove_webhook():
    """Supprime le webhook Telegram"""
    try:
        from config import settings
        
        bot_token = settings.TELEGRAM_BOT_TOKEN
        if not bot_token:
            print("❌ Erreur: TELEGRAM_BOT_TOKEN non défini dans .env")
            sys.exit(1)

        print("🗑️  Suppression du webhook...")
        
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/deleteWebhook",
            json={'drop_pending_updates': True},
            timeout=10
        )
        response.raise_for_status()
        
        result = response.json()
        if result.get('ok'):
            print("✅ Webhook supprimé avec succès!")
            print("   Le bot peut maintenant fonctionner en mode polling local")
        else:
            print(f"❌ Erreur: {result.get('description', 'Erreur inconnue')}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la suppression: {str(e)}")

def check_webhook_status():
    """Vérifie le statut actuel du webhook"""
    try:
        from config import settings
        
        bot_token = settings.TELEGRAM_BOT_TOKEN
        if not bot_token:
            print("❌ Erreur: TELEGRAM_BOT_TOKEN non défini dans .env")
            sys.exit(1)

        print("📋 Vérification du statut du webhook...")
        
        response = requests.get(
            f"https://api.telegram.org/bot{bot_token}/getWebhookInfo",
            timeout=10
        )
        response.raise_for_status()
        
        webhook_info = response.json()['result']
        url = webhook_info.get('url', '')
        
        if url:
            print(f"✅ Webhook configuré:")
            print(f"   - URL: {url}")
            print(f"   - Mises à jour en attente: {webhook_info.get('pending_update_count', 0)}")
            print(f"   - Dernière erreur: {webhook_info.get('last_error_message', 'Aucune')}")
            print(f"   - Date dernière erreur: {webhook_info.get('last_error_date', 'N/A')}")
        else:
            print("ℹ️  Aucun webhook configuré (mode polling)")
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description='Gestion du webhook Telegram pour le projet chatbot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python tools/set_webhook.py --url https://abc123.ngrok.io/telegram/webhook
  python tools/set_webhook.py --status
  python tools/set_webhook.py --remove
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', help='URL du webhook (https://...)')
    group.add_argument('--status', action='store_true', help='Vérifier le statut du webhook')
    group.add_argument('--remove', action='store_true', help='Supprimer le webhook')
    
    args = parser.parse_args()
    
    if args.url:
        setup_webhook(args.url)
    elif args.status:
        check_webhook_status()
    elif args.remove:
        remove_webhook()

if __name__ == "__main__":
    main()
