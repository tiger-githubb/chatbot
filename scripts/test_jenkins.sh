#!/bin/bash
# Script de test pour l'environnement Jenkins
# Ce script verifie que les variables d'environnement sont correctement chargees

echo "=== Verification des variables d'environnement Jenkins ==="

# Variables critiques pour les tests
REQUIRED_VARS=("ENV_NAME" "AWS_REGION" "DYNAMO_TABLE" "MISTRAL_API_KEY" "TELEGRAM_BOT_TOKEN")

# Verifier chaque variable
missing_vars=0
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo "ERREUR: Variable manquante: $var"
        missing_vars=1
    else
        echo "OK: $var definie"
    fi
done

if [ $missing_vars -eq 1 ]; then
    echo "ATTENTION: Certaines variables sont manquantes, mais on continue les tests..."
fi

echo "=== Verification des variables d'environnement terminee ==="

# Executer les tests unitaires
echo "=== Execution des tests unitaires ==="
# S'assurer que PYTHONPATH inclut le répertoire racine pour les imports src.*
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}./"
venv/bin/pytest tests/ --ignore=tools/ -v

if [ $? -eq 0 ]; then
    echo "=== Tous les tests sont passes ==="
    exit 0
else
    echo "=== Certains tests ont echoue ==="
    exit 1
fi
