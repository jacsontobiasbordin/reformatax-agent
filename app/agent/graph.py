"""Grafo do agente (LangGraph).

Nesta etapa, o grafo é 100% determinístico: valida a entrada, identifica o
cenário por palavras-chave e consulta a base local — sem nenhuma chamada a
LLM. O nó `gerar_analise`, que efetivamente chama o LLM configurado via
`app.llm.factory.get_llm()`, será inserido em um prompt futuro entre
`consultar_base_local` e o fim do fluxo (hoje, `consultar_base_local`
aponta diretamente para END).
"""

from __future__ import annotations

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.agent.nodes import (
    CENARIO_FORA_DE_ESCOPO,
    consultar_base_local,
    identificar_cenario,
    responder_entrada_invalida,
    responder_fora_de_escopo,
    validar_entrada,
)
from app.agent.state import AgentState


def _entrada_valida(state: AgentState) -> str:
    if state["alertas"]:
        return "invalida"
    return "valida"


def _cenario_em_escopo(state: AgentState) -> str:
    if state["cenario_identificado"] == CENARIO_FORA_DE_ESCOPO:
        return "fora_de_escopo"
    return "em_escopo"


def build_graph() -> CompiledStateGraph:
    """Monta e compila o grafo do agente, pronto para `.invoke()`."""
    grafo = StateGraph(AgentState)

    grafo.add_node("validar_entrada", validar_entrada)
    grafo.add_node("identificar_cenario", identificar_cenario)
    grafo.add_node("consultar_base_local", consultar_base_local)
    grafo.add_node("responder_entrada_invalida", responder_entrada_invalida)
    grafo.add_node("responder_fora_de_escopo", responder_fora_de_escopo)

    grafo.set_entry_point("validar_entrada")

    grafo.add_conditional_edges(
        "validar_entrada",
        _entrada_valida,
        {
            "invalida": "responder_entrada_invalida",
            "valida": "identificar_cenario",
        },
    )
    grafo.add_conditional_edges(
        "identificar_cenario",
        _cenario_em_escopo,
        {
            "fora_de_escopo": "responder_fora_de_escopo",
            "em_escopo": "consultar_base_local",
        },
    )

    grafo.add_edge("responder_entrada_invalida", END)
    grafo.add_edge("responder_fora_de_escopo", END)
    grafo.add_edge("consultar_base_local", END)

    return grafo.compile()
