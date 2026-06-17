import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    supabase_url: str
    supabase_key: str
    zapi_instance_id: str
    zapi_token: str
    zapi_client_token: str


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Variável de ambiente obrigatória ausente: {name}")
    return value


def load_settings() -> Settings:
    project_id = _require("SUPABASE_PROJECT_ID")
    return Settings(
        supabase_url=f"https://{project_id}.supabase.co",
        supabase_key=_require("SUPABASE_KEY"),
        zapi_instance_id=_require("ZAPI_INSTANCE_ID"),
        zapi_token=_require("ZAPI_TOKEN"),
        zapi_client_token=_require("ZAPI_CLIENT_TOKEN"),
    )
