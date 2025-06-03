#!/usr/bin/env python3
"""
Test wrapper pour tous les tests qui retournent au lieu d'utiliser assert
"""

import sys
import os
import importlib
import inspect
import types
import pytest
from pathlib import Path

# Ajouter tous les chemins nécessaires
sys.path.append(str(Path(__file__).parent / "src"))
sys.path.append(str(Path(__file__).parent / "tools"))

# Liste des modules de test problématiques
PROBLEM_MODULES = [
    'test_system',
    'tools.test_complete_integration',
    'tools.test_dynamodb_connection',
    'tools.test_telegram_integration'
]

class AssertWrapper:
    """
    Classe qui enveloppe les fonctions de test pour transformer les returns en asserts
    """
    def __init__(self, test_func):
        self.test_func = test_func
        self.__name__ = test_func.__name__
        self.__doc__ = test_func.__doc__
        self.__module__ = test_func.__module__

    def __call__(self, *args, **kwargs):
        try:
            result = self.test_func(*args, **kwargs)
            # Si la fonction renvoie True ou False au lieu d'utiliser assert
            if isinstance(result, bool):
                assert result, f"Test {self.test_func.__name__} a retourné False"
            return None  # Pour éviter que pytest ne considère la valeur de retour
        except AssertionError:
            raise  # Re-raise les assertions
        except Exception as e:
            pytest.fail(f"Exception dans {self.test_func.__name__}: {e}")

def load_and_wrap_test_functions():
    """
    Charge tous les tests problématiques et les enveloppe pour corriger les returns
    """
    test_functions = {}
    
    for module_name in PROBLEM_MODULES:
        try:
            # Remplacer les points par des slashes pour les sous-modules
            module_path = module_name.replace('.', '/')
            
            # Charger le module
            spec = importlib.util.find_spec(module_name)
            if spec:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Trouver toutes les fonctions de test dans le module
                for name, obj in inspect.getmembers(module):
                    if name.startswith('test_') and inspect.isfunction(obj):
                        # Envelopper la fonction de test et l'ajouter au dictionnaire
                        wrapped_func = AssertWrapper(obj)
                        test_name = f"{module_name}.{name}"
                        test_functions[test_name] = wrapped_func
                        print(f"✅ Fonction de test enveloppée: {test_name}")
            else:
                print(f"❌ Module non trouvé: {module_name}")
                
        except Exception as e:
            print(f"❌ Erreur lors du chargement du module {module_name}: {e}")
    
    return test_functions

# Charger et exporter les fonctions de test enveloppées
wrapped_tests = load_and_wrap_test_functions()
globals().update(wrapped_tests)

# Rendre les fonctions de test disponibles pour pytest
for test_name, test_func in wrapped_tests.items():
    # Créer un nom de variable conforme à Python (remplacer les points par des underscores)
    var_name = test_name.replace('.', '_')
    globals()[var_name] = test_func

if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
