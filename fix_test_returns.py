#!/usr/bin/env python3
"""
Runner pour les tests problématiques identifiés par pylint
"""

import os
import sys
import importlib.util
import subprocess
from pathlib import Path

def run_test_with_assert_replacement(test_file, test_name):
    """
    Charge un module de test et remplace les returns par des asserts
    """
    print(f"\n✅ Testing module: {test_file}")
    
    # Extraire le chemin complet
    test_file_path = Path(test_file)
    if not test_file_path.exists():
        print(f"❌ Fichier non trouvé: {test_file_path}")
        return False
    
    # Lire le contenu du fichier
    with open(test_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Créer un fichier temporaire avec les corrections
    temp_file = test_file_path.with_name(f"temp_{test_file_path.name}")
    
    modified_content = content.replace("return True", "assert True")
    modified_content = modified_content.replace("return False", "assert False")
    
    with open(temp_file, 'w', encoding='utf-8') as file:
        file.write(modified_content)
    
    print(f"✓ Fichier temporaire créé: {temp_file}")
    
    try:
        # Exécuter le fichier avec python
        result = subprocess.run(
            [sys.executable, str(temp_file)],
            capture_output=True,
            text=True
        )
        
        # Afficher la sortie
        print("\n=== SORTIE ===")
        print(result.stdout)
        
        if result.stderr:
            print("\n=== ERREURS ===")
            print(result.stderr)
        
        # Supprimer le fichier temporaire
        os.remove(temp_file)
        print(f"✓ Fichier temporaire supprimé: {temp_file}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        # Supprimer le fichier temporaire en cas d'erreur
        if temp_file.exists():
            os.remove(temp_file)
        return False

def main():
    """
    Fonction principale qui exécute les tests problématiques
    """
    print("🧪 Runner de tests problématiques")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    
    # Liste des tests problématiques
    problem_tests = [
        (project_root / "test_system.py", "test_api_health"),
        (project_root / "tools/test_complete_integration.py", "test_api_integration"),
        (project_root / "tools/test_dynamodb_connection.py", "test_aws_credentials"),
        (project_root / "tools/test_telegram_integration.py", "test_integration"),
    ]
    
    # Exécuter chaque test
    for test_file, test_name in problem_tests:
        success = run_test_with_assert_replacement(test_file, test_name)
        if success:
            print(f"✅ Test réussi: {test_name}")
        else:
            print(f"❌ Test échoué: {test_name}")
    
    print("=" * 50)
    print("Tests terminés")

if __name__ == "__main__":
    main()
