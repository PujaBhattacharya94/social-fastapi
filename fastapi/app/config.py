from pydantic_settings import BaseSettings
from pydantic_settings import BaseSettings, SettingsConfigDict

#configuring all environment variables using pydantic class
class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file=".env")
           
    database_hostname : str
    database_port : str
    database_password : str
    database_name : str    
    database_username : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int

    

    class Config:
        env_file = ".env"
    

settings = Settings()