import requests

from src.config import Settings
from src.logger import get_logger

logger = get_logger(__name__)

BASE_URL = "https://api.z-api.io"
REQUEST_TIMEOUT_SECONDS = 30


class ZapiClient:
    def __init__(self, settings: Settings):
        self._send_text_url = (
            f"{BASE_URL}/instances/{settings.zapi_instance_id}"
            f"/token/{settings.zapi_token}/send-text"
        )
        self._headers = {
            "Client-Token": settings.zapi_client_token,
            "Content-Type": "application/json",
        }

    def send_text(self, phone: str, message: str) -> str | None:
        response = requests.post(
            self._send_text_url,
            json={"phone": phone, "message": message},
            headers=self._headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
        message_id = payload.get("messageId") or payload.get("id")
        logger.info(
            "Mensagem enviada para %s (messageId=%s)", phone, message_id
        )
        return message_id
