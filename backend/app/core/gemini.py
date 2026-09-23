import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class GeminiAssistant:
    """Small REST client with key rotation and a deterministic offline fallback."""

    def __init__(self) -> None:
        configured = os.getenv("GEMINI_API_KEYS", os.getenv("GEMINI_API_KEY", ""))
        self.keys = [key.strip() for key in configured.split(",") if key.strip()]
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        self._key_index = 0

    @property
    def enabled(self) -> bool:
        return bool(self.keys)

    def answer(self, question: str, state: dict, fallback: str) -> tuple[str, str]:
        if not self.keys:
            return fallback, "deterministic_fallback"
        prompt = (
            "You are CAT Operator Companion, an operator-assistance prototype using synthetic data. "
            "Answer briefly and clearly. Never invent service procedures, never claim machine control, "
            "and label estimates as estimates. Use only the supplied live state.\n\n"
            f"LIVE STATE:\n{json.dumps(state, indent=2)}\n\nOPERATOR QUESTION:\n{question}"
        )
        for _ in range(len(self.keys)):
            key = self.keys[self._key_index % len(self.keys)]
            self._key_index = (self._key_index + 1) % len(self.keys)
            try:
                answer = self._request(key, prompt)
                if answer:
                    return answer, "gemini"
            except (HTTPError, URLError, TimeoutError, ValueError):
                continue
        return fallback, "deterministic_fallback"

    def _request(self, key: str, prompt: str) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={key}"
        body = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.2}}
        request = Request(
            url,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=12) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()


gemini = GeminiAssistant()