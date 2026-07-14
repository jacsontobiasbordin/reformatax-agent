"""Ferramenta de consulta à base de conhecimento local.

Lê e consulta o arquivo `data/reforma_tributaria_erp.json`, que contém os
três cenários de impacto da Reforma Tributária em sistemas ERP. Este módulo
é 100% determinístico — não faz nenhuma chamada a LLM. Será usado pelo nó
"consultar_base_local" do grafo LangGraph, implementado em um prompt futuro.
"""

import json
from functools import lru_cache
from pathlib import Path

CENARIOS_VALIDOS = (
    "cadastro_produtos",
    "emissao_nota_fiscal",
    "calculo_impostos",
)

_CAMINHO_BASE_LOCAL = (
    Path(__file__).resolve().parents[2] / "data" / "reforma_tributaria_erp.json"
)


class CenarioNaoEncontradoError(Exception):
    """Lançada quando o cenário solicitado não existe na base local."""


class BaseLocalIndisponivelError(Exception):
    """Lançada quando o arquivo da base local não pode ser lido ou parseado."""


@lru_cache
def carregar_base() -> dict:
    """Carrega e cacheia o conteúdo de data/reforma_tributaria_erp.json.

    O caminho do arquivo é fixo e relativo à raiz do projeto — não aceita
    caminho vindo de fora da função, para evitar leitura de arquivos fora
    da pasta `data/`.
    """
    try:
        with _CAMINHO_BASE_LOCAL.open(encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError as e:
        raise BaseLocalIndisponivelError(
            f"Arquivo da base local não encontrado em: {_CAMINHO_BASE_LOCAL}"
        ) from e
    except json.JSONDecodeError as e:
        raise BaseLocalIndisponivelError(
            f"Arquivo da base local contém JSON inválido: {_CAMINHO_BASE_LOCAL}"
        ) from e


def consultar_cenario(cenario: str) -> dict:
    """Retorna os dados do cenário solicitado a partir da base local.

    Levanta `CenarioNaoEncontradoError` se `cenario` não for um dos
    cenários válidos, ou se a chave não existir dentro do JSON carregado.
    """
    if cenario not in CENARIOS_VALIDOS:
        raise CenarioNaoEncontradoError(
            f"Cenário '{cenario}' não encontrado. "
            f"Cenários válidos: {', '.join(CENARIOS_VALIDOS)}"
        )

    base = carregar_base()
    try:
        return base["cenarios"][cenario]
    except KeyError as e:
        raise CenarioNaoEncontradoError(
            f"Cenário '{cenario}' não encontrado na base local. "
            f"Cenários válidos: {', '.join(CENARIOS_VALIDOS)}"
        ) from e


def listar_cenarios_disponiveis() -> list[str]:
    """Retorna a lista dos cenários suportados pela base local."""
    return list(CENARIOS_VALIDOS)
