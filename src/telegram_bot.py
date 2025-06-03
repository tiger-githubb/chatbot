import logging
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from config import settings
from utils import insert_chat_message

API_URL = settings.API_URL if hasattr(settings, 'API_URL') else "http://localhost:8001"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class TelegramBot:
    def __init__(self):
        if not settings.TELEGRAM_BOT_TOKEN:
            raise RuntimeError("TELEGRAM_BOT_TOKEN manquant dans .env !")
        
        self.application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
        self._setup_handlers()

    def _setup_handlers(self):
        """Configure les gestionnaires de commandes du bot"""
        # L'ordre est important: CommandHandlers avant MessageHandler
        self.application.add_handler(CommandHandler("start", self._start_command))
        self.application.add_handler(CommandHandler("help", self._help_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))

    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gère la commande /start"""
        if not update.effective_user or not update.message:
            logging.error("Invalid update received in _start_command")
            return
            
        logging.info(f"Command /start received from user {update.effective_user.id}")
        
        welcome_message = (
            "👋 Bonjour ! Je suis votre assistant conversationnel.\n\n"
            "💬 Posez-moi une question et je vous répondrai !\n\n"
            "Commandes disponibles:\n"
            "🔹 /help - Afficher l'aide\n\n"
            "Envoyez-moi simplement un message pour commencer!"
        )
        
        try:
            await update.message.reply_text(welcome_message)
            logging.info(f"Welcome message sent to user {update.effective_user.id}")
        except Exception as e:
            logging.error(f"Erreur dans /start: {e}")
            if update.message:
                await update.message.reply_text("Erreur lors du démarrage. Réessayez plus tard.")

    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gère la commande /help"""
        if not update.effective_user or not update.message:
            logging.error("Invalid update received in _help_command")
            return
            
        logging.info(f"Command /help received from user {update.effective_user.id}")
        
        help_message = (
            "📚 Aide du Chatbot IA\n\n"
            "💬 **Utilisation normale:**\n"
            "Envoyez-moi simplement vos messages et je vous répondrai !\n\n"
            "🤖 **Commandes disponibles:**\n"
            "🔹 /start - Démarrer une nouvelle conversation\n"
            "🔹 /help - Afficher cette aide\n\n"
            "🧠 Je suis alimenté par Mistral AI et je peux vous aider avec diverses tâches."
        )
        
        try:
            await update.message.reply_text(help_message)
            logging.info(f"Help message sent to user {update.effective_user.id}")
        except Exception as e:
            logging.error(f"Erreur dans /help: {e}")
            if update.message:
                await update.message.reply_text("Erreur lors de l'affichage de l'aide.")

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gère les messages text des utilisateurs"""
        if not update.effective_user or not update.message or not update.message.text:
            logging.error("Invalid update received in _handle_message")
            return
            
        user_message = update.message.text
        user_id = str(update.effective_user.id)
        username = update.effective_user.username or f"user_{user_id}"
        
        logging.info(f"Message received from user {user_id} (@{username}): {user_message}")

        try:
            # Appeler l'API de chat pour obtenir une réponse
            async with httpx.AsyncClient(timeout=30) as client:
                chat_response = await client.get(f"{API_URL}/chat", params={"question": user_message})
                
                if chat_response.status_code == 200:
                    chat_data = chat_response.json()
                    answer = chat_data.get("answer", {}).get("S", "Désolé, je n'ai pas pu générer de réponse.")
                    mistral_id = chat_data.get("id", "")
                else:
                    logging.error(f"API chat error: {chat_response.status_code} - {chat_response.text}")
                    answer = "Désolé, une erreur s'est produite. Réessayez plus tard."
                    mistral_id = ""

            # Sauvegarder la conversation dans DynamoDB
            try:
                success = insert_chat_message(
                    user_id=user_id,
                    user_message=user_message,
                    bot_response=answer,
                    source="telegram",
                    mistral_id=mistral_id if mistral_id else None
                )
                if success:
                    logging.info(f"Conversation saved to DynamoDB for user {user_id}")
                else:
                    logging.warning(f"Failed to save conversation to DynamoDB for user {user_id}")
            except Exception as db_error:
                logging.error(f"DynamoDB error for user {user_id}: {db_error}")
                # Continue anyway - don't let DB errors prevent the response

            # Répondre à l'utilisateur
            await update.message.reply_text(answer)
            logging.info(f"Response sent to user {user_id}")

        except Exception as e:
            logging.error(f"Erreur lors du traitement du message: {e}")
            if update.message:
                await update.message.reply_text(
                    "Désolé, une erreur s'est produite lors du traitement de votre message. Réessayez plus tard."
                )

    async def handle_update(self, update_data: dict):
        """
        Gère les mises à jour reçues via le webhook.
        """
        try:
            # Utilisation du contexte async pour initialiser l'application
            async with self.application:
                update = Update.de_json(update_data, self.application.bot)
                if update:
                    logging.info(f"Processing update ID: {update.update_id}")
                    # Log plus détaillé pour debugging
                    if update.message and update.effective_user:
                        logging.info(f"Message from {update.effective_user.id}: {update.message.text}")
                    await self.application.process_update(update)
                else:
                    logging.warning("Received invalid update data")
        except Exception as e:
            logging.error(f"Error processing update: {e}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
            raise

    def run_polling(self):
        """Lance le bot en mode polling (pour tests locaux)"""
        print("Bot Telegram démarré en mode polling. Appuyez sur Ctrl+C pour arrêter.")
        self.application.run_polling()

# Créer une instance globale du bot
telegram_bot = TelegramBot()
