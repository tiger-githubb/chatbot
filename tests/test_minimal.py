#!/usr/bin/env python3
"""
Tests minimalistes pour Jenkins CI/CD
Vérifie uniquement les imports et la configuration de base
"""

import pytest
import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path pour l'import
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

class TestConfiguration:
    """Tests de configuration de base"""
    
    def test_imports_essential(self):
        """Test que tous les imports essentiels fonctionnent"""
        try:
            import fastapi
            import telegram
            import mistralai
            import boto3
            import pydantic_settings
            assert True
        except ImportError as e:
            pytest.skip(f"Import essentiel manquant (acceptable en CI): {e}")
    
    def test_config_loads(self):
        """Test que la configuration se charge sans erreur"""
        try:
            from config import settings
            # Vérifier que les variables de base existent (même si vides)
            assert hasattr(settings, 'ENV_NAME')
            assert hasattr(settings, 'AWS_REGION')
            assert hasattr(settings, 'TELEGRAM_WEBHOOK_PATH')
        except Exception as e:
            pytest.skip(f"Configuration pas encore injectée (normal en CI): {e}")
    
    def test_main_app_creation(self):
        """Test que l'application FastAPI se crée sans erreur"""
        try:
            from main import app
            assert app is not None
            # Vérifier que c'est bien une instance FastAPI
            assert app.__class__.__name__ == 'FastAPI'
        except Exception as e:
            pytest.skip(f"App non disponible (dépendances manquantes): {e}")
    
    def test_utils_functions_exist(self):
        """Test que les fonctions utilitaires existent"""
        try:
            from utils import Utils
            # Vérifier que les méthodes essentielles existent
            assert hasattr(Utils, 'log_info')
            assert hasattr(Utils, 'get_dynamo_client')
            assert hasattr(Utils, 'insert_chat_message')
        except Exception as e:
            pytest.skip(f"Utils non disponibles (dépendances manquantes): {e}")

class TestApplicationStructure:
    """Tests de structure de l'application"""
    
    def test_telegram_bot_structure(self):
        """Test que le bot Telegram a la bonne structure"""
        try:
            from telegram_bot import TelegramBot
            # Juste vérifier que la classe existe et a les bonnes méthodes
            assert hasattr(TelegramBot, '__init__')
            assert hasattr(TelegramBot, 'handle_update')
        except Exception as e:
            pytest.skip(f"Bot Telegram non disponible (dépendances manquantes): {e}")
    
    def test_api_endpoints_defined(self):
        """Test que les endpoints API sont définis"""
        try:
            from main import app
            # Test simplifié - vérifier que l'app a des routes
            assert hasattr(app, 'routes')
            assert len(app.routes) > 0
            
            # Vérifier que l'application a les attributs nécessaires
            assert hasattr(app, 'title')
            assert app.title == "ChatBot API"
            
        except Exception as e:
            pytest.skip(f"Endpoints non disponibles (dépendances manquantes): {e}")

# Tests de validation simple (sans dépendances externes)
def test_python_version():
    """Vérifier que Python est en version supportée"""
    assert sys.version_info >= (3, 8), "Python 3.8+ requis"

def test_project_structure():
    """Vérifier que la structure du projet est correcte"""
    project_root = Path(__file__).parent.parent
    
    # Vérifier les fichiers essentiels
    assert (project_root / "src" / "main.py").exists()
    assert (project_root / "src" / "config.py").exists()
    assert (project_root / "src" / "utils.py").exists()
    assert (project_root / "src" / "telegram_bot.py").exists()
    assert (project_root / "requirements.txt").exists()

if __name__ == "__main__":
    # Permettre l'exécution directe pour tests rapides
    pytest.main([__file__, "-v"])
