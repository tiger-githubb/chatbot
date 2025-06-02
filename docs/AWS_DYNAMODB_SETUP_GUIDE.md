# 🚀 Guide AWS et DynamoDB Configuration

## 📋 **Prérequis**

✅ Vous avez accès à la console AWS : `https://eu-north-1.console.aws.amazon.com/console/home`  
✅ Votre chatbot Telegram fonctionne  
✅ Python et les dépendances sont installés

---

## 🔧 **Étape 1 : Installation d'AWS CLI**

### **Option A : Téléchargement Direct (Recommandé)**

1. **Télécharger AWS CLI** :

   - Allez sur : https://aws.amazon.com/cli/
   - Cliquez sur "Download for Windows"
   - Téléchargez le fichier MSI (64-bit)

2. **Installer** :
   - Exécutez le fichier `.msi` téléchargé
   - Suivez l'assistant d'installation
   - Redémarrez votre terminal PowerShell

### **Option B : PowerShell (Alternative)**

```powershell
# Télécharger AWS CLI
Invoke-WebRequest -Uri "https://awscli.amazonaws.com/AWSCLIV2.msi" -OutFile "AWSCLIV2.msi"

# Installer silencieusement
Start-Process msiexec.exe -Wait -ArgumentList '/I AWSCLIV2.msi /quiet'

# Redémarrer le terminal
```

### **Vérification de l'Installation**

```powershell
aws --version
# Sortie attendue : aws-cli/2.x.x Python/3.x.x Windows/...
```

---

## 🔑 **Étape 2 : Création des Credentials AWS**

### **Dans la Console AWS :**

1. **Accéder à IAM** :

   - Allez sur : https://console.aws.amazon.com/iam/
   - Ou cherchez "IAM" dans la barre de recherche AWS

2. **Créer un Utilisateur** :

   ```
   IAM → Users → Create User
   - User name: chatbot-user
   - Access type: Programmatic access
   - Next
   ```

3. **Attacher des Permissions** :

   ```
   Attach policies directly:
   ✅ AmazonDynamoDBFullAccess
   ✅ IAMReadOnlyAccess (optionnel)
   - Next → Create User
   ```

4. **Récupérer les Clés** :
   - **⚠️ IMPORTANT** : Notez immédiatement :
     - `Access Key ID` : AKIA...
     - `Secret Access Key` : (affiché une seule fois)

---

## 🛠️ **Étape 3 : Configuration AWS CLI**

### **Méthode A : Configuration Interactive**

```powershell
aws configure
```

Saisissez :

```
AWS Access Key ID [None]: VOTRE_ACCESS_KEY_ID
AWS Secret Access Key [None]: VOTRE_SECRET_ACCESS_KEY
Default region name [None]: eu-north-1
Default output format [None]: json
```

### **Méthode B : Script Automatisé**

```powershell
# Depuis le répertoire chatbot
cd tools
python setup_aws.py
```

---

## 🗄️ **Étape 4 : Création de la Table DynamoDB**

### **Option A : Via la Console AWS**

1. **Accéder à DynamoDB** :

   - Console AWS → DynamoDB
   - Ou : https://eu-north-1.console.aws.amazon.com/dynamodbv2/

2. **Créer une Table** :
   ```
   Create Table:
   - Table name: chatbot-dbtable-aristidekarbou
   - Partition key: conversation_id (String)
   - Sort key: timestamp (Number)
   - Settings: Use default settings
   - Create Table
   ```

### **Option B : Script Automatisé**

```powershell
# Utiliser notre script complet
cd tools
python setup_aws.py
```

### **Option C : AWS CLI**

```powershell
aws dynamodb create-table \
  --table-name chatbot-dbtable-aristidekarbou \
  --attribute-definitions \
    AttributeName=conversation_id,AttributeType=S \
    AttributeName=timestamp,AttributeType=N \
  --key-schema \
    AttributeName=conversation_id,KeyType=HASH \
    AttributeName=timestamp,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --region eu-north-1
```

---

## ✅ **Étape 5 : Vérification et Tests**

### **1. Vérifier AWS CLI**

```powershell
aws sts get-caller-identity
```

Sortie attendue :

