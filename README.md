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

## Exemplos de entrada e saída

Os exemplos abaixo são respostas **reais** do agente (Gemini 3.5 Flash),
obtidas manualmente uma vez por cenário — nunca dentro da suíte
automatizada de testes, que sempre usa mock do LLM.

### Exemplo de requisição via curl

```bash
curl -X POST http://127.0.0.1:8000/api/analisar \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Quais impactos no cadastro de produtos do ERP com a Reforma Tributária?"}'
```

### 1. Cadastro de produtos

**Pergunta:** "Quais impactos no cadastro de produtos do ERP com a Reforma Tributária?"

```json
{
  "cenario_identificado": "cadastro_produtos",
  "resposta_estruturada": {
    "cenario_analisado": "Análise dos impactos no cadastro de produtos do ERP decorrentes da transição para a Reforma Tributária (IBS/CBS), com foco em parametrização tributária, revisão de NCMs, criação do campo cClassTrib e novas regras de exceção.",
    "pontos_reforma_relacionados": [
      "O NCM continua obrigatório e ganha função estratégica: passa a ajudar a identificar a incidência de IBS, CBS e Imposto Seletivo.",
      "O cClassTrib substitui a lógica antiga de CST/CFOP e precisa ser atribuído a cada produto/serviço com base em análise contextual (NCM + natureza da operação + anexos da LC 214/2025), não apenas por 'de-para' automático.",
      "Existem anexos da LC 214/2025 com reduções e isenções específicas (ex.: cesta básica com alíquota zero, dispositivos de acessibilidade, medicamentos, educação, transporte público, saúde)."
    ],
    "impactos_tecnicos_erp": [
      "Necessidade de revisar e atualizar o campo NCM de todos os produtos cadastrados com base nas tabelas mais recentes.",
      "Criação/adequação de campo(s) para armazenar o cClassTrib e o CST do IBS/CBS por produto (ou por combinação produto + operação).",
      "Cadastro de regras de exceção por produto (redução de alíquota, isenção, alíquota zero) vinculadas aos anexos da LC 214/2025."
    ],
    "pontos_atencao": [
      "Deve-se validar com a área fiscal/contábil quais produtos se enquadram em reduções, isenções ou alíquota zero antes de aplicar qualquer classificação em massa no sistema.",
      "Este retorno tem caráter informativo de apoio tecnológico e não constitui parecer jurídico ou fiscal definitivo."
    ],
    "checklist_tecnico": [
      "Revisar o NCM de todos os produtos cadastrados com base na tabela vigente.",
      "Mapear e atribuir o cClassTrib e o CST do IBS/CBS a cada produto/operação.",
      "Testar simulação de emissão de nota para os produtos mais representativos do catálogo em ambiente de homologação."
    ]
  }
}
```

*(resposta completa tem 5-6 itens por bloco; alguns foram omitidos aqui por brevidade — a estrutura e o conteúdo são reais, sem edição de conteúdo.)*

### 2. Emissão de nota fiscal

**Pergunta:** "Preciso emitir uma NF-e, o que muda com a reforma tributária?"

```json
{
  "cenario_identificado": "emissao_nota_fiscal",
  "resposta_estruturada": {
    "cenario_analisado": "Emissão de Notas Fiscais Eletrônicas (NF-e/NFC-e) no ERP e as mudanças estruturais e de leiaute exigidas pela Reforma Tributária (IBS, CBS e Imposto Seletivo).",
    "pontos_reforma_relacionados": [
      "Novas Notas Técnicas (a partir da RT 2024.002) alteram o leiaute da NF-e/NFC-e inserindo grupos e campos para IBS, CBS e Imposto Seletivo.",
      "O CFOP perde parte de sua função estrutural, e a classificação passa a seguir tabelas nacionais do Comitê Gestor vinculadas ao cClassTrib.",
      "Existe um grupo de totais específico na NF-e para consolidar IBS, CBS e Imposto Seletivo, e divergências entre itens e totais provocarão rejeição da nota."
    ],
    "impactos_tecnicos_erp": [
      "Atualização do módulo emissor de NF-e/NFC-e para suportar os novos campos e grupos de IBS, CBS e IS no XML.",
      "Ajuste na geração do documento fiscal para integrar o cClassTrib e o CST por item a partir dos dados do cadastro.",
      "Implementação de validação interna pré-transmissão para garantir consistência entre os valores dos itens e o grupo de totais."
    ],
    "pontos_atencao": [
      "Erros de cadastro e parametrização serão validados em tempo real pela Receita Federal (CBS) e Comitê Gestor (IBS), gerando rejeições imediatas do XML.",
      "Este documento serve exclusivamente como orientação técnica para desenvolvimento e suporte de sistemas, não devendo ser considerado parecer jurídico, fiscal ou contábil definitivo."
    ],
    "checklist_tecnico": [
      "Confirmar a atualização do emissor de acordo com a Nota Técnica mais recente de IBS/CBS/IS.",
      "Garantir que os cálculos dos itens fecham perfeitamente com o grupo de totais do documento.",
      "Executar testes completos de emissão para operações comuns (venda, devolução, transferência, remessa) em homologação."
    ]
  }
}
```

*(mesma observação: alguns itens de cada bloco foram omitidos por brevidade.)*

### 3. Cálculo de impostos (IBS/CBS)

**Pergunta:** "Como o cálculo de impostos do ERP pode ser afetado pela CBS e IBS?"

```json
{
  "cenario_identificado": "calculo_impostos",
  "resposta_estruturada": {
    "cenario_analisado": "Avaliação de como o cálculo de impostos do ERP é impactado pela introdução da CBS e do IBS, estruturados sob o modelo de IVA Dual.",
    "pontos_reforma_relacionados": [
      "A base de cálculo do IBS/CBS é o valor da operação, sendo calculados por fora (não integram sua própria base), nos termos do art. 12 da LC 214/2025.",
      "Adoção do princípio da não cumulatividade plena, gerando direito a crédito ao adquirente desde que o bem ou serviço seja utilizado em atividade tributada.",
      "Tributação baseada no princípio do destino, onde o imposto é consolidado no local de consumo e não na origem."
    ],
    "impactos_tecnicos_erp": [
      "Revisão e adequação da engine de cálculo de impostos para aplicar o conceito de tributação por fora.",
      "Implementação de rotinas de cálculo de créditos e débitos de IBS/CBS por operação com foco na não cumulatividade plena.",
      "Preparação dos módulos financeiro e contábil do ERP para suportar o fluxo de conciliação e liquidação via split payment."
    ],
    "pontos_atencao": [
      "Qualquer alteração estrutural no ERP, parametrização ou simulação de preços deve ser obrigatoriamente validada junto às áreas fiscal e contábil da empresa.",
      "Este material serve exclusivamente como apoio técnico inicial ao desenvolvimento de sistemas e não deve ser interpretado como parecer legal, fiscal ou contábil definitivo."
    ],
    "checklist_tecnico": [
      "Validar se a engine de cálculo do ERP está aplicando corretamente a regra de tributação por fora para o IBS e a CBS.",
      "Testar a lógica de apropriação e geração de créditos e débitos por operação conforme o princípio da não cumulatividade.",
      "Mapear o impacto do fluxo de split payment na conciliação bancária e financeira dos meios de pagamento suportados."
    ]
  }
}
```

*(mesma observação: alguns itens de cada bloco foram omitidos por brevidade.)*

## Próximos passos

- Revisão do checklist de entrega do mini-projeto.

Essa etapa será realizada em um prompt futuro.
