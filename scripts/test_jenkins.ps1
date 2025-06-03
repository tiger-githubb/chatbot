# Script de test pour l'environnement Jenkins (PowerShell)
# Ce script vérifie que les variables d'environnement sont correctement chargées

Write-Host "🧪 Vérification des variables d'environnement Jenkins..." -ForegroundColor Cyan

# Variables critiques pour les tests
$RequiredVars = @("ENV_NAME", "AWS_REGION", "DYNAMO_TABLE", "MISTRAL_API_KEY", "TELEGRAM_BOT_TOKEN")

# Vérifier chaque variable
$missingVars = 0
foreach ($var in $RequiredVars) {
    $value = [Environment]::GetEnvironmentVariable($var)
    if ([string]::IsNullOrEmpty($value)) {
        Write-Host "❌ Variable manquante: $var" -ForegroundColor Red
        $missingVars = 1
    } else {
        Write-Host "✅ $var définie" -ForegroundColor Green
    }
}

if ($missingVars -eq 1) {
    Write-Host "⚠️  Certaines variables sont manquantes, mais on continue les tests..." -ForegroundColor Yellow
}

Write-Host "✅ Vérification des variables d'environnement terminée" -ForegroundColor Green

# Exécuter les tests unitaires
Write-Host "🧪 Exécution des tests unitaires..." -ForegroundColor Cyan

if (Test-Path "venv\Scripts\pytest.exe") {
    & venv\Scripts\pytest.exe tests\ --ignore=tools\ -v
} else {
    python -m pytest tests\ --ignore=tools\ -v
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Tous les tests sont passés" -ForegroundColor Green
    exit 0
} else {
    Write-Host "❌ Certains tests ont échoué" -ForegroundColor Red
    exit 1
}
