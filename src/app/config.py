from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings
import yaml
import os

class Settings(BaseSettings):
    app_name: str
    version: str
    host: str
    port: int
    enviroment: str
    debug: bool

    redis_host: str
    redis_port: int

    @classmethod
    def from_yaml(cls) -> 'Settings':
        env = os.getenv("ENVIROMENT", "local")
        config_path = Path(__file__).parent.parent / "config" / f"{env}.yaml"
        
        if not config_path.exists():
            raise RuntimeError(f"Config file {config_path} not found")

        with open(config_path, "r") as f:
            data = yaml.safe_load(f)

        return cls(**data)

@lru_cache
def get_settings() -> Settings:
    return Settings.from_yaml()