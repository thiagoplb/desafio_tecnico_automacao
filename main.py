import sys
import requests
from src.config import load_settings
from src.logger import configure_logging, get_logger
from src.supabase_client import MessageStatus, SupabaseRepository
from src.zapi_client import ZapiClient

logger = get_logger(__name__)

MAX_CONTACTS = 3


def run() -> None:
    configure_logging()
    try:
        settings = load_settings()
        repository = SupabaseRepository(settings)
        zapi_client = ZapiClient(settings)
        contacts = repository.fetch_contacts(MAX_CONTACTS)
    except Exception as error:
        logger.error("Falha ao iniciar a aplicação: %s", error)
        sys.exit(1)

    if not contacts:
        logger.warning("Nenhum contato cadastrado no banco. Nada a enviar.")
        return

    for contact in contacts:
        message = f"Olá, {contact['name']} tudo bem com você?"

        try:
            message_id = zapi_client.send_text(contact["phone"], message)
            status = MessageStatus.SENT
        except requests.RequestException as error:
            logger.error(
                "Falha ao enviar mensagem para %s: %s", contact["phone"], error
            )
            message_id = None
            status = MessageStatus.FAILED

        try:
            repository.log_message(contact["id"], message, status, message_id)
        except Exception as error:
            logger.error(
                "Falha ao registrar envio para %s: %s", contact["phone"], error
            )


if __name__ == "__main__":
    run()
