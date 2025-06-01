import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, Application
from config import settings

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
        self.application.add_handler(CommandHandler("start", self._start_command))
        self.application.add_handler(CommandHandler("help", self._help_command))
        self.application.add_handler(CommandHandler("close", self._close_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))

    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gère la commande /start"""
        user_id = str(update.effective_user.id)
        try:
            # Clôture la dernière conversation active si elle existe
            resp = requests.get(f"{API_URL}/conversation/active/{user_id}")
            if resp.status_code == 200:
                last_cid = resp.json().get("conversation_id")
                if last_cid:
                    requests.post(f"{API_URL}/conversation/{last_cid}/close", json={"telegram_id": user_id})
            
            # Démarre une nouvelle conversation
            resp = requests.post(f"{API_URL}/conversation/start", json={"telegram_id": user_id})
            conversation_id = resp.json().get("conversation_id")
            context.user_data["conversation_id"] = conversation_id
            
            welcome_message = (
                "👋 Bonjour ! Je suis votre assistant conversationnel.\n\n"
                "💬 Nouvelle conversation démarrée. Posez-moi une question !\n\n"
                "Commandes disponibles:\n"
                "🔹 /help - Afficher l'aide\n"
                "🔹 /close - Clôturer la conversation\n\n"
                "Envoyez-moi simplement un message pour commencer!"
            )
            await update.message.reply_text(welcome_message)
        except Exception as e:
            logging.error(f"Erreur dans /start: {e}")
            await update.message.reply_text("Erreur lors du démarrage. Réessayez plus tard.")

    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gère la commande /help"""
        help_message = (
            "📚 Guide d'utilisation\n\n"
            "1️⃣ Conversation normale:\n"
            "   - Envoyez simplement vos messages\n"
            "   - Je maintiens le contexte de la conversation\n\n"
            "2️⃣ Commandes disponibles:\n"
            "   🔸 /start - Démarrer une nouvelle conversation\n"
            "   🔸 /help - Afficher ce message d'aide\n"
            "   🔸 /close - Clôturer la conversation active\n\n"
            "3️⃣ Conseils:\n"
            "   - Soyez précis dans vos questions\n"
            "   - Une question à la fois pour de meilleurs résultats\n\n"
            "Pour toute question, n'hésitez pas à demander!"
        )
        await update.message.reply_text(help_message)

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gère les messages texte reçus"""
        user_id = str(update.effective_user.id)
        user_message = update.message.text

        try:
            # Récupérer la dernière conversation active ou en démarrer une
            resp = requests.get(f"{API_URL}/conversation/active/{user_id}")
            conversation_id = None
            if resp.status_code == 200:
                conversation_id = resp.json().get("conversation_id")
            
            if not conversation_id:
                resp = requests.post(f"{API_URL}/conversation/start", json={"telegram_id": user_id})
                if resp.status_code == 200:
                    conversation_id = resp.json().get("conversation_id")

            # Envoyer la question à l'API /chat
            chat_resp = requests.get(f"{API_URL}/chat", params={"question": user_message})
            if chat_resp.status_code == 200:
                answer = chat_resp.json().get("answer", {}).get("S", "Je n'ai pas compris votre question.")
            else:
                answer = "Désolé, je rencontre des difficultés techniques. Réessayez plus tard."

            # Sauvegarder la conversation
            if conversation_id:
                requests.post(f"{API_URL}/conversation/message", json={
                    "telegram_id": user_id,
                    "conversation_id": conversation_id,
                    "user_message": user_message,
                    "bot_response": answer
                })

            # Répondre à l'utilisateur
            await update.message.reply_text(answer)

        except Exception as e:
            logging.error(f"Erreur lors du traitement du message: {e}")
            await update.message.reply_text(
                "Désolé, une erreur s'est produite lors du traitement de votre message. Réessayez plus tard."
            )

    async def _close_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gère la commande /close"""
        user_id = str(update.effective_user.id)
        try:
            # Clôture la dernière conversation active
            resp = requests.get(f"{API_URL}/conversation/active/{user_id}")
            if resp.status_code == 200:
                conversation_id = resp.json().get("conversation_id")
                if conversation_id:
                    requests.post(f"{API_URL}/conversation/{conversation_id}/close", json={"telegram_id": user_id})
                    await update.message.reply_text("✅ Conversation clôturée. Tapez /start pour en démarrer une nouvelle.")
                else:
                    await update.message.reply_text("Aucune conversation active à clôturer.")
            else:
                await update.message.reply_text("Aucune conversation active à clôturer.")
        except Exception as e:
            logging.error(f"Erreur dans /close: {e}")
            await update.message.reply_text("Erreur lors de la clôture. Réessayez plus tard.")

    async def handle_update(self, update_data: dict):
        """Gère les mises à jour reçues via le webhook"""
        async with self.application:
            update = Update.de_json(update_data, self.application.bot)
            if update:
                await self.application.process_update(update)

    def run_polling(self):
        """Lance le bot en mode polling (pour tests locaux)"""
        print("Bot Telegram démarré en mode polling. Appuyez sur Ctrl+C pour arrêter.")
        self.application.run_polling()

# Instance globale du bot pour l'import
telegram_bot = TelegramBot()

# Fonctions de compatibilité pour l'ancien code
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await telegram_bot._start_command(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await telegram_bot._handle_message(update, context)

async def close(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await telegram_bot._close_command(update, context)

def main():
    """Lance le bot en mode polling pour les tests locaux"""
    telegram_bot.run_polling()

if __name__ == "__main__":
    main()
