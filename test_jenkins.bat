@echo off
REM Script de test pour Jenkins CI/CD sur Windows
echo Running Jenkins CI tests...

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Exécuter les tests unitaires appropriés pour Jenkins
python -m pytest tests\test_ci_minimal.py tests\test_main.py tests\test_minimal_fixed.py -v --tb=short --disable-warnings --junit-xml=test-results.xml

REM Afficher le résultat
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ All Jenkins CI tests passed!
    exit /b 0
) else (
    echo.
    echo ❌ Some tests failed. Check output above.
    exit /b 1
)
