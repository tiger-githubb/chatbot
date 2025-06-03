#!/usr/bin/env python3
"""
Test wrapper pour tous les tests qui retournent au lieu d'utiliser assert
"""

import sys
import os
import importlib
import importlib.util
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
        # Add proper pytest fixture detection
        self._pytestfixturefunction = getattr(test_func, "_pytestfixturefunction", None)

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
            
# Make our wrapper look like a test function to pytest
def pytest_function(func):
    """Decorator to mark a function as a pytest test function."""
    func.__test__ = True
    return func

def load_and_wrap_test_functions():
    """
    Charge tous les tests problématiques et les enveloppe pour corriger les returns
    """
    test_functions = {}
    
    for module_name in PROBLEM_MODULES:
        try:
            # Pour gérer à la fois les imports directs et les sous-modules
            if '.' in module_name:
                # Pour les sous-modules (comme tools.module_name)
                parent_module_name, child_module_name = module_name.rsplit('.', 1)
                try:
                    # Essayer d'importer le module parent d'abord
                    parent_module = importlib.import_module(parent_module_name)
                    # Puis tenter d'importer le sous-module
                    module = importlib.import_module(f"{parent_module_name}.{child_module_name}")
                except ImportError as e:
                    print(f"❌ Erreur d'import pour {module_name}: {e}")
                    continue
            else:
                # Pour les modules directs
                try:
                    module = importlib.import_module(module_name)
                except ImportError as e:
                    print(f"❌ Erreur d'import pour {module_name}: {e}")
                    continue
            
            # Trouver toutes les fonctions de test dans le module
            for name, obj in inspect.getmembers(module):
                if name.startswith('test_') and inspect.isfunction(obj):
                    # Envelopper la fonction de test et l'ajouter au dictionnaire
                    wrapped_func = AssertWrapper(obj)
                    test_name = f"{module_name}.{name}"
                    test_functions[test_name] = wrapped_func
                    print(f"✅ Fonction de test enveloppée: {test_name}")
                
        except Exception as e:
            print(f"❌ Erreur lors du chargement du module {module_name}: {e}")
    
    return test_functions

# Charger et exporter les fonctions de test enveloppées
wrapped_tests = load_and_wrap_test_functions()

# Rendre les fonctions de test disponibles pour pytest
for test_name, test_func in wrapped_tests.items():
    # Créer un nom de variable conforme à Python (remplacer les points par des underscores)
    var_name = test_name.replace('.', '_')
    # Apply the pytest_function decorator to make it look like a test function
    globals()[var_name] = pytest_function(test_func)

def run_wrapped_tests():
    """
    Run all test functions in problem modules without pytest
    """
    print("==== Running tests with return-to-assert conversion ====")
    success = True
    
    for module_name in PROBLEM_MODULES:
        try:
            module_path = module_name.replace('.', '/')
            # Try to import the module directly
            if '.' in module_name:
                parent_module_name, child_module_name = module_name.rsplit('.', 1)
                try:
                    parent_module = importlib.import_module(parent_module_name)
                    module = importlib.import_module(f"{parent_module_name}.{child_module_name}")
                except ImportError as e:
                    print(f"❌ Erreur d'import pour {module_name}: {e}")
                    continue
            else:
                try:
                    module = importlib.import_module(module_name)
                except ImportError as e:
                    print(f"❌ Erreur d'import pour {module_name}: {e}")
                    continue
                
            # Find all test functions in the module
            for name, obj in inspect.getmembers(module):
                if name.startswith('test_') and inspect.isfunction(obj):
                    # Run the test with our wrapper
                    print(f"Running {module_name}.{name}...")
                    try:
                        wrapper = AssertWrapper(obj)
                        result = wrapper()
                        print(f"✅ {module_name}.{name} passed")
                    except Exception as e:
                        print(f"❌ {module_name}.{name} failed: {e}")
                        success = False
        except Exception as e:
            print(f"❌ Error processing module {module_name}: {e}")
            success = False
    
    if success:
        print("==== All tests passed ====")
        return 0
    else:
        print("==== Some tests failed ====")
        return 1

if __name__ == "__main__":
    if "--wrapped" in sys.argv:
        # Run tests directly with our wrapper
        sys.exit(run_wrapped_tests())
    else:
        # Run with pytest
        sys.exit(pytest.main(["-xvs", __file__]))
