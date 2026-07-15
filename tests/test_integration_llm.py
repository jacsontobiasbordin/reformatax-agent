"""Teste de integração real, opcional — NÃO roda por padrão.

Chama o provedor de LLM configurado em LLM_PROVIDER de verdade (Gemini 3
Flash por padrão), gastando tokens reais. Requer uma API key válida no
`.env` local. Ignorado pela suíte padrão (ver `addopts` em pytest.ini) —
para rodar explicitamente:

    pytest -m integration
"""

import pytest

from app.agent.graph import build_graph


@pytest.mark.integration
def test_grafo_completo_com_llm_real():
    grafo = build_graph()
    resultado = grafo.invoke(
        {
            "pergunta_usuario": "Como funciona o cadastro de produtos com NCM?",
            "cenario_identificado": None,
            "dados_base_local": None,
            "resposta_estruturada": None,
            "alertas": [],
        }
    )

    assert resultado["cenario_identificado"] == "cadastro_produtos"
    assert resultado["resposta_estruturada"] is not None
    assert resultado["resposta_estruturada"]["cenario_analisado"]