```json
{
  "UserId": "AIDACKCEVSQ6C2EXAMPLE",
  "Account": "123456789012",
  "Arn": "arn:aws:iam::123456789012:user/chatbot-user"
}
```

### **2. Vérifier DynamoDB**

```powershell
aws dynamodb list-tables --region eu-north-1
```

Sortie attendue :

```json
{
  "TableNames": ["chatbot-dbtable-aristidekarbou"]
}
```

### **3. Test Complet avec le Script**

```powershell
cd tools
python setup_aws.py
```

---

## 📝 **Étape 6 : Mise à Jour de la Configuration**

### **Vérifier le fichier .env**

Le script met à jour automatiquement `.env` :

```env
# Configuration AWS mise à jour
ENV_NAME=aristidekarbou
AWS_REGION=eu-north-1
DYNAMO_TABLE=chatbot-dbtable-aristidekarbou
AWS_PROFILE=default

# Configuration existante
MISTRAL_API_KEY=lK8CMtpJG01K3ALyPQCY80CH1FmyeGjs
TELEGRAM_BOT_TOKEN=7553984013:AAHCmlyVzVGdo3eEFTw03VK7SDQwhRScbE0
TELEGRAM_WEBHOOK_URL=https://1839-102-64-172-180.ngrok-free.app
TELEGRAM_WEBHOOK_PATH=/telegram/webhook
API_URL=http://localhost:8001
```

---

## 🧪 **Étape 7 : Test d'Intégration**

### **Test DynamoDB dans le Chatbot**

```powershell
# Test API avec DynamoDB
curl "http://localhost:8001/chat?question=Hello%20world"

# Vérifier que les données sont sauvegardées
aws dynamodb scan --table-name chatbot-dbtable-aristidekarbou --region eu-north-1
```

---

## 🎯 **Résultat Final**

Après cette configuration, votre chatbot aura :

✅ **AWS CLI** configuré  
✅ **Credentials AWS** sécurisés  
✅ **Table DynamoDB** opérationnelle  
✅ **Sauvegarde des conversations** activée  
✅ **Intégration complète** AWS + Telegram + Mistral AI

---

## 🚨 **Dépannage**

### **Erreur de Credentials**

```powershell
aws configure list
aws sts get-caller-identity
```

### **Erreur DynamoDB**

```powershell
aws dynamodb describe-table --table-name chatbot-dbtable-aristidekarbou --region eu-north-1
```

### **Problème de Région**

```
Vérifiez que la région est cohérente :
- .env : AWS_REGION=eu-north-1
- AWS CLI : Default region eu-north-1
- Console AWS : eu-north-1
```

---

## 💰 **Coûts AWS**

- **DynamoDB** : Mode PAY_PER_REQUEST (quelques centimes pour des milliers de messages)
- **IAM** : Gratuit
- **API Calls** : Inclus dans le free tier

**Estimation** : < 1€/mois pour un usage normal du chatbot

---

🎉 **Configuration terminée ! Votre chatbot peut maintenant persister les conversations en DynamoDB.**

## 🎯 **CHOIX DES CREDENTIALS AWS - RECOMMANDATION**

### **Pour votre cas d'usage : "Local code" ✅**

**Pourquoi cette option ?**

- 🏠 **Développement local** : Votre bot tourne sur localhost Windows
- 🔧 **Code local** : Accès DynamoDB depuis votre application Python
- 🚀 **Simplicité** : Configuration directe avec access keys
- ⚡ **Rapidité** : Mise en place immédiate

### **Étapes à suivre :**

1. **Créer un utilisateur IAM** avec permissions DynamoDB
2. **Générer Access Key + Secret Key** pour cet utilisateur
3. **Configurer AWS CLI** avec ces credentials
4. **Tester la connexion** DynamoDB

### **⚠️ Sécurité - Bonnes Pratiques :**

- ✅ **Permissions minimales** : Seulement DynamoDB read/write
- ✅ **Rotation régulière** : Changer les clés tous les 90 jours
- ✅ **Environnement .env** : Ne jamais committer les clés
- ✅ **Migration future** : Passer aux rôles IAM lors du déploiement AWS

---
