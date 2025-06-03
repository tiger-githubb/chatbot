#!/usr/bin/env python3
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🧪 Testing imports for AWS Lambda...")
    
    # Test import config
    from src.config import settings
    print("✅ Config import OK")
    
    # Test import utils
    from src.utils import Utils
    print("✅ Utils import OK")
    
    # Test import telegram_bot
    from src.telegram_bot import TelegramBot
    print("✅ TelegramBot import OK")
    
    # Test import main et handler
    from src.main import app, handler
    print("✅ FastAPI app import OK")
    print("✅ Mangum handler import OK")
    
    print("\n🚀 ALL TESTS PASSED! Ready for AWS Lambda deployment!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
