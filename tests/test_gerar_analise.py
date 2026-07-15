from unittest.mock import MagicMock, patch

import pytest

from app.agent.graph import build_graph
from app.agent.nodes import gerar_analise
from app.agent.schemas import AnaliseEstruturada

ANALISE_FAKE = AnaliseEstruturada(
    cenario_analisado="Cadastro de produtos e classificação tributária.",
    pontos_reforma_relacionados=["Ponto de reforma de exemplo."],
    impactos_tecnicos_erp=["Impacto técnico de exemplo."],
    pontos_atencao=["Validar com a área fiscal."],
    checklist_tecnico=["Item de checklist de exemplo."],
)

BLOCOS_ESPERADOS = {
    "cenario_analisado",
    "pontos_reforma_relacionados",
    "impactos_tecnicos_erp",
    "pontos_atencao",
    "checklist_tecnico",
}


def _estado_inicial(pergunta: str) -> dict:
    return {
        "pergunta_usuario": pergunta,
        "cenario_identificado": None,
        "dados_base_local": None,
        "resposta_estruturada": None,
        "alertas": [],
    }


def _mock_llm_com_resposta(resposta: AnaliseEstruturada) -> MagicMock:
    llm_estruturado = MagicMock()
    llm_estruturado.invoke.return_value = resposta

    llm = MagicMock()
    llm.with_structured_output.return_value = llm_estruturado
    return llm


@pytest.mark.parametrize(
    ("pergunta", "cenario_esperado"),
    [
        ("Como funciona o cadastro de produtos com NCM?", "cadastro_produtos"),
        ("Como emitir uma nota fiscal (NF-e)?", "emissao_nota_fiscal"),
        ("Como é feito o cálculo do IBS e da CBS?", "calculo_impostos"),
    ],
)
def test_grafo_completo_com_llm_mockado(pergunta, cenario_esperado):
    with patch(
        "app.agent.nodes.get_llm", return_value=_mock_llm_com_resposta(ANALISE_FAKE)
    ):
        grafo = build_graph()
        resultado = grafo.invoke(_estado_inicial(pergunta))

    assert resultado["cenario_identificado"] == cenario_esperado
    assert resultado["dados_base_local"] is not None
    assert BLOCOS_ESPERADOS.issubset(resultado["resposta_estruturada"].keys())
    assert resultado["resposta_estruturada"] == ANALISE_FAKE.model_dump()


def test_gerar_analise_erro_no_llm_nao_propaga_excecao():
    llm = MagicMock()
    llm.with_structured_output.side_effect = RuntimeError("timeout simulado")

    state = _estado_inicial("Como funciona o cadastro de produtos?")
    state["cenario_identificado"] = "cadastro_produtos"
    state["dados_base_local"] = {"nome": "Cadastro de produtos"}

    with patch("app.agent.nodes.get_llm", return_value=llm):
        resultado = gerar_analise(state)

    # O nó não deve lançar exceção nem popular resposta_estruturada — apenas
    # acumular um alerta amigável.
    assert "resposta_estruturada" not in resultado
    assert resultado["alertas"]
    assert "análise" in resultado["alertas"][-1].lower()


def test_grafo_completo_erro_no_llm_mantem_resposta_estruturada_none():
    llm = MagicMock()
    llm.with_structured_output.side_effect = RuntimeError("timeout simulado")

    with patch("app.agent.nodes.get_llm", return_value=llm):
        grafo = build_graph()
        resultado = grafo.invoke(
            _estado_inicial("Como funciona o cadastro de produtos com NCM?")
        )

    assert resultado["resposta_estruturada"] is None
    assert resultado["alertas"]
