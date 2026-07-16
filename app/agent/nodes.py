"""Nós do grafo do agente.

A identificação de cenário usa uma heurística simples por palavras-chave
(sem LLM), e as respostas de erro/fora de escopo são montadas com texto
fixo. O único nó que chama um LLM é `gerar_analise`, sempre através de
`app.llm.factory.get_llm()` — nunca instanciando um client de provedor
diretamente. O nó `validar_resposta` confere se a saída de gerar_analise
está completa, permitindo retry (até MAX_TENTATIVAS_GERACAO vezes) antes
de `responder_erro_geracao` encerrar o fluxo com uma mensagem de fallback.
"""

from __future__ import annotations

import json

from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.prompts import SYSTEM_PROMPT_ANALISE
from app.agent.schemas import AnaliseEstruturada
from app.agent.state import AgentState
from app.llm.factory import get_llm
from app.tools.local_kb import (
    BaseLocalIndisponivelError,
    CenarioNaoEncontradoError,
    consultar_cenario,
)

MENSAGEM_PERGUNTA_VAZIA = "Por favor, informe uma pergunta ou selecione um cenário."
MENSAGEM_PERGUNTA_LONGA = "Sua pergunta é muito longa. Tente resumir em até 500 caracteres."
LIMITE_CARACTERES_PERGUNTA = 500

# Número máximo de vezes que gerar_analise pode ser executado para a mesma
# pergunta antes do fluxo desistir e cair em responder_erro_geracao.
MAX_TENTATIVAS_GERACAO = 2

MENSAGEM_ERRO_GERACAO = (
    "Não foi possível concluir a análise após múltiplas tentativas. Tente "
    "novamente em instantes ou reformule sua pergunta."
)

CAMPOS_ANALISE_ESTRUTURADA = (
    "cenario_analisado",
    "pontos_reforma_relacionados",
    "impactos_tecnicos_erp",
    "pontos_atencao",
    "checklist_tecnico",
)

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


class GeracaoAnaliseError(Exception):
    """Erro interno ao chamar o LLM — usada apenas para log/depuração.

    Nunca propaga para fora do nó gerar_analise: é capturada e convertida
    em uma mensagem amigável em `alertas`.
    """


def _invocar_llm_estruturado(mensagens: list) -> AnaliseEstruturada:
    """Chama o LLM configurado via get_llm() e retorna a análise estruturada.

    Qualquer falha (rede, timeout, formato de resposta inesperado) é
    relançada como GeracaoAnaliseError, preservando a causa original.
    """
    try:
        llm = get_llm()
        llm_estruturado = llm.with_structured_output(AnaliseEstruturada)
        return llm_estruturado.invoke(mensagens)
    except Exception as e:
        raise GeracaoAnaliseError("Falha ao gerar análise via LLM") from e


def gerar_analise(state: AgentState) -> dict:
    """Gera a análise estruturada chamando o LLM configurado via get_llm().

    Incrementa `tentativas_geracao` a cada execução, para permitir que o
    nó validar_resposta decida se ainda cabe um retry (ver
    MAX_TENTATIVAS_GERACAO). Em caso de erro na chamada ao LLM, não deixa
    a exceção propagar: adiciona uma mensagem amigável a `alertas` e
    mantém `resposta_estruturada` como None.
    """
    tentativas_geracao = state.get("tentativas_geracao", 0) + 1

    contexto = json.dumps(state["dados_base_local"], indent=2, ensure_ascii=False)
    mensagens = [
        SystemMessage(content=SYSTEM_PROMPT_ANALISE),
        HumanMessage(
            content=(
                f"Pergunta do usuário:\n{state['pergunta_usuario']}\n\n"
                f"Contexto recuperado da base de conhecimento local:\n{contexto}"
            )
        ),
    ]

    try:
        resultado = _invocar_llm_estruturado(mensagens)
        return {
            "resposta_estruturada": resultado.model_dump(),
            "tentativas_geracao": tentativas_geracao,
        }
    except GeracaoAnaliseError:
        return {
            "alertas": [
                *state.get("alertas", []),
                "Não foi possível gerar a análise no momento. "
                "Tente novamente em instantes.",
            ],
            "tentativas_geracao": tentativas_geracao,
        }


def _resposta_e_valida(resposta: dict | None) -> bool:
    """Verifica se a resposta estruturada tem os 5 blocos preenchidos.

    Retorna True somente se `resposta` não for None e todos os campos de
    CAMPOS_ANALISE_ESTRUTURADA estiverem presentes e não vazios (strings
    não em branco, listas com pelo menos 1 item).
    """
    if resposta is None:
        return False

    for campo in CAMPOS_ANALISE_ESTRUTURADA:
        valor = resposta.get(campo)
        if valor is None:
            return False
        if isinstance(valor, str) and not valor.strip():
            return False
        if isinstance(valor, list) and len(valor) == 0:
            return False

    return True


def validar_resposta(state: AgentState) -> dict:
    """Verifica se a resposta gerada por gerar_analise está completa.

    Não altera o estado quando a resposta é válida — este nó existe para
    alimentar a decisão de roteamento do grafo (retry vs. fim vs.
    fallback), feita em app/agent/graph.py.
    """
    if _resposta_e_valida(state.get("resposta_estruturada")):
        return {}

    return {
        "alertas": [
            *state.get("alertas", []),
            "A resposta gerada pelo LLM veio incompleta ou em formato "
            "inesperado.",
        ]
    }


def responder_erro_geracao(state: AgentState) -> dict:
    """Monta uma resposta de fallback após esgotar as tentativas de geração.

    Preserva os alertas já acumulados, para fins de diagnóstico.
    """
    return {
        "resposta_estruturada": {"mensagem": MENSAGEM_ERRO_GERACAO},
        "alertas": state.get("alertas", []),
    }
