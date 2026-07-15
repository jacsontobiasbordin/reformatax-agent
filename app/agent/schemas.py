"""Schema de saída estruturada da análise gerada pelo LLM.

`AnaliseEstruturada` é usado com `llm.with_structured_output(...)` no nó
`gerar_analise`, garantindo que a resposta do modelo já chegue no formato
dos 5 blocos definidos no escopo do projeto (seção 8 de docs/escopo.md).
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class AnaliseEstruturada(BaseModel):
    """Resposta final estruturada nos 5 blocos exigidos pelo escopo."""

    cenario_analisado: str = Field(
        ...,
        description=(
            "Resumo objetivo, em 1-2 frases, da dúvida ou situação "
            "informada pelo usuário e do cenário identificado."
        ),
    )
    pontos_reforma_relacionados: list[str] = Field(
        ...,
        description=(
            "Conceitos e regras da Reforma Tributária (IBS/CBS), extraídos "
            "do contexto fornecido, que são pertinentes ao cenário "
            "analisado."
        ),
    )
    impactos_tecnicos_erp: list[str] = Field(
        ...,
        description=(
            "Pontos técnicos do sistema ERP que podem exigir revisão em "
            "função da Reforma Tributária, com base no contexto fornecido."
        ),
    )
    pontos_atencao: list[str] = Field(
        ...,
        description=(
            "Itens que precisam de validação com a área fiscal/contábil "
            "ou que exigem cuidado especial antes de qualquer decisão "
            "estrutural no sistema."
        ),
    )
    checklist_tecnico: list[str] = Field(
        ...,
        description=(
            "Lista prática de verificação, com passos objetivos, para o "
            "desenvolvedor ou analista de sistemas validar o cenário no "
            "ERP."
        ),
    )
