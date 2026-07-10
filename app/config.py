"""Configurações do ReformaTax Agent.

Este módulo apenas carrega variáveis de ambiente (via .env) necessárias para
acessar o modelo Gemini. Não faz nenhuma chamada de rede nem instancia
clientes do Gemini — isso será feito pelo nó de geração do agente,
implementado em um prompt futuro (Prompt 06).
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    google_api_key: str
    gemini_model: str = "gemini-3-flash"
    app_env: str = "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()
