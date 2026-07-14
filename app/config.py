"""Configurações do ReformaTax Agent.

Este módulo carrega variáveis de ambiente (via .env) e expõe as
configurações necessárias para os provedores de LLM suportados (Gemini,
Claude e OpenAI). O provedor efetivamente usado em tempo de execução é
selecionado pela variável `LLM_PROVIDER`. Este módulo não instancia nenhum
client de LLM nem faz chamadas de rede — a instanciação é feita pela fábrica
em `app/llm/factory.py`.
"""

from functools import lru_cache
from typing import Literal, Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ProviderName = Literal["gemini", "anthropic", "openai"]

_MISSING_API_KEY_MESSAGES: dict[ProviderName, str] = {
    "gemini": "GOOGLE_API_KEY é obrigatória quando LLM_PROVIDER=gemini",
    "anthropic": "ANTHROPIC_API_KEY é obrigatória quando LLM_PROVIDER=anthropic",
    "openai": "OPENAI_API_KEY é obrigatória quando LLM_PROVIDER=openai",
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_provider: ProviderName = "gemini"

    google_api_key: Optional[str] = None
    gemini_model: str = "gemini-3-flash"

    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-sonnet-5"

    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-5.1"

    app_env: str = "development"

    @model_validator(mode="after")
    def _validate_active_provider_api_key(self) -> "Settings":
        active_provider_keys: dict[ProviderName, Optional[str]] = {
            "gemini": self.google_api_key,
            "anthropic": self.anthropic_api_key,
            "openai": self.openai_api_key,
        }
        if not active_provider_keys[self.llm_provider]:
            raise ValueError(_MISSING_API_KEY_MESSAGES[self.llm_provider])
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
