import logging

from pydantic import SecretStr

from app.core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    debug: bool = True
    title: str = "Test FastAPI Inventory App"
    secret_key: SecretStr = SecretStr("test_secret")
    
    database_url: str #FIXME:
    max_connection_count: int = 5
    min_connection_count: int = 5
    
    logging_level: int = logging.DEBUG