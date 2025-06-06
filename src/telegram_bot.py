from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler,
)
from .config import env_vars
from .utils import Utils
from datetime import datetime


class TelegramBot:
    def __init__(self) -> None:
        self.application = Application.builder().token(env_vars.TELEGRAM_BOT_TOKEN).build()
        self.application.add_error_handler(self._error_handler)
        self._setup_handlers()

    async def _error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        Utils.log_error(f"Unhandled exception: {context.error}")

    def _setup_handlers(self) -> None:
        """Configure les gestionnaires de commandes du bot"""
        self.application.add_handler(CommandHandler("start", self._start_command))
        self.application.add_handler(CommandHandler("help", self._help_command))
        self.application.add_handler(CommandHandler("stats", self._stats_command))
        self.application.add_handler(CommandHandler("clear", self._clear_command))
        self.application.add_handler(CallbackQueryHandler(self._button_click))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message)
        )

    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Gère la commande /start"""
        if not update.message or not update.effective_chat:
            Utils.log_error("Ignored update: not a message or chat.")
            return

        welcome_message = (
            "🐅 Salut ! Moi c'est Tiger, ton assistant IA !\n\n"
            "✨ Je suis là pour tchatcher avec toi et t'aider sur tout ce que tu veux :\n"
            "• Répondre à tes questions (même les plus bizarres)\n"
            "• Expliquer des trucs compliqués simplement\n"
            "• T'aider sur tes projets\n"
            "• Analyser du contenu\n\n"
            "🎯 Commandes dispo :\n"
            "• /help - Si tu veux plus d'infos\n"
            "• /stats - Voir tes stats de chat\n"
            "• /clear - Reset total si tu veux repartir à zéro\n\n"
            "💬 Balance-moi juste ton message et on se lance ! 🚀"
        )
        await self.application.bot.send_message(
            chat_id=update.message.chat.id, text=welcome_message
        )

    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Gère la commande /help"""
        if not update.message or not update.effective_chat:
            return

        help_message = (
            "📚 Guide Tiger - Comment ça marche ?\n\n"
            "🤙 En gros c'est simple :\n"
            "   • Tu m'écris ce que tu veux\n"
            "   • Je traite chaque message indépendamment\n"
            "   • Je te réponds avec l'IA Mistral\n"
            "   • Tout est sauvegardé au cas où\n\n"
            "⚡ Les commandes qui marchent vraiment :\n"
            "   🔸 /start - Retour à l'accueil\n"
            "   🔸 /help - Ce message (tu y es déjà !)\n"
            "   🔸 /stats - Tes stats de ouf\n"
            "   🔸 /clear - Effacer l'historique si tu veux reset\n\n"
            "💡 Mes tips pour bien s'amuser :\n"
            "   • Sois précis, ça m'aide à mieux répondre\n"
            "   • Une question à la fois, on n'est pas pressés\n"
            "   • Si je bug, utilise /clear et on repart\n\n"
            "🤔 Une question ? Vas-y, pose-moi ce que tu veux !"
        )
        await self.application.bot.send_message(chat_id=update.message.chat.id, text=help_message)

    async def _stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Gère la commande /stats"""
        if not update.effective_chat or not update.message:
            return

        if not update.message and not update.callback_query:
            Utils.log_info("Ignored update: not a message or callback query.")
            return

        chat_id = str(update.effective_chat.id)
        try:
            # Récupérer les statistiques depuis DynamoDB
            messages = Utils.get_conversation_messages(chat_id)

            total_messages = len(messages)
            if total_messages > 0:
                first_message = min(messages, key=lambda x: x["timestamp"])
                first_date = datetime.fromisoformat(first_message["timestamp"])
                average_messages_per_day = total_messages / max(
                    1, (datetime.now() - first_date).days
                )

                stats_message = (
                    "📊 Tes stats de ouf avec Tiger !\n\n"
                    f"💬 Messages échangés ensemble : {total_messages}\n"
                    f"📅 On se connaît depuis le : {first_date.strftime('%d/%m/%Y à %H:%M')}\n"
                    f"⏱️ Ça fait : {(datetime.now() - first_date).days} jour(s) qu'on tchat\n"
                    f"📈 En moyenne : {average_messages_per_day:.1f} message(s) par jour\n\n"
                    f"🔥 Continue comme ça, on forme une super équipe ! 🚀"
                )
            else:
                stats_message = (
                    "📊 Tes stats avec Tiger\n\n"
                    "🆕 Hey ! On vient juste de se rencontrer !\n\n"
                    "💡 Commençons l'aventure :\n"
                    "• Pose-moi une question cool\n"
                    "• Demande-moi d'expliquer un truc\n"
                    "• Fais-moi analyser quelque chose\n"
                    "• Ou on peut juste papoter tranquille\n\n"
                    "🎯 Tes stats vont apparaître ici au fur et à mesure de nos discussions !"
                )

            await self.application.bot.send_message(
                chat_id=update.message.chat.id, text=stats_message
            )
        except Exception as e:
            Utils.log_error(f"Erreur lors de la récupération des statistiques: {str(e)}")
            await self.application.bot.send_message(
                chat_id=update.message.chat.id,
                text="😅 Oups, Tiger a un petit problème technique avec tes stats...\n\n"
                     "🔄 Réessaie dans quelques secondes, ça devrait passer !",
            )

    async def _clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Gère la commande /clear"""
        if not update.message or not update.effective_chat:
            return

        keyboard = [
            [
                InlineKeyboardButton("🗑️ Ouais, on efface tout", callback_data="clear_confirm"),
                InlineKeyboardButton("🔙 Non, on garde", callback_data="clear_cancel"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await self.application.bot.send_message(
            chat_id=update.message.chat.id,
            text="⚠️ Attends, tu es sûr ?\n\n"
                 "Tiger va supprimer définitivement :\n"
                 "• Tout notre historique de chat\n"
                 "• Toutes tes questions et mes réponses\n"
                 "• Tes stats actuelles\n\n"
                 "⚡ Impossible de revenir en arrière après ça !\n\n"
                 "Tu confirmes le reset total ?",
            reply_markup=reply_markup,
        )

    async def _button_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Gère les clics sur les boutons inline"""
        if not update.callback_query or not update.effective_chat:
            return

        query = update.callback_query
        await query.answer()

        if not query.data:
            return

        if query.data.startswith("clear_"):
            action = query.data.split("_")[1]
            chat_id = str(update.effective_chat.id)
            if action == "confirm":
                try:
                    # Supprimer les messages
                    Utils.delete_conversation_messages(chat_id)
                    await query.edit_message_text(
                        "✅ C'est fait ! Historique effacé !\n\n"
                        "🆕 On repart à zéro toi et moi.\n"
                        "💬 Vas-y, relance-moi quelque chose de cool ! 🚀"
                    )
                except Exception as e:
                    Utils.log_error(f"Erreur lors de la suppression de l'historique: {str(e)}")
                    await query.edit_message_text(
                        "😅 Oups ! Tiger galère à effacer l'historique...\n\n"
                        "🔧 Problème technique temporaire.\n"
                        "🔄 Réessaie dans quelques instants !"
                    )
            else:
                await query.edit_message_text(
                    "👍 Parfait ! On garde tout !\n\n"
                    "✅ Notre historique de chat est bien conservé.\n"
                    "💬 On continue notre discussion ! 😎"
                )

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Gère les messages texte reçus"""
        if not update.effective_chat or not update.message:
            return

        if not update.message and not update.callback_query:
            Utils.log_info("Ignored update: not a message or callback query.")
            return

        chat_id = str(update.effective_chat.id)
        message_text = update.message.text

        try:
            Utils.log_info(
                f"Message reçu de Telegram - Chat ID: {chat_id}, Message: {message_text}"
            )

            # Utiliser directement le client Mistral
            from .main import client, model

            chat_response = client.chat.complete(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": message_text,
                    },
                ],
            )

            if not chat_response.choices:
                raise ValueError("No response received from Mistral AI")

            # Sauvegarder dans DynamoDB
            timestamp = datetime.now().isoformat()
            response = {
                "id": {
                    "S": f"{chat_response.id}",
                },
                "conversation_id": {"S": chat_id},
                "timestamp": {"S": timestamp},
                "question": {
                    "S": f"{message_text}",
                },
                "answer": {
                    "S": f"{chat_response.choices[0].message.content}",
                },
                "source": {"S": "telegram"},
            }
            Utils.insert_data(response)

            # Envoyer la réponse à l'utilisateur
            await self.application.bot.send_message(
                chat_id=update.message.chat.id, text=chat_response.choices[0].message.content
            )

        except Exception as e:
            Utils.log_error(f"Erreur lors du traitement du message Telegram: {str(e)}")
            await self.application.bot.send_message(
                chat_id=update.message.chat.id,
                text="😅 Oups ! Tiger a un petit bug là...\n\n"
                     "🔄 Réessaie ton message dans quelques secondes !\n"
                     "💡 Si ça persiste, utilise /clear pour qu'on reparte à zéro.",
            )

    async def setup_webhook(self) -> None:
        """Configure le webhook pour le bot"""
        webhook_url = f"{env_vars.TELEGRAM_WEBHOOK_URL}{env_vars.TELEGRAM_WEBHOOK_PATH}"
        await self.application.bot.set_webhook(webhook_url)
        Utils.log_info(f"Webhook set to {webhook_url}")

    async def handle_update(self, update_data: dict) -> None:
        """Gère les mises à jour reçues via le webhook"""
        async with self.application:
            update = Update.de_json(update_data, self.application.bot)
            if update:
                await self.application.process_update(update)


telegram_bot = TelegramBot()
