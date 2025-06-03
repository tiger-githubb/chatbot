# 🤖 Telegram AI Chatbot

Un chatbot Telegram intelligent alimenté par Mistral AI, construit avec FastAPI et déployable sur AWS Lambda.

## 🎯 **Aperçu du Projet**

**Status: 🟢 Fonctionnel**  
**Fonctionnalités:**

- Webhook Telegram pour réception instantanée des messages
- Intelligence artificielle avec Mistral AI (modèle mistral-small-latest)
- Commandes `/start` et `/help` fonctionnelles
- Architecture asynchrone performante
- Déploiement sur AWS Lambda avec DynamoDB pour le stockage

## 📋 Architecture

### **Locale**

```
🌐 Telegram API → 🔗 ngrok → 🚀 FastAPI Server → 🧠 Mistral AI
```

### **AWS (Production)**

```
🌐 Telegram API → 🔒 API Gateway → λ AWS Lambda → 🧠 Mistral AI
                                        ↓
                                   🗄️ DynamoDB
```

## 🚀 **Démarrage Rapide**

### **Prérequis**

```powershell
# Python 3.12+ installé
python --version
# Installer les dépendances
pip install -r requirements.txt
pip install -e .
```

### **Configuration**

Créer un fichier `.env` avec :

```env
ENV_NAME=production
MISTRAL_API_KEY=your_mistral_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_WEBHOOK_URL=your_ngrok_url
TELEGRAM_WEBHOOK_PATH=/telegram/webhook
API_URL=http://localhost:8001
```

### **Lancement en Local**

```powershell
# 1. Démarrer l'API FastAPI
cd src
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# 2. Dans un nouveau terminal : Exposer avec ngrok
ngrok http 8001

# 3. Dans un troisième terminal : Configurer le webhook
cd tools
python set_webhook.py
```

## 🛠️ API Endpoints

- **API Chat**: `/chat?question=<question>` - Envoyer une question au bot
- **Documentation Swagger**: `/docs` - Documentation interactive
- **Webhook Telegram**: `/telegram/webhook` - Endpoint pour les mises à jour Telegram
- **Conversations**:
  - `/conversation/start` - Démarrer une nouvelle conversation
  - `/conversation/{conversation_id}/close` - Fermer une conversation

## 📱 Commandes Bot

| Commande         | Description               |
| ---------------- | ------------------------- |
| `/start`         | Démarrer une conversation |
| `/help`          | Afficher l'aide           |
| Messages normaux | Réponses Mistral AI       |

## 📁 Structure du Projet

```
chatbot/
├── infrastructure/          # Infrastructure AWS
│   └── template.yaml       # Template CloudFormation SAM
├── src/                     # Code source principal
│   ├── main.py             # API FastAPI et point d'entrée Lambda
│   ├── telegram_bot.py     # Bot Telegram (async)
│   ├── config.py           # Configuration (.env)
│   └── utils.py            # Utilitaires
├── tools/                   # Outils de configuration
│   ├── set_webhook.py      # Configuration webhook local
│   └── set_webhook_aws.py  # Configuration webhook AWS
└── tests/                   # Tests unitaires et d'intégration
```

## 🚨 **Gestion des Services**

### **Arrêt des Services**

```powershell
# Arrêter avec Ctrl+C dans les terminaux respectifs ou :
Get-Process python | Stop-Process -Force
Get-Process ngrok | Stop-Process -Force
```

### **Vérification des Services**

```powershell
# Vérifier l'API
curl http://localhost:8001/
# Vérifier ngrok
curl http://127.0.0.1:4040/api/tunnels
```

## 🚀 Déploiement AWS

### **Prérequis AWS**

```powershell
# AWS CLI
aws configure

# SAM CLI
sam --version
```

### **Déploiement**

```powershell
# Construction
make build

# Déploiement
make deploy env=dev

# Configurer le webhook Telegram vers AWS
cd tools
python set_webhook_aws.py
```

### **URL AWS Production**

L'URL de l'API déployée sur AWS est :
`https://hky4t9y1fh.execute-api.eu-west-3.amazonaws.com`

## 🔧 **Variables d'Environnement**

| Variable             | Description           | Exemple                                     |
| -------------------- | --------------------- | ------------------------------------------- |
| `MISTRAL_API_KEY`    | Clé API Mistral AI    | `mistral_api_key123`                        |
| `TELEGRAM_BOT_TOKEN` | Token du bot Telegram | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `AWS_REGION`         | Région AWS            | `eu-west-3`                                 |
| `API_URL`            | URL de l'API          | `http://localhost:8001` ou l'URL AWS        |
| `DYNAMO_TABLE`       | Table DynamoDB        | `chatbot-dbtable-dev`                       |
