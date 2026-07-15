"""Nós determinísticos do grafo do agente.

Nenhuma função deste módulo chama um LLM — a identificação de cenário usa
uma heurística simples por palavras-chave, e as respostas de erro/fora de
escopo são montadas com texto fixo. O nó que efetivamente chama o LLM
(gerar_analise, via app.llm.factory.get_llm()) será adicionado em um prompt
futuro.
"""

from __future__ import annotations

from app.agent.state import AgentState
from app.tools.local_kb import (
    BaseLocalIndisponivelError,
    CenarioNaoEncontradoError,
    consultar_cenario,
)

MENSAGEM_PERGUNTA_VAZIA = "Por favor, informe uma pergunta ou selecione um cenário."
MENSAGEM_PERGUNTA_LONGA = "Sua pergunta é muito longa. Tente resumir em até 500 caracteres."
LIMITE_CARACTERES_PERGUNTA = 500

# Heurística simples por palavras-chave (case-insensitive). Não usa LLM.
# Uma versão futura poderia usar o LLM para desambiguar casos que não
# batem com nenhuma palavra-chave, mas isso está fora do escopo desta etapa.
PALAVRAS_CHAVE_POR_CENARIO: dict[str, list[str]] = {
    "cadastro_produtos": [
        "cadastro",
        "produto",
        "ncm",
        "classificação tributária",
        "cclasstrib",
    ],
    "emissao_nota_fiscal": [
        "nota fiscal",
        "nf-e",
        "nfe",
        "nfc-e",
        "emissão",
        "danfe",
    ],
    "calculo_impostos": [
        "cálculo",
        "calculo",
        "imposto",
        "ibs",
        "cbs",
        "tributo",
        "alíquota",
        "aliquota",
    ],
}

CENARIO_FORA_DE_ESCOPO = "fora_de_escopo"


def validar_entrada(state: AgentState) -> dict:
    """Normaliza a pergunta e sinaliza problemas de validação em `alertas`.

    Não lança exceção — apenas acumula mensagens em `alertas`. A decisão
    do que fazer com esses alertas é da aresta condicional do grafo.
    """
    pergunta = state["pergunta_usuario"].strip()
    alertas: list[str] = []

    if not pergunta:
        alertas.append(MENSAGEM_PERGUNTA_VAZIA)
    elif len(pergunta) > LIMITE_CARACTERES_PERGUNTA:
        alertas.append(MENSAGEM_PERGUNTA_LONGA)

    return {"pergunta_usuario": pergunta, "alertas": alertas}


def identificar_cenario(state: AgentState) -> dict:
    """Identifica o cenário da pergunta por palavras-chave, sem LLM."""
    pergunta = state["pergunta_usuario"].lower()

    for cenario, palavras_chave in PALAVRAS_CHAVE_POR_CENARIO.items():
        if any(palavra in pergunta for palavra in palavras_chave):
            return {"cenario_identificado": cenario}

    return {"cenario_identificado": CENARIO_FORA_DE_ESCOPO}


def consultar_base_local(state: AgentState) -> dict:
    """Consulta a base local para o cenário identificado.

    Captura falhas da ferramenta (cenário inexistente na base ou base
    indisponível) e as transforma em mensagens amigáveis em `alertas`, sem
    deixar a exceção propagar para fora do nó.
    """
    try:
        dados = consultar_cenario(state["cenario_identificado"])
        return {"dados_base_local": dados}
    except (CenarioNaoEncontradoError, BaseLocalIndisponivelError) as e:
        return {"alertas": [*state.get("alertas", []), str(e)]}


def responder_entrada_invalida(state: AgentState) -> dict:
    """Monta uma resposta simplificada para pergunta inválida."""
    return {
        "resposta_estruturada": {
            "mensagem": " ".join(state["alertas"]),
        }
    }


def responder_fora_de_escopo(state: AgentState) -> dict:
    """Monta uma resposta simplificada para pergunta fora dos cenários suportados."""
    return {
        "resposta_estruturada": {
            "mensagem": (
                "Sua pergunta não se encaixa em nenhum dos cenários "
                "suportados no momento (cadastro de produtos, emissão de "
                "nota fiscal ou cálculo de impostos). Tente reformular a "
                "pergunta mencionando um desses temas."
            ),
        }
    }
