"""Abstract base for all LLM providers."""
import time
from abc import ABC, abstractmethod


class BaseLLM(ABC):
    def __init__(self, model: str, temperature: float = 0.3, max_tokens: int = 4000):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    @abstractmethod
    def _call(self, prompt: str, system: str = "") -> str:
        pass

    def generate(self, prompt: str, system: str = "") -> str:
        """Call with one automatic retry on failure."""
        provider_name = self.__class__.__name__.replace("Provider", "")
        try:
            return self._call(prompt, system)
        except Exception:
            try:
                time.sleep(1)
                return self._call(prompt, system)
            except Exception as e:
                raise RuntimeError(
                    f"Provider: {provider_name}\nModel: {self.model}\nError: {e}"
                ) from e
