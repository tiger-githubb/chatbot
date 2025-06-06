from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Awaitable, Callable, Dict, List, Optional, Union
from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI, Request, Response, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from mistralai import ChatCompletionResponse, Mistral
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from .config import env_vars
from .telegram_bot import telegram_bot
from .utils import Utils

ExceptionHandler = Union[
    Callable[[Request, Exception], Union[Response, Awaitable[Response]]],
    Callable[[WebSocket, Exception], Awaitable[None]],
]

api_key = env_vars.MISTRAL_API_KEY
model = "mistral-small-latest"
client = Mistral(api_key=api_key)

limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def app_lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    Utils.log_info("Starting the application")
    yield


app = FastAPI(
    title="ChatBot API",
    description="Chatbot API description",
    version="1.0.0",
    lifespan=app_lifespan,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
@limiter.limit("5/minute")
async def root(request: Request) -> Dict[str, str]:
    return {"msg": "Hello World"}


@app.post(env_vars.TELEGRAM_WEBHOOK_PATH)
@limiter.limit("60/minute")
async def telegram_webhook(request: Request, background_tasks: BackgroundTasks) -> Dict[str, str]:
    try:
        content_type = request.headers.get("content-type", "")
        if not content_type.startswith("application/json"):
            Utils.log_error(f"Invalid content-type: {content_type}")
            return {"status": "error", "message": "Invalid content-type"}

        body = await request.body()
        if not body:
            Utils.log_error("Empty request body received")
            return {"status": "error", "message": "Empty request body"}

        try:
            update_data = await request.json()
        except ValueError as json_error:
            Utils.log_error(f"JSON parsing error: {json_error}. Raw body: {body.decode('utf-8', errors='ignore')}")
            return {"status": "error", "message": f"Invalid JSON: {json_error}"}

        if not update_data:
            Utils.log_error("Parsed JSON is empty")
            return {"status": "error", "message": "Empty update data"}

        background_tasks.add_task(telegram_bot.handle_update, update_data)
        return {"status": "ok"}

    except Exception as e:
        error_msg = str(e)
        Utils.log_error(f"==> Error in telegram_webhook: {error_msg}")
        Utils.log_error(f"Error type: {type(e).__name__}")
        return {"status": "error", "message": error_msg}


@app.get("/chat")
@limiter.limit("30/minute")
async def chat(
    request: Request, question: str, conversation_id: Optional[str] = None
) -> Dict[str, Dict[str, str]]:
    Utils.log_info(f"Nouvelle question reçue: {question}")

    if not conversation_id:
        conversation_id = str(uuid4())
        Utils.log_info(f"Nouvelle conversation créée avec ID: {conversation_id}")

    try:
        chat_response: ChatCompletionResponse = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": question,
                },
            ],
        )
        Utils.log_info("Réponse reçue de Mistral AI")

        if not chat_response.choices:
            raise ValueError("No response received from Mistral AI")

        timestamp = datetime.now(timezone.utc).isoformat()
        response = {
            "id": {"S": f"{chat_response.id}"},
            "conversation_id": {"S": conversation_id},
            "timestamp": {"S": timestamp},
            "question": {"S": f"{question}"},
            "answer": {"S": f"{chat_response.choices[0].message.content}"},
            "source": {"S": "api"},
        }
        Utils.insert_data(response)
        Utils.log_info("Traitement de la question terminé avec succès")
        return response
    except Exception as e:
        Utils.log_error(f"Erreur lors du traitement de la question: {str(e)}")
        raise e


@app.get("/conversations/{conversation_id}")
@limiter.limit("30/minute")
async def get_conversation(
    request: Request, conversation_id: str
) -> Dict[str, List[Dict[str, Any]]]:
    messages = Utils.get_conversation_messages(conversation_id)
    return {"messages": messages}


@app.get("/chats/{user_id}")
@limiter.limit("30/minute")
async def get_user_chats(request: Request, user_id: str) -> Dict[str, List[Dict[str, Any]]]:
    messages = Utils.get_user_conversations(user_id)
    return {"conversations": messages}


handler = Mangum(app)
