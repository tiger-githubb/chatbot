# 🤖 Telegram AI Chatbot

Un chatbot Telegram intelligent alimenté par Mistral AI, construit avec FastAPI et déployable sur AWS Lambda.

## 🎯 MVP Fonctionnel

**✅ Le chatbot est opérationnel !** Il peut :

- 💬 Recevoir des messages sur Telegram
- 🧠 Générer des réponses intelligentes avec Mistral AI
- 🔄 Maintenir des conversations contextuelles
- 🚀 Fonctionner en mode local (polling) ou webhook

## 📋 Fonctionnalités

### 🤖 Intelligence Artificielle

- **Mistral AI** : Génération de réponses naturelles et contextuelles
- **Gestion des conversations** : Historique et contexte préservés
- **Commandes Telegram** : `/start`, `/help`, `/close`

### 🔧 Architecture Technique

- **FastAPI** : API REST moderne et performante
- **Telegram Bot API** : Intégration native avec Telegram
- **DynamoDB** : Stockage des conversations (optionnel)
- **AWS Lambda** : Déploiement serverless (optionnel)

### 📊 Modes de Fonctionnement

- **Mode Local** : Polling pour développement et tests
- **Mode Webhook** : Production avec ngrok ou serveur public
- **Mode AWS** : Déploiement serverless complet

## 🚀 Démarrage Rapide

### 1. Prérequis

```bash
# Python 3.12+
python --version

# Dépendances système
pip install --upgrade pip
```

### 2. Installation

```bash
# Cloner le projet
git clone <repository-url>
cd chatbot

# Installer les dépendances
pip install -r requirements.txt

# Installer en mode développement
pip install -e .
```

### 3. Configuration

Créez un fichier `.env` à partir de `.env.example` :

```bash
# Copier le template
cp .env.example .env
```

Configurez vos clés API dans `.env` :

```env
# Configuration essentielle pour le MVP
ENV_NAME=local
MISTRAL_API_KEY=your_mistral_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Configuration AWS (optionnelle pour le mode local)
AWS_REGION=eu-west-3
DYNAMO_TABLE=chatbot-dbtable-yourname
AWS_PROFILE=your_aws_profile

# Configuration webhook (optionnelle)
TELEGRAM_WEBHOOK_URL=https://your-domain.com
TELEGRAM_WEBHOOK_PATH=/telegram/webhook
API_URL=http://localhost:8001
```

### 4. Test du MVP

```bash
# Vérifier que tout fonctionne
python test_mvp.py

# Démarrer l'API
cd src
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Dans un autre terminal : Tester le bot
python test_bot_local.py
```

## 🛠️ Utilisation

### Mode Développement Local

1. **Démarrer l'API** (Terminal 1) :

```bash
cd src
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

2. **Tester le bot** (Terminal 2) :

```bash
python test_bot_local.py
```

3. **Ouvrir Telegram** et parler avec votre bot !

### Mode Production (Webhook)

```bash
# Installer ngrok pour exposer l'API localement
# Télécharger depuis : https://ngrok.com/download

# Exposer l'API
ngrok http 8001

# Configurer le webhook Telegram avec l'URL ngrok
# Le webhook sera automatiquement configuré
```

## 📚 API Endpoints

### Chat Principal

- `GET /chat?question=<question>` - Envoyer une question au bot
- `GET /` - Documentation interactive (Swagger UI)

### Gestion des Conversations

- `POST /conversation/start` - Démarrer une nouvelle conversation
- `GET /conversation/active/{telegram_id}` - Conversation active d'un utilisateur
- `GET /conversation/history/{telegram_id}` - Historique des conversations
- `POST /conversation/message` - Sauvegarder un message
- `POST /conversation/{conversation_id}/close` - Fermer une conversation

### Webhook Telegram

- `POST /telegram/webhook` - Endpoint pour les mises à jour Telegram

## 🧪 Tests

```bash
# Test complet du MVP
python test_mvp.py

# Test du bot en mode polling
python test_bot_local.py

# Test API simple
python test_api_simple.py

# Tests unitaires
python -m pytest tests/
```

## 📁 Structure du Projet

```
chatbot/
├── 📄 README.md              # Documentation principale
├── 📄 .env.example           # Template de configuration
├── 📄 requirements.txt       # Dépendances Python
├── 📄 setup.py              # Configuration du package
├── 📁 src/                   # Code source principal
│   ├── 🐍 main.py           # API FastAPI
│   ├── 🐍 telegram_bot.py   # Bot Telegram
│   ├── 🐍 config.py         # Configuration
│   └── 🐍 utils.py          # Utilitaires
├── 📁 tests/                 # Tests unitaires
├── 📁 infrastructure/        # Templates AWS SAM
├── 📄 test_mvp.py           # Test d'intégration MVP
├── 📄 test_bot_local.py     # Test bot en polling
└── 📄 Makefile              # Automatisation
```

## 🚀 Déploiement AWS (Optionnel)

### Prérequis AWS

```bash
# AWS CLI
aws configure

# SAM CLI
sam --version
```

### Commandes de Déploiement

```bash
# Construction
make build

# Déploiement
make deploy env=dev

# Test de l'endpoint déployé
make test-endpoint env=dev
```

## 🔧 Configuration Avancée

### Variables d'Environnement

| Variable             | Description           | Requis | Défaut                  |
| -------------------- | --------------------- | ------ | ----------------------- |
| `MISTRAL_API_KEY`    | Clé API Mistral AI    | ✅     | -                       |
| `TELEGRAM_BOT_TOKEN` | Token du bot Telegram | ✅     | -                       |
| `API_URL`            | URL de l'API locale   | ❌     | `http://localhost:8001` |
| `AWS_REGION`         | Région AWS            | ❌     | `eu-west-3`             |
| `DYNAMO_TABLE`       | Table DynamoDB        | ❌     | -                       |

### Commandes Telegram Disponibles

| Commande | Description                        |
| -------- | ---------------------------------- |
| `/start` | Démarrer une nouvelle conversation |
| `/help`  | Afficher l'aide                    |
| `/close` | Fermer la conversation active      |

## 🐛 Dépannage

### Problèmes Courants

1. **Erreurs d'import** :

```bash
# Réinstaller en mode développement
pip install -e .
```

2. **Bot ne répond pas** :

```bash
# Vérifier que l'API tourne sur le bon port
curl http://localhost:8001/
```

3. **Erreur Mistral AI** :

```bash
# Vérifier la clé API
python -c "from config import settings; print(settings.MISTRAL_API_KEY[:10] + '...')"
```

### Logs de Debug

```bash
# Voir les logs de l'API
cd src
python -m uvicorn main:app --log-level debug

# Voir les logs du bot
python test_bot_local.py
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est créé à des fins éducatives.

## 🏆 État du Projet

- ✅ **MVP Fonctionnel** - Bot répond intelligemment
- ✅ **Intégration Mistral AI** - Réponses contextuelles
- ✅ **Commandes Telegram** - Interface utilisateur complète
- ✅ **Mode Local** - Développement et tests
- 🔄 **Mode Webhook** - En cours (nécessite ngrok)
- 🔄 **Déploiement AWS** - Prêt (nécessite credentials)

---

**🎉 Le chatbot est prêt à utiliser ! Démarrez avec `python test_mvp.py` puis `python test_bot_local.py`**
