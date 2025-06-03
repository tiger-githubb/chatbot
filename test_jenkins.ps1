# Script de test pour Jenkins CI/CD sur Windows (PowerShell)
Write-Host "Running Jenkins CI tests..." -ForegroundColor Green

try {
    # Vérifier que l'environnement virtuel existe
    if (-not (Test-Path "venv\Scripts\activate.bat")) {
        Write-Host "❌ Virtual environment not found. Please run 'make install' first." -ForegroundColor Red
        exit 1
    }

    # Activer l'environnement virtuel et exécuter les tests
    & "venv\Scripts\python.exe" -m pytest `
        tests\test_ci_minimal.py `
        tests\test_main.py `
        tests\test_minimal_fixed.py `
        -v --tb=short --disable-warnings --junit-xml=test-results.xml

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ All Jenkins CI tests passed!" -ForegroundColor Green
        exit 0
    } else {
        Write-Host ""
        Write-Host "❌ Some tests failed. Check output above." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Error running tests: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
