"""Fábrica de LLM multi-provedor.

Este é o único ponto do projeto que deve conhecer as classes específicas de
cada provedor (ChatGoogleGenerativeAI, ChatAnthropic, ChatOpenAI). Qualquer
outro módulo — nós do agente, grafo do LangGraph, etc. — deve chamar apenas
`get_llm()` e programar contra a interface genérica `BaseChatModel` do
LangChain, nunca importar um client de provedor diretamente.

`get_llm()` apenas instancia o client localmente; não faz nenhuma chamada de
rede nem invoca o modelo.
"""

from langchain_core.language_models.chat_models import BaseChatModel

from app.config import get_settings


def get_llm() -> BaseChatModel:
    settings = get_settings()

    if settings.llm_provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
        )

    if settings.llm_provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(
            model=settings.anthropic_model,
            api_key=settings.anthropic_api_key,
        )

    if settings.llm_provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
        )

    raise ValueError(f"Provedor de LLM não suportado: {settings.llm_provider!r}")
