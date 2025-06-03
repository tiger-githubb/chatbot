"""
Configuration pytest pour les tests Jenkins CI/CD
Définit les marqueurs et configurations spécifiques aux tests
"""
import pytest


def pytest_configure(config):
    """Configuration des marqueurs personnalisés"""
    config.addinivalue_line("markers", "unit: Tests unitaires rapides pour CI/CD")
    config.addinivalue_line("markers", "integration: Tests d'intégration nécessitant des services")
    config.addinivalue_line("markers", "slow: Tests lents ou avec dépendances externes")


def pytest_collection_modifyitems(config, items):
    """Modification automatique des items de test selon les critères"""
    for item in items:
        # Marquer automatiquement les tests d'intégration
        if "api_simple" in item.nodeid or "localhost" in str(item):
            item.add_marker(pytest.mark.integration)
        
        # Marquer les tests unitaires rapides
        if any(name in item.nodeid for name in ["test_ci_minimal", "test_main", "test_minimal_fixed"]):
            item.add_marker(pytest.mark.unit)
