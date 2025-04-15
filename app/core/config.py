from dotenv import load_dotenv
import os
import logging

# Setup basic logger
logger = logging.getLogger(__name__)

try:
    load_dotenv()

    class Settings:
        DATABASE_URL = os.getenv("DATABASE_URL")
        JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
        JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
        ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    settings = Settings()
    logger.info("Configuration loaded successfully.")

except Exception as e:
    logger.error(f"Error loading configuration: {e}")
    raise 
