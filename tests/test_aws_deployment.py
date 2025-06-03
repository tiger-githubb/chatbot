#!/usr/bin/env python3
"""
Test de déploiement AWS - Valide que l'API est déployée et accessible
"""

import requests
import json
import os
from urllib.parse import urljoin

def test_aws_deployment():
    """Test que l'API AWS est accessible et fonctionne"""
      # URL de base AWS - URL fournie pour le déploiement
    base_url = "https://hky4t9y1fh.execute-api.eu-west-3.amazonaws.com/"
    
    print(f"🧪 Test de déploiement AWS: {base_url}")
    
    # Test 1: Root endpoint (redirection vers /docs)
    try:
        response = requests.get(base_url, timeout=30, allow_redirects=False)
        print(f"✅ Root endpoint: Status {response.status_code}")
        
        if response.status_code in [200, 307, 308]:  # Redirection vers /docs
            print("   ✅ Redirection vers documentation OK")
        else:
            print(f"   ⚠️  Status inattendu: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur root endpoint: {e}")
        return False
    
    # Test 2: Chat endpoint
    try:
        chat_url = urljoin(base_url, "chat")
        params = {"question": "Hello AWS deployment test"}
        
        response = requests.get(chat_url, params=params, timeout=60)
        print(f"✅ Chat endpoint: Status {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "answer" in data:
                answer = data.get("answer", {}).get("S", "")[:50]
                print(f"   ✅ Réponse reçue: {answer}...")
            else:
                print("   ⚠️  Format de réponse inattendu")
        else:
            print(f"   ❌ Erreur chat: {response.status_code}")
            print(f"   Réponse: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Erreur chat endpoint: {e}")
        return False
    
    # Test 3: Documentation endpoint
    try:
        docs_url = urljoin(base_url, "docs")
        response = requests.get(docs_url, timeout=30)
        print(f"✅ Docs endpoint: Status {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Documentation accessible")
        else:
            print(f"   ⚠️  Documentation non accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur docs endpoint: {e}")
    
    print("🎉 Test de déploiement AWS terminé")
    return True

def test_webhook_endpoint():
    """Test que l'endpoint webhook est accessible (sans envoyer de données)"""
    
    base_url = "https://hky4t9y1fh.execute-api.eu-west-3.amazonaws.com/"
    webhook_url = urljoin(base_url, "telegram/webhook")
    
    try:
        # Test HEAD pour vérifier que l'endpoint existe sans envoyer de données
        response = requests.head(webhook_url, timeout=30)
        print(f"✅ Webhook endpoint accessible: Status {response.status_code}")
        
        # 405 Method Not Allowed est acceptable (POST attendu)
        if response.status_code in [200, 405]:
            print("   ✅ Endpoint webhook configuré")
            return True
        else:
            print(f"   ⚠️  Status inattendu: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur webhook endpoint: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Test de déploiement AWS Lambda")
    print("=" * 50)
    
    success = True
    
    if not test_aws_deployment():
        success = False
    
    if not test_webhook_endpoint():
        success = False
    
    if success:
        print("\n🎉 Tous les tests de déploiement sont passés!")
        exit(0)
    else:
        print("\n❌ Certains tests de déploiement ont échoué!")
        exit(1)
