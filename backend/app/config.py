##### ERROR ########
'''
        ERROR
not able to get the data from .env file
'''


from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from os import getenv
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):

    database_hostname: str = getenv('DATABASE_HOSTNAME') or ""
    database_port: str = getenv('DATABASE_PORT') or ''
    database_username: str = getenv('DATABASE_USERNAME') or ''
    database_password: str = getenv("DATABASE_PASSWORD") or ''
    database_name: str = getenv("DATABASE_NAME") or ''
    secret_key: str = getenv("SECRET_KEY") or ''
    algorithm: str = getenv("ALGORITHM") or ''
    access_token_expire_minute: str = getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or ''
    
    # model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, env_prefix='', env_file_encoding='utf-8') NOT WORKING

settings = Settings() 

