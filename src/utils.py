from datetime import datetime
import json
from uuid import uuid4
import logging
from typing import List

import boto3

from config import settings
## Simple edit


class Utils:
    
    @staticmethod
    def close_conversation(conversation_id: str, telegram_id: str):
        """
        Marque une conversation comme close (ajoute ou met à jour un item status=closed).
        """
        dynamo_client = Utils.get_dynamo_client()
        # On récupère tous les items de la conversation pour cet utilisateur et on les met à jour
        items = Utils.get_conversation_history_by_id(conversation_id, telegram_id)
        for item in items:
            pk = item['PK']['S']
            sk = item['SK']['S']
            dynamo_client.update_item(
                TableName=settings.DYNAMO_TABLE,
                Key={"PK": {"S": pk}, "SK": {"S": sk}},
                UpdateExpression="SET #s = :closed",
                ExpressionAttributeNames={"#s": "status"},
                ExpressionAttributeValues={":closed": {"S": "closed"}}
            )

    @staticmethod
    def get_last_active_conversation(telegram_id: str):
        """
        Retourne le dernier conversation_id actif (status != closed) pour un utilisateur.
        """
        dynamo_client = Utils.get_dynamo_client()
        response = dynamo_client.query(
            TableName=settings.DYNAMO_TABLE,
            KeyConditionExpression='PK = :pk',
            ExpressionAttributeValues={
                ':pk': {'S': f'USER#{telegram_id}'},
            },
            ScanIndexForward=False,  # du plus récent au plus ancien
            Limit=50
        )
        items = response.get('Items', [])
        for item in items:
            # On considère la première conversation non close comme la dernière active
            if item.get('status', {}).get('S', 'active') != 'closed':
                return item.get('conversation_id', {}).get('S', None)
        return None

    @staticmethod
    def start_conversation(telegram_id: str) -> str:
        """
        Crée un nouvel identifiant de conversation (UUID) et retourne cet ID.
        """
        conversation_id = str(uuid4())
        # Optionnel : on peut enregistrer un "démarrage" de conversation dans DynamoDB si besoin
        # Ici, on ne stocke rien, on retourne juste l'ID
        return conversation_id    @staticmethod
    def get_conversation_history_by_id(conversation_id: str, telegram_id: str = None, limit: int = 50):
        """
        Récupère l'historique des messages pour un conversation_id donné (optionnellement filtré par telegram_id).
        Nécessite que conversation_id soit un attribut dans chaque item.
        """
        dynamo_client = Utils.get_dynamo_client()
        # Utilisation de Query avec FilterExpression (pas optimal, mais pas de Scan)
        # Si un GSI sur conversation_id existe, il faudrait l'utiliser ici
        key_condition = 'PK = :pk'
        expr_attr = {':pk': {'S': f'USER#{telegram_id}'}}
        response = dynamo_client.query(
            TableName=settings.DYNAMO_TABLE,
            KeyConditionExpression=key_condition,
            FilterExpression='conversation_id = :cid',
            ExpressionAttributeValues={**expr_attr, ':cid': {'S': conversation_id}},
            Limit=limit,
            ScanIndexForward=True
        )
        return response.get('Items', [])
    
    @staticmethod
    def save_conversation_message(telegram_id: str, conversation_id: str, user_message: str, bot_response: str, timestamp: str = None):
        """
        Enregistre un message de conversation dans DynamoDB avec la structure PK/SK recommandée.
        """
        if not timestamp:
            timestamp = datetime.utcnow().isoformat()
        item = {
            'PK': {'S': f'USER#{telegram_id}'},
            'SK': {'S': f'MSG#{timestamp}'},
            'conversation_id': {'S': conversation_id},
            'user_message': {'S': user_message},
            'bot_response': {'S': bot_response},
            'timestamp': {'S': timestamp},
        }
        dynamo_client = Utils.get_dynamo_client()
        dynamo_client.put_item(
            TableName=settings.DYNAMO_TABLE,
            Item=item,
        )

    @staticmethod
    def get_conversation_history(telegram_id: str, limit: int = 20):
        """
        Récupère l'historique des messages d'un utilisateur via Query (jamais Scan).
        """
        dynamo_client = Utils.get_dynamo_client()
        response = dynamo_client.query(
            TableName=settings.DYNAMO_TABLE,
            KeyConditionExpression='PK = :pk',
            ExpressionAttributeValues={
                ':pk': {'S': f'USER#{telegram_id}'},
            },
            Limit=limit,
            ScanIndexForward=True  # Chronological order
        )
        return response.get('Items', [])

    ALLOWED_EXTENSIONS = ["pdf", "docx", "doc", "png", "jpg", "jpeg"]

    @staticmethod
    def log_info(message):
        """_summary_
        Log a simple info message
        """
        logging.getLogger("uvicorn.error").info(msg=f"==> {message}")

    @staticmethod
    def log_debug(message):
        """_summary_
        Log a debug message
        """
        logging.getLogger("uvicorn.error").debug(msg=f"==> {message}")

    @staticmethod
    def log_error(message):
        """_summary_
        Log an error message
        """
        logging.getLogger("uvicorn.error").error(msg=f"==> {message}")

    @staticmethod
    def log_list(elements: List[any]):
        if elements:
            logging.getLogger("uvicorn.error").info(
                msg=f"Displaying all the {len(elements)} elements of the list"
            )
            for i in range(len(elements)):
                logging.getLogger("uvicorn.error").info(
                    msg=f"##### {i} ==> {json.dumps(elements[i], indent=4)}"
                )

    @staticmethod
    def get_logger():
        return logging.getLogger("uvicorn.error")    @staticmethod
    def get_session():
        return boto3.Session(
            region_name=settings.AWS_REGION, profile_name=settings.AWS_PROFILE
        )

    @staticmethod
    def get_dynamo_client():
        """Retourne un client DynamoDB configuré avec les bonnes credentials"""
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            return boto3.client(
                'dynamodb',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
        else:
            return boto3.client('dynamodb', region_name=settings.AWS_REGION)

    @staticmethod
    def insert_data(item):
        """Insère un item dans DynamoDB avec gestion d'erreurs améliorée"""
        try:
            dynamo_client = Utils.get_dynamo_client()
            dynamo_client.put_item(
                TableName=settings.DYNAMO_TABLE,
                Item=item,
            )
            Utils.log_info(f"Données sauvegardées dans DynamoDB: {item.get('id', {}).get('S', 'unknown_id')}")
            return True
        except Exception as e:
            Utils.log_error(f"Erreur lors de l'insertion DynamoDB: {e}")
            return False

    @staticmethod
    def insert_chat_message(conversation_id: str, user_id: str, user_message: str, bot_response: str, mistral_id: str = None):
        """
        Insère un message de chat complet dans DynamoDB avec tous les champs requis et timestamp automatique
        """
        from datetime import datetime
        from uuid import uuid4
        
        timestamp = datetime.now().isoformat()
        created_date = datetime.now().strftime('%Y-%m-%d')
        message_id = f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"
        
        item = {
            'id': {'S': message_id},
            'conversation_id': {'S': conversation_id},
            'user_id': {'S': user_id},
            'user_message': {'S': user_message},
            'bot_response': {'S': bot_response},
            'timestamp': {'S': timestamp},
            'created_date': {'S': created_date},
            'source': {'S': 'telegram'}
        }
        
        # Ajouter l'ID Mistral si disponible
        if mistral_id:
            item['mistral_id'] = {'S': mistral_id}
        
        return Utils.insert_data(item)

# Export standalone functions for easier importing
def get_dynamo_client():
    """Standalone function to get DynamoDB client"""
    return Utils.get_dynamo_client()

def insert_chat_message(user_id: str, user_message: str, bot_response: str, source: str = "api", mistral_id: str = None):
    """
    Standalone function to insert chat message with auto-generated conversation_id
    """
    from datetime import datetime
    from uuid import uuid4
    
    # Generate conversation_id based on source
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    conversation_id = f"{source}_chat_{timestamp_str}_{uuid4().hex[:8]}"
    
    return Utils.insert_chat_message(conversation_id, user_id, user_message, bot_response, mistral_id)
