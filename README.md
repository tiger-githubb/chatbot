# 🐅 Tiger ChatBot

Un chatbot intelligent basé sur Telegram utilisant l'IA Mistral, déployé sur AWS avec FastAPI.

## 📋 Description

Tiger est un assistant conversationnel développé en Python qui combine :

- **Interface Telegram** : Bot accessible via Telegram avec commandes interactives
- **IA Mistral** : Intégration de l'API Mistral pour des réponses intelligentes
- **Architecture AWS** : Déploiement serverless avec Lambda et DynamoDB
- **API REST** : Interface FastAPI avec limitation de taux et CORS

## 🚀 Fonctionnalités

### Bot Telegram

- `/start` - Accueil et présentation
- `/help` - Aide et liste des commandes
- `/stats` - Statistiques d'utilisation
- `/clear` - Réinitialisation de l'historique
- Chat conversationnel avec historique persistant

### API Features

- Rate limiting pour éviter les abus
- Gestion CORS pour intégration web
- Monitoring et logging
- Architecture serverless AWS

## 🛠️ Technologies

- **Python 3.12** - Langage principal
- **FastAPI** - Framework web moderne
- **python-telegram-bot** - SDK Telegram
- **Mistral AI** - Modèle d'intelligence artificielle
- **AWS Lambda** - Compute serverless
- **DynamoDB** - Base de données NoSQL
- **SAM** - Infrastructure as Code

## 📦 Installation

### Prérequis

- Python 3.12+
- AWS CLI configuré
- SAM CLI installé
- Compte Telegram Bot (via BotFather)
- Clé API Mistral

### Configuration locale

1. **Cloner le projet**

```bash
git clone <repository-url>
cd chatbot
```

2. **Créer l'environnement virtuel**

```bash
make venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Installer les dépendances**

```bash
make install
```

4. **Configuration des variables d'environnement**
   Créer un fichier `.env` :

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
MISTRAL_API_KEY=your_mistral_api_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
DYNAMO_TABLE=chatbot-table
TELEGRAM_WEBHOOK_URL=your_webhook_url
```

## 🚦 Démarrage

### Développement local

```bash
# Démarrer l'API localement
make deploy-local

# Ou directement avec uvicorn
uvicorn src.main:app --reload
```

### Tests

```bash
# Exécuter tous les tests
make test

# Tests avec couverture
pytest --cov=src tests/
```

### Déploiement AWS

```bash
# Build du projet
make build

# Déploiement
make deploy env=aristidekarbou
```

## 📁 Structure du Projet

```
chatbot/
├── src/                    # Code source principal
│   ├── main.py            # Point d'entrée FastAPI
│   ├── telegram_bot.py    # Logique du bot Telegram
│   ├── config.py          # Configuration et variables d'environnement
│   └── utils.py           # Utilitaires et helpers
├── tests/                 # Tests unitaires et d'intégration
├── infrastructure/        # Templates AWS SAM
├── tools/                 # Scripts d'initialisation
├── requirements.txt       # Dépendances Python
├── Makefile              # Commandes de build et déploiement
└── Jenkinsfile           # Pipeline CI/CD
```

## 🔧 Configuration

### Variables d'environnement requises

- `TELEGRAM_BOT_TOKEN` : Token du bot Telegram
- `MISTRAL_API_KEY` : Clé API Mistral AI
- `AWS_ACCESS_KEY_ID` : Clé d'accès AWS
- `AWS_SECRET_ACCESS_KEY` : Clé secrète AWS
- `DYNAMO_TABLE` : Nom de la table DynamoDB

### Architecture AWS

- **Lambda Function** : Exécution du code Python
- **API Gateway** : Exposition des endpoints REST
- **DynamoDB** : Stockage des conversations
- **CloudFormation** : Provisioning infrastructure

## 🧪 Tests

Le projet inclut une suite de tests complète :

- Tests unitaires des composants
- Tests d'intégration API
- Tests du bot Telegram
- Mock des services AWS avec `moto`

```bash
# Exécution des tests
pytest tests/

# Tests avec rapport de couverture
pytest --cov=src --cov-report=html tests/
```

## 📊 Qualité de Code

- **MyPy** : Vérification des types
- **Black** : Formatage automatique
- **Flake8** : Linting
- **Bandit** : Analyse de sécurité

```bash
# Vérifications qualité
mypy src/
black src/ tests/
flake8 src/ tests/
bandit -r src/
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👤 Auteur

**Aristide Karbou**

- GitHub: [@aristidekarbou](https://github.com/tiger-githubb)

## 🔗 Ressources

- [Documentation Telegram Bot API](https://core.telegram.org/bots/api)
- [Mistral AI Documentation](https://docs.mistral.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [AWS SAM Documentation](https://docs.aws.amazon.com/sam/)
