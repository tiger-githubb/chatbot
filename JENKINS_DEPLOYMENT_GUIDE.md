# 🚀 GUIDE DE DÉPLOIEMENT AWS via JENKINS

## ✅ **État Actuel**

- ✅ **Dépendances installées**
- ✅ **Tests nettoyés et optimisés**
- ✅ **Configuration AWS intégrée**
- ✅ **Scripts de webhook créés**

## 🔧 **Configuration Jenkins Nécessaire**

### **Variables d'Environnement à Configurer**

Dans Jenkins, assurez-vous d'avoir ces credentials configurés :

```
TELEGRAM_BOT_TOKEN=your_actual_bot_token
MISTRAL_API_KEY=your_actual_mistral_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

### **Fichier .env Automatique**

Le fichier `.env.aws` a été créé avec la bonne configuration AWS. Jenkins doit l'utiliser comme template.

## 🚀 **Étapes de Déploiement**

### **1. Test Local avant Jenkins**

```powershell
# Vérifier que les nouveaux tests passent
cd "c:\Users\arist\Desktop\chatbot"
make test
```

### **2. Pipeline Jenkins**

Le Jenkinsfile a été mis à jour avec ces étapes :

1. **Initialisation** ✅
2. **Injection variables** ✅  
3. **Tests minimalistes** ✅ (maintenant optimisés)
4. **Build SAM** 🔧
5. **Deploy AWS** 🚀
6. **Configuration Webhook** 📡 (nouveau)
7. **Test endpoint** 🧪

### **3. Post-Déploiement**

Après le déploiement réussi, le bot sera accessible via :
- **API Gateway** : `https://hky4t9y1fh.execute-api.eu-west-3.amazonaws.com`
- **Webhook Telegram** : configuré automatiquement
- **DynamoDB** : Table `chatbot-dbtable-aristidekarbou`

## 🧪 **Tests de Validation**

### **Test API Direct**
```bash
curl "https://hky4t9y1fh.execute-api.eu-west-3.amazonaws.com/chat?question=Hello"
```

### **Test Telegram**
1. Envoyez `/start` à votre bot
2. Envoyez un message normal
3. Vérifiez la réponse IA

## ⚠️ **Points d'Attention**

1. **DynamoDB** : La table doit être créée avec le bon nom
2. **Permissions IAM** : Lambda doit avoir accès à DynamoDB
3. **Timeout** : Vérifier que les timeouts Lambda sont suffisants (30s min)
4. **Mistral API** : Vérifier que la clé API est valide et a du crédit

## 🔍 **Debugging**

Si Jenkins échoue encore aux tests :

```powershell
# Test local des nouvelles configs
python tests/test_ci_minimal.py

# Vérifier la structure SAM
sam validate -t infrastructure/template.yaml

# Test build local
sam build --use-container -t infrastructure/template.yaml
```

## 📞 **Support**

En cas de problème, fournissez :
1. Logs complets de Jenkins
2. Étape qui échoue exactement
3. Messages d'erreur spécifiques
