from google import genai
from google.genai import types
from .base import BaseLLM


class GeminiProvider(BaseLLM):
    def __init__(self, model: str, temperature: float = 0.3, max_tokens: int = 4000, api_key: str = ""):
        super().__init__(model, temperature, max_tokens)
        self._client = genai.Client(api_key=api_key)

    def _call(self, prompt: str, system: str = "") -> str:
        config = types.GenerateContentConfig(
            system_instruction=system or None,
            temperature=self.temperature,
            max_output_tokens=self.max_tokens,
        )
        response = self._client.models.generate_content(
            model=self.model,
            config=config,
            contents=prompt,
        )
        return response.text
