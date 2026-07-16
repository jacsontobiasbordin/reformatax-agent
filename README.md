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
   preenchida com o modelo padrão do projeto (`gemini-3.5-flash`).

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
modelo `gemini-3.5-flash`, pelo custo-benefício. Os demais provedores existem
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

## Grafo do agente (LangGraph)

O fluxo do agente é implementado como um grafo do LangGraph em `app/agent`,
e agora está **funcionalmente completo de ponta a ponta**:

```
validar_entrada → identificar_cenario → consultar_base_local →
gerar_analise ⇄ validar_resposta → (fim | responder_erro_geracao → fim)
```

O laço entre `gerar_analise` e `validar_resposta` é o mecanismo de retry:
se a resposta estruturada do LLM vier incompleta ou em formato inesperado,
o grafo tenta gerar novamente, até `MAX_TENTATIVAS_GERACAO` (2) chamadas ao
LLM por pergunta. Esgotadas as tentativas, o fluxo cai em
`responder_erro_geracao`, que monta uma mensagem de fallback amigável antes
de encerrar — o grafo sempre termina, nunca entra em loop infinito.

- `app/agent/state.py` — define `AgentState`, o estado compartilhado entre
  os nós (pergunta do usuário, cenário identificado, dados da base local,
  resposta estruturada, alertas de validação e `tentativas_geracao`, o
  contador de execuções do nó `gerar_analise`). Ao montar o estado de
  entrada do grafo (`.invoke({...})`), `tentativas_geracao` deve começar em
  `0` — o código também trata a ausência dessa chave como `0` na primeira
  execução, então ela pode ser omitida do dicionário de entrada sem quebrar
  o fluxo.
- `app/agent/nodes.py` — implementa os nós do fluxo: `validar_entrada`,
  `identificar_cenario` (heurística por palavras-chave, sem LLM),
  `consultar_base_local` (integra com `app/tools/local_kb.py`),
  `responder_entrada_invalida`, `responder_fora_de_escopo`,
  `gerar_analise` (único nó que chama um LLM, sempre via
  `app.llm.factory.get_llm()`, incrementando `tentativas_geracao` a cada
  execução), `validar_resposta` (confere se os 5 blocos da resposta
  estruturada estão presentes e não vazios) e `responder_erro_geracao`
  (fallback após esgotar as tentativas de geração).
- `app/agent/schemas.py` — define `AnaliseEstruturada`, o schema
  `pydantic` dos 5 blocos da resposta final, usado com
  `with_structured_output`.
- `app/agent/prompts.py` — define o prompt de sistema do nó
  `gerar_analise`.
- `app/agent/graph.py` — monta o `StateGraph`, com arestas condicionais
  para tratar entrada inválida, perguntas fora dos três cenários
  suportados e o laço de retry/fallback de `gerar_analise`, e expõe
  `build_graph()`, que retorna o grafo já compilado.

O nó `gerar_analise` consome a API do provedor configurado em
`LLM_PROVIDER` (Gemini 3 Flash por padrão) para gerar a resposta
estruturada a partir do contexto recuperado da base local. Os testes
automatizados (`tests/test_gerar_analise.py` e
`tests/test_validacao_resposta.py`) usam mock do LLM — não gastam tokens
nem exigem API key real, incluindo o cenário de esgotamento de tentativas.
Há também um teste de integração opcional
(`tests/test_integration_llm.py`, marcado com `@pytest.mark.integration`),
que chama o provedor de verdade e só roda manualmente com
`pytest -m integration` (fica de fora da suíte padrão, configurada em
`pytest.ini`).

## Interface web (FastAPI)

O agente é exposto através de uma API em FastAPI (`app/web/main.py`) e uma
tela estática em HTML/CSS/JS puro (`app/web/static/`), sem nenhum
framework front-end — apenas uma camada de apresentação sobre o grafo já
implementado em `app/agent`.

- `app/web/schemas.py` — `PerguntaRequest` (validação leve de tamanho do
  payload) e `AnaliseResponse` (cenário identificado, resposta estruturada
  e alertas).
- `app/web/main.py` — `get_graph()` constrói o grafo uma única vez (cache
  com `lru_cache`); `GET /api/cenarios` lista os cenários suportados (a
  partir de `listar_cenarios_disponiveis()`, sem duplicar essa lista no
  front-end); `POST /api/analisar` monta o estado inicial do grafo
  (incluindo `tentativas_geracao: 0`), executa `.invoke()` e devolve o
  resultado. Qualquer falha inesperada do `.invoke()` vira um HTTP 500
  genérico, sem vazar stack trace ao navegador — o acesso ao LLM continua
  acontecendo somente no backend, via `app.llm.factory.get_llm()`.
- `app/web/static/index.html`, `style.css`, `app.js` — cabeçalho com nome
  e descrição do projeto, campo de pergunta, botões rápidos por cenário
  (preenchem a textarea com uma pergunta de exemplo — o backend continua
  identificando o cenário a partir do texto), botão "Analisar impacto",
  indicador de progresso e os 5 cards do resultado, com ações de "Copiar
  resposta" e "Baixar relatório" (arquivo `.txt`, via `Blob`, sem
  dependências externas nem geração de PDF).

### Como executar a interface web

```bash
uvicorn app.web.main:app --reload
```

Acesse `http://127.0.0.1:8000` no navegador.

A indicação de progresso desta versão é simplificada (um texto
"Analisando..." com spinner enquanto a requisição está em andamento) —
não há acompanhamento granular de cada nó do grafo em tempo real (isso
exigiria Server-Sent Events/streaming, fora do escopo deste mini-projeto,
mas é uma evolução possível). A tela segue a estrutura definida na seção
12 do escopo do projeto ([docs/escopo.md](docs/escopo.md)): campo de
pergunta, botões rápidos para os três cenários, botão de análise,
progresso e resultado em cards com ação de copiar/baixar.

## Próximos passos

- Testes finais, exemplos reais de entrada/saída no README e revisão do
  checklist de entrega do mini-projeto.

Essa etapa será realizada em um prompt futuro.
