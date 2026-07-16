from unittest.mock import MagicMock, patch

import pytest

from app.agent.graph import build_graph
from app.agent.nodes import MAX_TENTATIVAS_GERACAO, MENSAGEM_ERRO_GERACAO
from app.agent.schemas import AnaliseEstruturada

ANALISE_FAKE = AnaliseEstruturada(
    cenario_analisado="Cadastro de produtos e classificação tributária.",
    pontos_reforma_relacionados=["Ponto de reforma de exemplo."],
    impactos_tecnicos_erp=["Impacto técnico de exemplo."],
    pontos_atencao=["Validar com a área fiscal."],
    checklist_tecnico=["Item de checklist de exemplo."],
)

ANALISE_INVALIDA = AnaliseEstruturada(
    cenario_analisado="Cadastro de produtos e classificação tributária.",
    pontos_reforma_relacionados=[],
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
        "tentativas_geracao": 0,
    }


def _mock_llm_com_respostas(*respostas: AnaliseEstruturada) -> MagicMock:
    llm_estruturado = MagicMock()
    llm_estruturado.invoke.side_effect = list(respostas)

    llm = MagicMock()
    llm.with_structured_output.return_value = llm_estruturado
    return llm


def test_resposta_valida_na_primeira_tentativa_encerra_com_sucesso():
    with patch(
        "app.agent.nodes.get_llm",
        return_value=_mock_llm_com_respostas(ANALISE_FAKE),
    ):
        grafo = build_graph()
        resultado = grafo.invoke(
            _estado_inicial("Como funciona o cadastro de produtos com NCM?")
        )

    assert resultado["tentativas_geracao"] == 1
    assert BLOCOS_ESPERADOS.issubset(resultado["resposta_estruturada"].keys())
    assert resultado["resposta_estruturada"] == ANALISE_FAKE.model_dump()


def test_resposta_invalida_depois_valida_faz_retry_e_encerra_com_sucesso():
    with patch(
        "app.agent.nodes.get_llm",
        return_value=_mock_llm_com_respostas(ANALISE_INVALIDA, ANALISE_FAKE),
    ):
        grafo = build_graph()
        resultado = grafo.invoke(
            _estado_inicial("Como funciona o cadastro de produtos com NCM?")
        )

    assert resultado["tentativas_geracao"] == 2
    assert resultado["resposta_estruturada"] == ANALISE_FAKE.model_dump()


def test_resposta_sempre_invalida_esgota_tentativas_e_cai_no_fallback():
    respostas_invalidas = [ANALISE_INVALIDA] * (MAX_TENTATIVAS_GERACAO + 1)

    with patch(
        "app.agent.nodes.get_llm",
        return_value=_mock_llm_com_respostas(*respostas_invalidas),
    ):
        grafo = build_graph()
        resultado = grafo.invoke(
            _estado_inicial("Como funciona o cadastro de produtos com NCM?")
        )

    assert resultado["tentativas_geracao"] == MAX_TENTATIVAS_GERACAO
    assert resultado["resposta_estruturada"] == {"mensagem": MENSAGEM_ERRO_GERACAO}
    assert resultado["alertas"]


def test_grafo_nunca_entra_em_loop_infinito_mesmo_com_llm_sempre_falhando():
    llm = MagicMock()
    llm.with_structured_output.side_effect = RuntimeError("timeout simulado")

    with patch("app.agent.nodes.get_llm", return_value=llm):
        grafo = build_graph()
        resultado = grafo.invoke(
            _estado_inicial("Como funciona o cadastro de produtos com NCM?")
        )

    assert resultado["tentativas_geracao"] == MAX_TENTATIVAS_GERACAO
    assert resultado["resposta_estruturada"] == {"mensagem": MENSAGEM_ERRO_GERACAO}


@pytest.mark.parametrize(
    "resposta_incompleta",
    [
        None,
        {
            "cenario_analisado": "",
            "pontos_reforma_relacionados": ["x"],
            "impactos_tecnicos_erp": ["x"],
            "pontos_atencao": ["x"],
            "checklist_tecnico": ["x"],
        },
        {
            "cenario_analisado": "ok",
            "pontos_reforma_relacionados": [],
            "impactos_tecnicos_erp": ["x"],
            "pontos_atencao": ["x"],
            "checklist_tecnico": ["x"],
        },
    ],
)
def test_resposta_e_valida_rejeita_campos_ausentes_ou_vazios(resposta_incompleta):
    from app.agent.nodes import _resposta_e_valida

    assert _resposta_e_valida(resposta_incompleta) is False


def test_resposta_e_valida_aceita_todos_os_campos_preenchidos():
    from app.agent.nodes import _resposta_e_valida

    assert _resposta_e_valida(ANALISE_FAKE.model_dump()) is True
