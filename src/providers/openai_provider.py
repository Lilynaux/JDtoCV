from openai import OpenAI
from .base import BaseLLM


class OpenAIProvider(BaseLLM):
    def __init__(self, model: str, temperature: float = 0.3, max_tokens: int = 4000, api_key: str = ""):
        super().__init__(model, temperature, max_tokens)
        self._client = OpenAI(api_key=api_key)

    def _call(self, prompt: str, system: str = "") -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content
