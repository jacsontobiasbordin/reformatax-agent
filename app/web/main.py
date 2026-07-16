"""API web (FastAPI) que expõe o grafo do agente.

Camada de apresentação apenas: não altera a lógica do grafo, dos nós ou do
LLM (implementados em `app/agent`). O acesso ao LLM continua acontecendo
somente no backend, através de `app.llm.factory.get_llm()` — nenhuma chave
de API é exposta ao front-end estático servido por este módulo.
"""

from __future__ import annotations

import logging
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from langgraph.graph.state import CompiledStateGraph

from app.agent.graph import build_graph
from app.tools.local_kb import listar_cenarios_disponiveis
from app.web.schemas import AnaliseResponse, PerguntaRequest

logger = logging.getLogger(__name__)

app = FastAPI(title="ReformaTax Agent")


@lru_cache
def get_graph() -> CompiledStateGraph:
    """Constrói o grafo do agente uma única vez e reutiliza a instância."""
    return build_graph()


@app.get("/api/cenarios")
def listar_cenarios() -> list[str]:
    """Lista os cenários suportados, para popular a interface web."""
    return listar_cenarios_disponiveis()


@app.post("/api/analisar", response_model=AnaliseResponse)
def analisar(payload: PerguntaRequest) -> AnaliseResponse:
    """Executa o grafo completo para a pergunta informada."""
    estado_inicial = {
        "pergunta_usuario": payload.pergunta,
        "cenario_identificado": None,
        "dados_base_local": None,
        "resposta_estruturada": None,
        "alertas": [],
        "tentativas_geracao": 0,
    }

    try:
        resultado = get_graph().invoke(estado_inicial)
    except Exception:
        logger.exception("Falha inesperada ao executar o grafo do agente")
        raise HTTPException(
            status_code=500,
            detail="Não foi possível processar sua pergunta no momento. "
            "Tente novamente em instantes.",
        ) from None

    return AnaliseResponse(
        cenario_identificado=resultado.get("cenario_identificado"),
        resposta_estruturada=resultado.get("resposta_estruturada"),
        alertas=resultado.get("alertas", []),
    )


# Servida por último: qualquer rota /api/* acima tem precedência sobre os
# arquivos estáticos.
app.mount("/", StaticFiles(directory="app/web/static", html=True), name="static")
