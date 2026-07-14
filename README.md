# ReformaTax Agent

## Descrição

Assistente de IA que analisa impactos técnicos da Reforma Tributária
brasileira em sistemas ERP.

## Status

🚧 Em desenvolvimento — estrutura inicial do projeto.

## Objetivo do agente

O agente terá como objetivo apoiar times técnicos de ERP a identificar e
compreender os impactos da Reforma Tributária (IBS/CBS) em rotinas e
cadastros do sistema, respondendo a perguntas e apontando pontos de atenção
com base em uma base de conhecimento local.

## Escopo

O agente cobrirá, inicialmente, os seguintes cenários:

1. Cadastro de produtos
2. Emissão de nota fiscal
3. Cálculo de impostos (IBS/CBS)

Mais detalhes em [docs/escopo.md](docs/escopo.md).

## Estrutura de pastas

```
reformatax/
├── app/
│   ├── agent/        # grafo LangGraph (estado, nós, conexões) — futuro
│   ├── llm/           # fábrica de LLM multi-provedor (get_llm())
│   ├── tools/         # ferramentas de consulta à base local — futuro
│   └── web/           # interface web — futuro
├── data/
│   └── reforma_tributaria_erp.json
├── docs/
│   ├── escopo.md
│   ├── prompts.md
│   └── apresentacao/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Como configurar o ambiente

1. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Copie o arquivo de variáveis de ambiente de exemplo e preencha os valores:

   ```bash
   cp .env.example .env
   ```

4. Obtenha uma API key do Gemini no [Google AI Studio](https://aistudio.google.com/app/apikey)
   e preencha a variável `GOOGLE_API_KEY` no arquivo `.env` local (nunca no
   `.env.example`, que é versionado). A variável `GEMINI_MODEL` já vem
   preenchida com o modelo padrão do projeto (`gemini-3-flash`).

## Provedores de LLM suportados

O agente é capaz de rodar com diferentes provedores de LLM — Gemini
(Google), Claude (Anthropic) ou OpenAI —, sem alterar código do grafo ou dos
nós. A troca de provedor é feita inteiramente por variável de ambiente.

- `LLM_PROVIDER` seleciona o provedor ativo: `gemini`, `anthropic` ou
  `openai`.
- Cada provedor tem sua própria seção de variáveis no `.env.example`
  (`GOOGLE_API_KEY`/`GEMINI_MODEL`, `ANTHROPIC_API_KEY`/`ANTHROPIC_MODEL`,
  `OPENAI_API_KEY`/`OPENAI_MODEL`). Apenas as variáveis do provedor
  selecionado em `LLM_PROVIDER` precisam estar preenchidas no `.env` real;
  as demais podem ficar vazias.
- O nome do modelo de cada provedor é configurável através das variáveis
  `GEMINI_MODEL`, `ANTHROPIC_MODEL` e `OPENAI_MODEL`.

Para trocar de provedor, altere `LLM_PROVIDER` no `.env` e preencha a API
key correspondente. Nenhum código do agente precisa ser alterado — todo
acesso ao LLM passa pela fábrica em `app/llm/factory.py`.

O provedor padrão e recomendado para este mini-projeto é `gemini`, com o
modelo `gemini-3-flash`, pelo custo-benefício. Os demais provedores existem
para portabilidade entre ambientes, não como substituição da entrega.

## Ferramenta: consulta à base local

O módulo `app/tools/local_kb.py` lê e consulta o arquivo
`data/reforma_tributaria_erp.json`, que contém os três cenários de impacto
da Reforma Tributária em sistemas ERP: `cadastro_produtos`,
`emissao_nota_fiscal` e `calculo_impostos`. É uma ferramenta puramente
determinística — não faz nenhuma chamada a LLM — e será usada pelo nó
`consultar_base_local` do grafo do agente, implementado em um prompt
futuro.

Exemplo mínimo de uso:

```python
from app.tools.local_kb import consultar_cenario

dados = consultar_cenario("cadastro_produtos")
```

## Próximos passos

- Implementação do grafo do agente com LangGraph (`app/agent`).
- Implementação da interface web (`app/web`).
- Ampliação dos testes automatizados (`tests`).

Essas etapas serão realizadas em prompts futuros.
