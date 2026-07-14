from pathlib import Path

import pytest

from app.tools import local_kb
from app.tools.local_kb import (
    CENARIOS_VALIDOS,
    BaseLocalIndisponivelError,
    CenarioNaoEncontradoError,
    consultar_cenario,
    listar_cenarios_disponiveis,
)

CHAVES_ESPERADAS = {
    "nome",
    "resumo",
    "pontos_reforma_relacionados",
    "impactos_tecnicos_erp",
    "pontos_atencao",
    "checklist_tecnico",
}


@pytest.mark.parametrize("cenario", CENARIOS_VALIDOS)
def test_consultar_cenario_retorna_chaves_esperadas(cenario):
    dados = consultar_cenario(cenario)

    assert isinstance(dados, dict)
    assert CHAVES_ESPERADAS.issubset(dados.keys())


def test_consultar_cenario_invalido_lanca_erro():
    with pytest.raises(CenarioNaoEncontradoError):
        consultar_cenario("cenario_invalido")


def test_carregar_base_arquivo_inexistente(monkeypatch):
    local_kb.carregar_base.cache_clear()
    monkeypatch.setattr(
        local_kb,
        "_CAMINHO_BASE_LOCAL",
        Path("caminho/que/nao/existe/reforma_tributaria_erp.json"),
    )

    with pytest.raises(BaseLocalIndisponivelError):
        local_kb.carregar_base()

    local_kb.carregar_base.cache_clear()


def test_listar_cenarios_disponiveis():
    assert listar_cenarios_disponiveis() == list(CENARIOS_VALIDOS)
