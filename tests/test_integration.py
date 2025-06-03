"""
Tests d'intégration pour les composants AWS
"""
import pytest
import os
from unittest.mock import patch, MagicMock


def test_config_loading():
    """Test que la configuration se charge correctement"""
    from src.config import settings
    
    # Vérifier que les settings existent
    assert hasattr(settings, 'ENV_NAME')
    assert hasattr(settings, 'AWS_REGION')
    assert hasattr(settings, 'DYNAMO_TABLE')


def test_utils_import():
    """Test que les utils s'importent correctement"""
    from src.utils import Utils
    
    # Vérifier que les méthodes importantes existent
    assert hasattr(Utils, 'get_dynamo_client')
    assert hasattr(Utils, 'insert_chat_message')
    assert hasattr(Utils, 'log_info')


@patch('boto3.client')
def test_dynamodb_client_creation(mock_boto3_client):
    """Test la création du client DynamoDB avec des credentials"""
    from src.utils import Utils
    from src.config import settings
    
    # Mock du client DynamoDB
    mock_client = MagicMock()
    mock_boto3_client.return_value = mock_client
    
    # Simuler des credentials AWS
    with patch.object(settings, 'AWS_ACCESS_KEY_ID', 'test_key_id'):
        with patch.object(settings, 'AWS_SECRET_ACCESS_KEY', 'test_secret'):
            with patch.object(settings, 'AWS_REGION', 'eu-west-3'):
                client = Utils.get_dynamo_client()
                
                # Vérifier que boto3.client a été appelé avec les bons paramètres
                mock_boto3_client.assert_called_once_with(
                    'dynamodb',
                    aws_access_key_id='test_key_id',
                    aws_secret_access_key='test_secret',
                    region_name='eu-west-3'
                )


def test_telegram_bot_import():
    """Test que le bot Telegram s'importe correctement"""
    # Test d'import sans échec
    try:
        from src.telegram_bot import TelegramBot
        assert TelegramBot is not None
    except ImportError as e:
        pytest.fail(f"Impossible d'importer TelegramBot: {e}")


def test_main_app_import():
    """Test que l'application FastAPI s'importe correctement"""
    try:
        from src.main import app, handler
        assert app is not None
        assert handler is not None
    except ImportError as e:
        pytest.fail(f"Impossible d'importer l'app FastAPI: {e}")


@patch('src.utils.boto3.client')
def test_insert_chat_message_structure(mock_boto3_client):
    """Test la structure des données pour insert_chat_message"""
    from src.utils import Utils
    
    # Mock du client DynamoDB
    mock_client = MagicMock()
    mock_boto3_client.return_value = mock_client
    mock_client.put_item.return_value = {}
    
    # Test avec des données valides
    with patch.object(Utils, 'get_dynamo_client', return_value=mock_client):
        result = Utils.insert_chat_message(
            conversation_id="test_conv",
            user_id="test_user",
            user_message="Hello",
            bot_response="Hi there!",
            mistral_id="test_mistral_id"
        )
        
        # Vérifier que put_item a été appelé
        assert mock_client.put_item.called
        
        # Récupérer les arguments de l'appel
        call_args = mock_client.put_item.call_args
        item = call_args[1]['Item']
        
        # Vérifier la structure des données DynamoDB
        assert 'id' in item
        assert 'S' in item['id']
        assert 'conversation_id' in item
        assert item['conversation_id']['S'] == "test_conv"
        assert 'user_id' in item
        assert item['user_id']['S'] == "test_user"
        assert 'mistral_id' in item
        assert item['mistral_id']['S'] == "test_mistral_id"


def test_environment_variables_format():
    """Test que les variables d'environnement ont le bon format"""
    from src.config import settings
    
    # Vérifier que AWS_REGION a un format valide
    if settings.AWS_REGION:
        assert isinstance(settings.AWS_REGION, str)
        assert len(settings.AWS_REGION) > 0
    
    # Vérifier que TELEGRAM_WEBHOOK_PATH commence par /
    if settings.TELEGRAM_WEBHOOK_PATH:
        assert settings.TELEGRAM_WEBHOOK_PATH.startswith('/')


def test_lambda_handler_exists():
    """Test que le handler Lambda existe et est callable"""
    from src.main import handler
    
    assert callable(handler)
    
    # Test avec un événement minimal (sans l'exécuter réellement)
    assert handler is not None
