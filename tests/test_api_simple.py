#!/usr/bin/env python3
"""
Test simple de l'API sans Telegram
"""

import requests
import json
import pytest
import os

@pytest.mark.skipif(os.environ.get('CI') == 'true',
                   reason="Test ignoré dans l'environnement CI - nécessite API locale")
def test_chat_api():
    """Test l'endpoint /chat directement"""
    print("🧪 Test de l'API /chat...")
    
    # Test 1: Question simple
    response = requests.get("http://localhost:8001/chat", params={"question": "Bonjour, qui êtes-vous ?"})
    
    if response.status_code == 200:
        data = response.json()
        answer = data.get("answer", {}).get("S", "Pas de réponse")
        print(f"✅ Question: 'Bonjour, qui êtes-vous ?'")
        print(f"✅ Réponse: {answer}")
        print()
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(f"❌ Détails: {response.text}")
        return False
    
    # Test 2: Question technique
    response = requests.get("http://localhost:8001/chat", params={"question": "Expliquez-moi ce qu'est Python en 2 phrases"})
    
    if response.status_code == 200:
        data = response.json()
        answer = data.get("answer", {}).get("S", "Pas de réponse")
        print(f"✅ Question: 'Expliquez-moi ce qu'est Python en 2 phrases'")
        print(f"✅ Réponse: {answer}")
        print()
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(f"❌ Détails: {response.text}")
        return False
    
    return True

@pytest.mark.skipif(os.environ.get('CI') == 'true',
                   reason="Test ignoré dans l'environnement CI - nécessite API locale")
def test_conversation_endpoints():
    """Test les endpoints de conversation"""
    print("🧪 Test des endpoints de conversation...")
    
    # Test démarrage conversation
    response = requests.post("http://localhost:8001/conversation/start", 
                           json={"telegram_id": "test_user_123"})
    
    if response.status_code == 200:
        data = response.json()
        conversation_id = data.get("conversation_id")
        print(f"✅ Conversation créée: {conversation_id}")
        
        # Test sauvegarde message
        response = requests.post("http://localhost:8001/conversation/message", 
                               json={
                                   "telegram_id": "test_user_123",
                                   "conversation_id": conversation_id,
                                   "user_message": "Test message",
                                   "bot_response": "Test response"
                               })
        
        if response.status_code == 200:
            print("✅ Message sauvegardé (mode local)")
        else:
            print(f"❌ Erreur sauvegarde: {response.status_code}")
            return False
            
    else:
        print(f"❌ Erreur création conversation: {response.status_code}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Test simple de l'API chatbot")
    print("=" * 50)
    
    if test_chat_api():
        print("✅ Tests API /chat réussis!")
    else:
        print("❌ Tests API /chat échoués!")
        exit(1)
    
    if test_conversation_endpoints():
        print("✅ Tests endpoints conversation réussis!")
    else:
        print("❌ Tests endpoints conversation échoués!")
        exit(1)
    
    print("=" * 50)
    print("🎉 Tous les tests sont passés! L'API fonctionne en mode local.")
    print("📝 Le bot devrait maintenant répondre intelligemment via Mistral AI.")
