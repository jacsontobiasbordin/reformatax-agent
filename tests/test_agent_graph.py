import pytest

from app.agent.graph import build_graph


def _estado_inicial(pergunta: str) -> dict:
    return {
        "pergunta_usuario": pergunta,
        "cenario_identificado": None,
        "dados_base_local": None,
        "resposta_estruturada": None,
        "alertas": [],
    }


@pytest.fixture(scope="module")
def grafo():
    return build_graph()


@pytest.mark.parametrize(
    ("pergunta", "cenario_esperado"),
    [
        ("Como funciona o cadastro de produtos com NCM?", "cadastro_produtos"),
        ("Como emitir uma nota fiscal (NF-e)?", "emissao_nota_fiscal"),
        ("Como é feito o cálculo do IBS e da CBS?", "calculo_impostos"),
    ],
)
def test_pergunta_valida_identifica_cenario_e_consulta_base(
    grafo, pergunta, cenario_esperado
):
    resultado = grafo.invoke(_estado_inicial(pergunta))

    assert resultado["cenario_identificado"] == cenario_esperado
    assert resultado["dados_base_local"] is not None
    assert resultado["dados_base_local"]["nome"]


def test_pergunta_vazia_retorna_resposta_de_validacao(grafo):
    resultado = grafo.invoke(_estado_inicial("   "))

    assert resultado["dados_base_local"] is None
    assert resultado["resposta_estruturada"] is not None
    assert "pergunta" in resultado["resposta_estruturada"]["mensagem"].lower()


def test_pergunta_fora_de_escopo_retorna_resposta_amigavel(grafo):
    resultado = grafo.invoke(_estado_inicial("qual a previsão do tempo hoje?"))

    assert resultado["cenario_identificado"] == "fora_de_escopo"
    assert resultado["dados_base_local"] is None
    assert resultado["resposta_estruturada"] is not None
