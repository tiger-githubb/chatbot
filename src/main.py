from fastapi import Path, Request
from uuid import uuid4
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from mangum import Mangum
import json, boto3
from mistralai.client import MistralClient
import os

from config import settings
from utils import Utils

class ConversationMessageIn(BaseModel):
    telegram_id: str
    conversation_id: str
    user_message: str
    bot_response: str
    timestamp: str = None

class ConversationMessageOut(BaseModel):
    conversation_id: str
    user_message: str
    bot_response: str
    timestamp: str

api_key = settings.MISTRAL_API_KEY
if not api_key or api_key.strip() == "":
    raise RuntimeError("MISTRAL_API_KEY is missing or empty. Please set it in your environment variables or .env file.")
model = "mistral-small-latest"
client = MistralClient(api_key=api_key)



@asynccontextmanager
async def app_lifespan(application: FastAPI):
    Utils.log_info("Starting the application")
    yield



app = FastAPI(
    title="ChatBot API",
    description="Chatbot API description",
    version="1.0.0",
    lifespan=app_lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Redirige le root vers la documentation interactive
from fastapi.responses import RedirectResponse

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/chat")
async def chat(question: str):
    try:
        chat_response = client.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": question,
                },
            ]
        )
        print("chat_response:", chat_response)
        
        # Format simple pour le mode local (sans DynamoDB)
        answer_content = ""
        if hasattr(chat_response, 'choices') and chat_response.choices:
            answer_content = getattr(chat_response.choices[0].message, 'content', 'no_content')
        
        response = {
            "id": {
                "S": f"{getattr(chat_response, 'id', 'no_id')}",
            },
            "question": {
                "S": f"{question}",
            },
            "answer": {
                "S": answer_content,
            }
        }
        
        # Temporairement désactivé pour le mode local
        # Utils.insert_data(response)
        print(f"Mode local - Réponse générée: {answer_content}")
        
        return response
    except Exception as e:
        import traceback
        print("Exception in /chat endpoint:", e)
        traceback.print_exc()
        return {"error": str(e)}

# --- Conversation Management Endpoints ---

# 1. Démarrer une conversation et obtenir un conversation_id
class ConversationStartIn(BaseModel):
    telegram_id: str

class ConversationStartOut(BaseModel):
    conversation_id: str

@app.post("/conversation/start", response_model=ConversationStartOut)
async def start_conversation(data: ConversationStartIn):
    """
    Démarre une nouvelle conversation pour un utilisateur et retourne un conversation_id unique.
    Mode local - génère un ID simple sans stockage DynamoDB.
    """
    # Mode local - génération d'un ID simple
    conversation_id = f"conv_{data.telegram_id}_{uuid4().hex[:8]}"
    print(f"Mode local - Nouvelle conversation: {conversation_id}")
    return {"conversation_id": conversation_id}

# 2. Récupérer l'historique d'une conversation précise
@app.get("/conversation/{conversation_id}/history")
async def get_conversation_history_by_id(conversation_id: str = Path(...), telegram_id: str = None, limit: int = 50):
    """
    Récupère l'historique des messages pour un conversation_id donné (optionnellement filtré par telegram_id).
    Mode local - retourne un historique vide.
    """
    if not telegram_id:
        raise HTTPException(status_code=400, detail="telegram_id est requis pour la requête.")
    
    # Mode local - retourne un historique vide
    print(f"Mode local - Historique demandé pour conversation: {conversation_id}")
    return {"history": []}


# --- Conversation Endpoints (placés après la création de app) ---
@app.post("/conversation/message", response_model=None)
async def save_conversation_message(data: ConversationMessageIn):
    """
    Enregistre un message utilisateur + réponse bot dans DynamoDB.
    Mode local - affiche seulement dans les logs.
    """
    try:
        # Mode local - juste afficher dans les logs
        print(f"Mode local - Message sauvegardé:")
        print(f"  User: {data.telegram_id}")
        print(f"  Conversation: {data.conversation_id}")
        print(f"  Message: {data.user_message}")
        print(f"  Réponse: {data.bot_response}")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversation/history/{telegram_id}")
async def get_conversation_history(telegram_id: str, limit: int = 20):
    """
    Récupère l'historique des messages pour un utilisateur (par son Telegram ID).
    Mode local - retourne un historique vide.
    """
    try:
        # Mode local - retourne un historique vide
        print(f"Mode local - Historique demandé pour utilisateur: {telegram_id}")
        return {"history": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. Clôturer une conversation
class ConversationCloseIn(BaseModel):
    telegram_id: str

@app.post("/conversation/{conversation_id}/close")
async def close_conversation(conversation_id: str = Path(...), data: ConversationCloseIn = Body(...)):
    """
    Clôture une conversation (status=closed pour tous les messages de cette conversation).
    Mode local - affiche seulement dans les logs.
    """
    try:
        # Mode local - juste afficher dans les logs
        print(f"Mode local - Conversation fermée: {conversation_id} pour utilisateur: {data.telegram_id}")
        return {"status": "closed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. Récupérer la dernière conversation active d'un utilisateur
@app.get("/conversation/active/{telegram_id}")
async def get_last_active_conversation(telegram_id: str):
    """
    Retourne le dernier conversation_id actif (non clos) pour un utilisateur.
    Mode local - retourne toujours None pour créer une nouvelle conversation.
    """
    # Mode local - retourne toujours None pour forcer la création d'une nouvelle conversation
    print(f"Mode local - Conversation active demandée pour: {telegram_id}")
    return {"conversation_id": None}

# --- Telegram Webhook Endpoint ---
@app.post(settings.TELEGRAM_WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    """
    Endpoint pour recevoir les mises à jour de Telegram via webhook
    """
    try:
        # Récupération et validation des données
        update_data = await request.json()
        
        # Log de debug (masquer les données sensibles en production)
        if settings.ENV_NAME != "production":
            Utils.log_info(f"Webhook reçu: {update_data}")
        else:
            Utils.log_info("Webhook reçu (données masquées en production)")        # Import du bot Telegram et traitement de la mise à jour
        from telegram_bot import TelegramBot
        
        # Créer une instance si nécessaire ou utiliser l'instance globale
        try:
            from telegram_bot import telegram_bot
            bot_instance = telegram_bot
        except ImportError:
            bot_instance = TelegramBot()
          # Traitement de la mise à jour en arrière-plan pour éviter les timeouts
        import asyncio
        # Créer une tâche asynchrone pour traiter l'update sans bloquer la réponse
        asyncio.create_task(bot_instance.handle_update(update_data))
        
        Utils.log_info("Webhook accepté - traitement en cours en arrière-plan")
        return {"status": "ok"}
        
    except ValueError as e:
        Utils.log_error(f"Données JSON invalides dans le webhook: {str(e)}")
        raise HTTPException(status_code=400, detail="Données JSON invalides")
    except Exception as e:
        Utils.log_error(f"Erreur lors du traitement du webhook Telegram: {str(e)}")
        import traceback
        Utils.log_error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Erreur lors du traitement du webhook")



async def chats():
    # Get al chats here
    return {}

handler = Mangum(app)
