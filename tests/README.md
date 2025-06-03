# Tests de Base

Ce répertoire contient un test minimal pour vérifier que le projet fonctionne correctement avec Jenkins CI/CD.

## Fichier de test

- `test_basic.py` : Test basique qui vérifie la structure du projet, les imports et la configuration

## Exécution des tests

### Méthode 1 : Script Python direct

```bash
python tests/test_basic.py
```

### Méthode 2 : Avec Make

```bash
make test
```

### Méthode 3 : Avec pytest

```bash
make test-pytest
```

ou

```bash
python -m pytest tests/test_basic.py -v
```

## Ce que le test vérifie

1. **Version Python** : Vérifie que Python 3.8+ est utilisé
2. **Structure du projet** : Vérifie la présence des fichiers essentiels
3. **Imports de base** : Teste que FastAPI et les modules du projet s'importent correctement
4. **Configuration** : Vérifie que la configuration se charge sans erreur

## Pour Jenkins

Le test est conçu pour être minimaliste et fonctionner en environnement CI sans dépendances externes complexes. Il utilise uniquement les imports Python standard et les modules du projet.

## Sortie attendue

Le test affiche des messages détaillés avec des emoji pour indiquer le statut :

- ✅ pour les tests réussis
- ❌ pour les tests échoués
- 🚀 pour le début de l'exécution
- 📊 pour le résumé final
