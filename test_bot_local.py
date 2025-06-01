#!/usr/bin/env python3
"""
Script de test pour le bot Telegram en mode polling local
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path pour l'import
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_bot_polling():
    """Test du bot en mode polling local"""
    print("🤖 Test du bot Telegram en mode polling...")
    print("⚠️  ATTENTION: Ce test va démarrer le bot en mode polling.")
    print("   Le bot va écouter les messages Telegram en temps réel.")
    print("   Appuyez sur Ctrl+C pour arrêter.")
    
    confirm = input("\n🔧 Voulez-vous continuer ? (y/N): ")
    if confirm.lower() != 'y':
        print("❌ Test annulé.")
        return
    
    try:
        from telegram_bot import TelegramBot
        from config import settings
        
        if not settings.TELEGRAM_BOT_TOKEN:
            print("❌ TELEGRAM_BOT_TOKEN manquant dans .env")
            return
            
        print(f"✅ Token configuré: {settings.TELEGRAM_BOT_TOKEN[:10]}...")
        print("\n🚀 Démarrage du bot en mode polling...")
        print("📱 Ouvrez Telegram et envoyez /start à votre bot !")
        
        bot = TelegramBot()
        bot.run_polling()
        
    except KeyboardInterrupt:
        print("\n⏹️  Bot arrêté par l'utilisateur.")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_bot_polling()
