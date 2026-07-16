from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.agent.schemas import AnaliseEstruturada
from app.web.main import app

ANALISE_FAKE = AnaliseEstruturada(
    cenario_analisado="Cadastro de produtos e classificação tributária.",
    pontos_reforma_relacionados=["Ponto de reforma de exemplo."],
    impactos_tecnicos_erp=["Impacto técnico de exemplo."],
    pontos_atencao=["Validar com a área fiscal."],
    checklist_tecnico=["Item de checklist de exemplo."],
)


def _mock_llm_com_resposta(resposta: AnaliseEstruturada) -> MagicMock:
    llm_estruturado = MagicMock()
    llm_estruturado.invoke.return_value = resposta

    llm = MagicMock()
    llm.with_structured_output.return_value = llm_estruturado
    return llm


client = TestClient(app)


def test_get_raiz_retorna_index_com_nome_do_projeto():
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert "ReformaTax" in resposta.text


def test_get_api_cenarios_retorna_os_tres_cenarios_esperados():
    resposta = client.get("/api/cenarios")

    assert resposta.status_code == 200
    assert set(resposta.json()) == {
        "cadastro_produtos",
        "emissao_nota_fiscal",
        "calculo_impostos",
    }


def test_post_analisar_com_pergunta_valida_retorna_resposta_completa():
    with patch(
        "app.agent.nodes.get_llm", return_value=_mock_llm_com_resposta(ANALISE_FAKE)
    ):
        resposta = client.post(
            "/api/analisar",
            json={"pergunta": "Como funciona o cadastro de produtos com NCM?"},
        )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["cenario_identificado"] == "cadastro_produtos"
    assert corpo["resposta_estruturada"] == ANALISE_FAKE.model_dump()


def test_post_analisar_com_pergunta_vazia_retorna_alerta_de_validacao():
    # Só espaços: passa pela validação leve do schema (min_length=1), mas é
    # tratada como vazia pelo nó validar_entrada do grafo.
    resposta = client.post("/api/analisar", json={"pergunta": "   "})

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["alertas"]
    assert corpo["resposta_estruturada"] is not None
    assert "mensagem" in corpo["resposta_estruturada"]


def test_post_analisar_com_pergunta_realmente_vazia_e_rejeitada_pelo_schema():
    resposta = client.post("/api/analisar", json={"pergunta": ""})

    assert resposta.status_code == 422


def test_post_analisar_com_pergunta_fora_de_escopo_retorna_mensagem_amigavel():
    resposta = client.post(
        "/api/analisar", json={"pergunta": "qual a previsão do tempo hoje?"}
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["cenario_identificado"] == "fora_de_escopo"
    assert corpo["resposta_estruturada"] is not None
    assert "mensagem" in corpo["resposta_estruturada"]
