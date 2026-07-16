"""Schemas da API web (FastAPI).

Modelos de entrada/saída da API que expõe o grafo do agente
(`app/web/main.py`). Não redefinem regra de negócio já aplicada pelo nó
`validar_entrada` — apenas evitam payloads absurdos antes de chegar ao
grafo.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class PerguntaRequest(BaseModel):
    """Corpo da requisição de POST /api/analisar."""

    pergunta: str = Field(..., min_length=1, max_length=1000)


class AnaliseResponse(BaseModel):
    """Resposta de POST /api/analisar, com os campos relevantes do estado
    final do grafo."""

    cenario_identificado: str | None = None
    resposta_estruturada: dict | None = None
    alertas: list[str] = Field(default_factory=list)
