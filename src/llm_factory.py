"""Return a BaseLLM instance based on config.yaml."""
import yaml
from pathlib import Path
from src.providers.base import BaseLLM

_CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"


def get_llm() -> BaseLLM:
    with open(_CONFIG_PATH, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    lc = cfg.get("llm", {})
    provider = lc.get("provider", "google")
    model = lc.get("model", "gemini-2.5-flash")
    temperature = float(lc.get("temperature", 0.3))
    max_tokens = int(lc.get("max_tokens", 4000))

    if provider == "google":
        from src.providers.gemini import GeminiProvider
        from config import GEMINI_API_KEY
        return GeminiProvider(model=model, temperature=temperature, max_tokens=max_tokens, api_key=GEMINI_API_KEY)

    if provider == "openai":
        from src.providers.openai_provider import OpenAIProvider
        from config import OPENAI_API_KEY
        return OpenAIProvider(model=model, temperature=temperature, max_tokens=max_tokens, api_key=OPENAI_API_KEY)

    raise ValueError(f"Unknown provider '{provider}'. Supported: google, openai")
