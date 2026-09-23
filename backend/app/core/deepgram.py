import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.core.config import load_local_env


load_local_env()


class DeepgramVoice:
    """Deepgram Aura TTS client with simple key rotation and browser fallback."""

    def __init__(self) -> None:
        configured = os.getenv("DEEPGRAM_API_KEYS", os.getenv("DEEPGRAM_API_KEY", ""))
        self.keys = [key.strip() for key in configured.split(",") if key.strip()]
        self.model = os.getenv("DEEPGRAM_TTS_MODEL", "aura-2-thalia-en")
        self._key_index = 0

    @property
    def enabled(self) -> bool:
        return bool(self.keys)

    def synthesize(self, text: str) -> bytes:
        if not self.keys:
            raise RuntimeError("Deepgram is not configured; use browser speech synthesis.")
        payload = text[:4000].encode("utf-8")
        for _ in range(len(self.keys)):
            key = self.keys[self._key_index % len(self.keys)]
            self._key_index = (self._key_index + 1) % len(self.keys)
            request = Request(
                "https://api.deepgram.com/v1/speak?encoding=mp3&model=" + self.model,
                data=(b'{"text":' + _json_string(payload) + b"}"),
                headers={"Authorization": f"Token {key}", "Content-Type": "application/json"},
                method="POST",
            )
            try:
                with urlopen(request, timeout=20) as response:
                    audio = response.read()
                if audio:
                    return audio
            except (HTTPError, URLError, TimeoutError):
                continue
        raise RuntimeError("All configured Deepgram keys failed; use browser speech synthesis.")


def _json_string(value: bytes) -> bytes:
    import json

    return json.dumps(value.decode("utf-8")).encode("utf-8")


deepgram = DeepgramVoice()