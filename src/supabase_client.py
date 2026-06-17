from enum import Enum

from supabase import Client, create_client

from src.config import Settings
from src.logger import get_logger

logger = get_logger(__name__)

CONTACTS_TABLE = "contacts"
MESSAGE_LOGS_TABLE = "message_logs"


class MessageStatus(str, Enum):
    SENT = "sent"
    FAILED = "failed"


class SupabaseRepository:
    def __init__(self, settings: Settings):
        self._client: Client = create_client(
            settings.supabase_url, settings.supabase_key
        )

    def fetch_contacts(self, limit: int) -> list[dict]:
        response = (
            self._client.table(CONTACTS_TABLE)
            .select("id, name, phone")
            .limit(limit)
            .execute()
        )
        contacts = response.data or []
        logger.info("Buscados %d contato(s) no Supabase", len(contacts))
        return contacts

    def log_message(
        self,
        contact_id: str,
        message: str,
        status: MessageStatus,
        zapi_message_id: str | None,
    ) -> None:
        self._client.table(MESSAGE_LOGS_TABLE).insert(
            {
                "contact_id": contact_id,
                "message": message,
                "status": status.value,
                "zapi_message_id": zapi_message_id,
            }
        ).execute()
        logger.info(
            "Registrado envio do contato %s com status '%s'",
            contact_id,
            status.value,
        )
