from pathlib import Path
from pydantic_settings import BaseSettings


from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):

    # logging settings
    DEBUG: bool
    LOG_LEVEL: str
    LOG_DIR: Path  = Path("logs")


settings = Settings()