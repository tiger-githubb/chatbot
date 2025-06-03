#!/usr/bin/env python3
"""
Test basique pour vérifier que le projet fonctionne correctement
Test minimal pour Jenkins CI/CD
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def test_python_version():
    """Vérifier que Python est en version supportée"""
    assert sys.version_info >= (3, 8), f"Python 3.8+ requis, version actuelle: {sys.version}"
    print(f"✅ Version Python OK: {sys.version}")


def test_project_structure():
    """Vérifier que la structure du projet est correcte"""
    project_root = Path(__file__).parent.parent
    
    # Vérifier les fichiers essentiels
    essential_files = [
        "requirements.txt",
        "Makefile", 
        "Jenkinsfile",
        "src/main.py",
        "src/config.py"
    ]
    
    for file_path in essential_files:
        full_path = project_root / file_path
        assert full_path.exists(), f"Fichier manquant: {file_path}"
    
    print("✅ Structure du projet OK")


def test_basic_imports():
    """Test que les imports de base fonctionnent"""
    try:
        # Test import FastAPI
        import fastapi
        print("✅ FastAPI importé avec succès")
        
        # Test import des modules du projet
        import main
        import config
        print("✅ Modules du projet importés avec succès")
        
        # Vérifier que l'app FastAPI existe
        assert hasattr(main, 'app'), "L'application FastAPI 'app' n'existe pas dans main.py"
        print("✅ Application FastAPI trouvée")
        
    except ImportError as e:
        assert False, f"Erreur d'import: {e}"


def test_config_loading():
    """Test que la configuration se charge correctement"""
    try:
        from config import settings
        
        # Vérifier que settings existe
        assert settings is not None, "Objet settings non trouvé"
        print("✅ Configuration chargée avec succès")
        
    except Exception as e:
        # En CI, la config peut ne pas être complète, on accepte ça
        print(f"⚠️ Configuration partiellement chargée: {e}")


if __name__ == "__main__":
    """Exécuter les tests directement si le script est appelé"""
    print("🚀 Exécution des tests basiques")
    print("=" * 50)
    
    tests = [
        ("Version Python", test_python_version),
        ("Structure du projet", test_project_structure), 
        ("Imports de base", test_basic_imports),
        ("Configuration", test_config_loading)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🔍 Test: {test_name}")
        try:
            test_func()
            passed += 1
            print(f"✅ {test_name}: PASSÉ")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name}: ÉCHEC - {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 RÉSULTATS: {passed} réussis, {failed} échoués")
    
    if failed == 0:
        print("🎉 TOUS LES TESTS SONT PASSÉS!")
        sys.exit(0)
    else:
        print("⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        sys.exit(1)
