import json
import os
import time
from dataclasses import dataclass
from typing import Optional

try:
    import openai
except ImportError:  # pragma: no cover - environment might not have openai
    openai = None


def _call_o3(prompt: str, model: str = "o3") -> str:
    """Call an external LLM named 'o3' to generate text.

    This helper supports both the old (<1.0) and new (>=1.0) versions of the
    ``openai`` package. If ``openai`` is unavailable, a stubbed response is
    returned. The function is deliberately simple, as tests may run in an
    environment without network access or valid credentials.
    """

    if openai is None:
        # Fallback stub if the OpenAI package is not installed.
        return f"[o3 stubbed response to: {prompt}]"

    try:
        # New 1.x style client
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except AttributeError:
        # Old 0.x style API
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["choices"][0]["message"]["content"].strip()


@dataclass
class PoetryAgent:
    name: str
    llm_model: str = "o3"

    def generate_poetry(self, prompt: str, style_guide: dict, form: str) -> str:
        """Generate a poem using the configured LLM."""
        full_prompt = (
            f"Compose a {form} in the style of Frederick Turner. "
            f"Theme: {prompt}."
        )
        return _call_o3(full_prompt, model=self.llm_model)

    def interpret_poetry(self, poetry: str) -> str:
        """Create a simple follow-up prompt based on received poetry."""
        words = poetry.split()
        snippet = " ".join(words[:4]) if words else ""
        return f"Respond to '{snippet}'"

    def send_message(self, recipient_id: str, message_type: str, payload: str) -> None:
        msg = {
            "sender_id": self.name,
            "recipient_id": recipient_id,
            "message_type": message_type,
            "payload": payload,
            "timestamp": time.time(),
        }
        filename = f"message_to_{recipient_id}.json"
        with open(filename, "w", encoding="utf-8") as fh:
            json.dump(msg, fh)

    def receive_message(self) -> Optional[dict]:
        filename = f"message_to_{self.name}.json"
        if not os.path.exists(filename):
            return None
        with open(filename, "r", encoding="utf-8") as fh:
            msg = json.load(fh)
        os.remove(filename)
        return msg
