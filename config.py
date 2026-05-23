from fastapi import FastAPI, Basesettings

class Settings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    jwt_secret_key: str
    
    class Config:
        env_file = ".env"