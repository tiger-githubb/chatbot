#!/bin/bash
# Script de test pour Jenkins CI/CD sur Linux
echo "Running Jenkins CI tests..."

# Activer l'environnement virtuel
source venv/bin/activate

# Exécuter les tests unitaires appropriés pour Jenkins
python -m pytest tests/test_ci_minimal.py tests/test_main.py tests/test_minimal_fixed.py \
    -v --tb=short --disable-warnings --junit-xml=test-results.xml

# Vérifier le résultat
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All Jenkins CI tests passed!"
    exit 0
else
    echo ""
    echo "❌ Some tests failed. Check output above."
    exit 1
fi
