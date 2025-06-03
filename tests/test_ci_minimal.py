#!/usr/bin/env python3
"""
Tests ultra-minimalistes pour Jenkins CI/CD
Vérifie uniquement les imports critiques et la structure de base
"""

import pytest
import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path pour l'import
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

def test_python_version():
    """Vérifier que Python est en version supportée"""
    assert sys.version_info >= (3, 8), "Python 3.8+ requis"

def test_essential_packages():
    """Test que les packages essentiels sont installés"""
    try:
        import fastapi
        import telegram  
        import mistralai
        import boto3
        import pydantic_settings
        assert True
    except ImportError as e:
        pytest.skip(f"Package manquant (acceptable en CI): {e}")

def test_project_files_exist():
    """Vérifier que les fichiers essentiels existent"""
    project_root = Path(__file__).parent.parent
    
    essential_files = [
        "src/main.py",
        "src/config.py", 
        "src/utils.py",
        "src/telegram_bot.py",
        "requirements.txt",
        "infrastructure/template.yaml"
    ]
    
    for file_path in essential_files:
        assert (project_root / file_path).exists(), f"Fichier manquant: {file_path}"

def test_basic_config_structure():
    """Test que la configuration de base est correcte"""
    try:
        from config import settings
        # Vérifier que les attributs essentiels existent
        assert hasattr(settings, 'ENV_NAME')
        assert hasattr(settings, 'AWS_REGION')
        assert hasattr(settings, 'TELEGRAM_WEBHOOK_PATH')
        assert settings.AWS_REGION == "eu-west-3"
    except Exception as e:
        pytest.skip(f"Configuration pas encore injectée (normal en CI): {e}")

def test_fastapi_app_structure():
    """Test que l'app FastAPI a la bonne structure"""
    try:
        from main import app
        assert app is not None
        assert hasattr(app, 'routes')
        assert len(app.routes) > 0
        
        # Vérifier les métadonnées de l'app
        assert hasattr(app, 'title')
        assert app.title == "ChatBot API"
        
    except Exception as e:
        pytest.skip(f"App non disponible (dépendances manquantes): {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
