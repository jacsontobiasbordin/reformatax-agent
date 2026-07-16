"""Estado compartilhado do grafo do agente.

Define o `AgentState`, dicionário tipado que trafega entre os nós do grafo
LangGraph (`app/agent/graph.py`), carregando a pergunta do usuário, o
resultado da identificação de cenário, os dados consultados na base local
e a resposta estruturada final.
"""

from __future__ import annotations

from typing import Optional

from typing_extensions import TypedDict


class AgentState(TypedDict):
    """Estado compartilhado entre os nós do grafo.

    Campos:
        pergunta_usuario: Pergunta original informada pelo usuário.
        cenario_identificado: Um de "cadastro_produtos",
            "emissao_nota_fiscal", "calculo_impostos" ou
            "fora_de_escopo", definido pelo nó identificar_cenario.
            None antes desse nó ser executado.
        dados_base_local: Dados do cenário consultados em
            app.tools.local_kb, populados pelo nó consultar_base_local.
            None enquanto o cenário não foi consultado.
        resposta_estruturada: Resposta final montada para o usuário (por
            um nó de erro/fora de escopo nesta etapa, ou pelo nó
            gerar_analise em um prompt futuro). None enquanto não houver
            resposta.
        alertas: Lista de mensagens de validação/erro acumuladas ao longo
            do fluxo (ex.: pergunta vazia, pergunta muito longa, falha ao
            consultar a base local).
        tentativas_geracao: Quantas vezes o nó gerar_analise já foi
            executado para a pergunta atual. Controla o número de retries
            permitidos antes do fluxo desistir e cair no nó de fallback
            (ver MAX_TENTATIVAS_GERACAO em app/agent/nodes.py). Deve ser
            iniciado em 0 ao montar o estado de entrada do grafo
            (`.invoke({...})`); o código também trata a ausência dessa
            chave como 0 na primeira execução.
    """

    pergunta_usuario: str
    cenario_identificado: Optional[str]
    dados_base_local: Optional[dict]
    resposta_estruturada: Optional[dict]
    alertas: list[str]
    tentativas_geracao: int
