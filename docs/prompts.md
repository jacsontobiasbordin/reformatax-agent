# Registro de Prompts

Este documento registra os prompts utilizados ao longo do desenvolvimento do
ReformaTax Agent, na íntegra, para fins de rastreabilidade e documentação do
processo.

## Prompt 1 — 2026-07-09

**Resultado:** Estrutura de pastas e arquivos criada; repositório Git
inicializado na branch `main`; documentação inicial (README, escopo,
prompts), `.gitignore`, `requirements.txt` e `.env.example` adicionados;
seis commits semânticos criados. Nenhuma lógica em Python implementada
nesta etapa.

**Prompt integral:**

```
Você vai me ajudar a iniciar um projeto em Python chamado "ReformaTax Agent" —
um assistente de IA que analisa impactos técnicos da Reforma Tributária em
sistemas ERP, para os cenários: cadastro de produtos, emissão de nota fiscal
e cálculo de impostos (IBS/CBS). O agente será implementado com LangGraph em
uma etapa futura.

IMPORTANTE: Nesta primeira etapa, NÃO implemente nenhuma lógica em Python.
Não crie funções, classes, grafos do LangGraph, rotas de API ou qualquer
código funcional. O objetivo aqui é apenas montar a estrutura do projeto,
a documentação inicial e o versionamento com Git. Arquivos de código Python
podem ser criados vazios ou apenas com um placeholder mínimo (ex.: comentário
indicando o que será implementado depois), nunca com implementação real.

Execute as seguintes etapas, nesta ordem:

1. INICIALIZAR O REPOSITÓRIO GIT
   - Rode `git init` na raiz do projeto.
   - Configure a branch principal como `main`.
   - Não faça nenhum commit ainda; isso será feito ao final, por partes,
     seguindo o padrão de commits semânticos descrito no passo 5.

2. CRIAR A ESTRUTURA DE PASTAS E ARQUIVOS
   Crie exatamente esta estrutura (pastas vazias devem conter um arquivo
   `.gitkeep` para serem versionadas pelo Git):

   reformatax-agent/
   ├── app/
   │   ├── __init__.py
   │   ├── agent/
   │   │   ├── __init__.py
   │   │   └── .gitkeep          # grafo LangGraph (estado, nós, conexões) — futuro
   │   ├── tools/
   │   │   ├── __init__.py
   │   │   └── .gitkeep          # ferramenta de consulta à base local — futuro
   │   └── web/
   │       ├── __init__.py
   │       └── .gitkeep          # interface web — futuro
   ├── data/
   │   └── reforma_tributaria_erp.json   # já existente, apenas mover para cá
   ├── docs/
   │   ├── escopo.md              # já existente, apenas mover para cá
   │   ├── prompts.md             # novo, ver passo 4
   │   └── apresentacao/
   │       └── .gitkeep           # slides da apresentação — mover para cá
   ├── tests/
   │   ├── __init__.py
   │   └── .gitkeep               # testes automatizados — futuro
   ├── .env.example
   ├── .gitignore
   ├── requirements.txt
   └── README.md

   Cada arquivo `__init__.py` deve ficar vazio por enquanto (apenas para marcar
   os diretórios como pacotes Python).

3. CRIAR O .gitignore
   Gere um `.gitignore` adequado para um projeto Python, cobrindo pelo menos:
   - Ambientes virtuais (`.venv/`, `venv/`, `env/`)
   - Cache do Python (`__pycache__/`, `*.pyc`, `*.pyo`)
   - Arquivos de variáveis de ambiente (`.env`)
   - Arquivos de IDE/editor (`.vscode/`, `.idea/`)
   - Arquivos de sistema operacional (`.DS_Store`, `Thumbs.db`)
   - Diretórios de build/distribuição (`build/`, `dist/`, `*.egg-info/`)
   - Logs (`*.log`)
   Nunca ignore o arquivo `.env.example` — ele deve ser versionado.

4. CRIAR OS ARQUIVOS DE DOCUMENTAÇÃO (specs em Markdown)
   - `README.md`: crie um esqueleto inicial com as seções: nome do projeto,
     descrição breve, status ("em desenvolvimento — estrutura inicial"),
     objetivo do agente, escopo (3 cenários), estrutura de pastas, como
     configurar o ambiente (instruções de instalação do requirements.txt),
     e uma seção "Próximos passos" citando que a implementação em LangGraph
     será feita em prompts futuros. Não descreva funcionalidades como se já
     estivessem implementadas.
   - `docs/escopo.md`: mover para esse caminho o conteúdo do escopo do projeto
     já definido (não reescrever, apenas organizar no novo caminho).
   - `docs/prompts.md`: criar o arquivo com um título e uma tabela/lista vazia
     pronta para receber os prompts usados ao longo do projeto, e já registrar
     este prompt inicial como o primeiro item.
   - `.env.example`: liste apenas os nomes de variáveis de ambiente que
     provavelmente serão necessárias (sem valores reais), por exemplo:
     `ANTHROPIC_API_KEY=` ou `OPENAI_API_KEY=` (o que for definido depois)
     e `APP_ENV=development`.

5. CRIAR O requirements.txt (linguagem: Python)
   Como o projeto usará LangGraph para o agente e uma interface web simples,
   crie um `requirements.txt` inicial com as dependências esperadas do projeto
   (mesmo que ainda não sejam usadas em código), fixando versões compatíveis
   conhecidas no momento da criação:
   - langgraph
   - langchain
   - langchain-core
   - langchain-anthropic  (ou langchain-openai, conforme o provedor de LLM escolhido)
   - python-dotenv
   - fastapi
   - uvicorn
   - pydantic
   Adicione um comentário no topo do arquivo explicando que as versões devem
   ser fixadas (`==`) assim que o ambiente for testado pela primeira vez.

6. PADRÃO DE COMMITS SEMÂNTICOS (Conventional Commits)
   Utilize o padrão:

     <tipo>(<escopo opcional>): <descrição curta no imperativo>

   Tipos permitidos neste projeto:
   - feat:     nova funcionalidade
   - fix:      correção de bug
   - docs:     documentação (README, docs/*.md, comentários)
   - chore:    tarefas de configuração/estrutura que não alteram lógica (ex.: estrutura de pastas, .gitignore)
   - refactor: mudança de código que não corrige bug nem adiciona feature
   - test:     criação ou ajuste de testes
   - style:    formatação, espaços, ponto e vírgula (sem mudança de lógica)
   - build:    mudanças em dependências ou build (ex.: requirements.txt)
   - ci:       configuração de integração contínua

   Exemplos de commits para esta primeira etapa (crie um commit por etapa
   concluída, na ordem abaixo, nunca um único commit genérico):

   1. chore: inicializa repositório e estrutura de pastas do projeto
   2. chore: adiciona .gitignore para projeto Python
   3. docs: adiciona README inicial e escopo do projeto
   4. docs: cria docs/prompts.md com registro do primeiro prompt
   5. build: adiciona requirements.txt com dependências iniciais
   6. chore: adiciona .env.example com variáveis esperadas

7. VALIDAÇÃO FINAL
   Ao final, rode `git log --oneline` e `git status` e me mostre a saída,
   confirmando que:
   - Não há arquivos sensíveis (chaves, tokens, .env real) sendo versionados;
   - Todos os commits seguem o padrão semântico definido acima;
   - Nenhum arquivo `.py` contém lógica implementada (apenas placeholders vazios).

Não avance para a implementação do grafo LangGraph, da ferramenta de consulta
ao JSON ou da interface web nesta etapa — isso será feito em prompts seguintes.
```

## Prompt 2 — 2026-07-09

**Resultado:** Remote `origin` configurado apontando para
`github.com/jacsontobiasbordin/reformatax-agent`; branch `develop` criada
a partir de `main` e enviada ao remoto; branch
`chore/estrutura-inicial-projeto` criada a partir de `develop` com o
histórico de commits do Prompt 1; PR #1 aberto de
`chore/estrutura-inicial-projeto` para `develop` e posteriormente
mergeado. Nenhuma lógica em Python implementada nesta etapa.

**Prompt integral:**

```
Agora vamos conectar o repositório local ao GitHub e abrir o primeiro Pull
Request, mantendo a estrutura de branches do projeto. Ainda NÃO implemente
nenhuma lógica em Python — este prompt trata apenas de Git/GitHub (remote,
branches e PR).

Repositório remoto: https://github.com/jacsontobiasbordin/reformatax-agent.git
Branch de destino do PR: develop

Execute as etapas na ordem abaixo:

1. ADICIONAR O REMOTO
   - Verifique se já existe um remote chamado "origin" (`git remote -v`).
   - Se não existir, adicione:
     git remote add origin https://github.com/jacsontobiasbordin/reformatax-agent.git
   - Rode `git fetch origin` para trazer o estado atual do repositório remoto.

2. GARANTIR A EXISTÊNCIA DA BRANCH "develop"
   - Verifique se a branch `develop` já existe no remoto
     (`git ls-remote --heads origin develop`).
   - Se existir: crie a branch local rastreando a remota
     (`git checkout -b develop origin/develop`).
   - Se NÃO existir: crie a branch `develop` localmente a partir da branch
     atual (`main`), que já contém a estrutura inicial do projeto:
     git checkout -b develop
     git push -u origin develop
   - `develop` deve ser tratada como a branch de integração do projeto.
     Nenhum commit deve ser feito diretamente nela a partir de agora —
     todo trabalho passa por uma branch de feature e um Pull Request.

3. CRIAR A BRANCH COM A ESTRUTURA INICIAL
   - A partir de `develop`, crie uma nova branch para organizar o trabalho
     já realizado no Prompt 01 (estrutura de pastas, .gitignore, README,
     docs/escopo.md, docs/prompts.md, requirements.txt, .env.example):
     git checkout -b chore/estrutura-inicial-projeto develop
   - Use o padrão de nomes de branch abaixo em todo o projeto, alinhado aos
     tipos de commit semântico já definidos no Prompt 01:
       feature/<descrição-curta>   → novas funcionalidades
       fix/<descrição-curta>       → correções
       docs/<descrição-curta>      → documentação
       chore/<descrição-curta>     → configuração/estrutura
       refactor/<descrição-curta>  → refatoração
       test/<descrição-curta>      → testes
   - Se os commits da estrutura inicial já existirem em `main` (feitos no
     Prompt 01) e ainda não estiverem em `develop`/na nova branch, traga-os
     com `git cherry-pick` ou `git rebase`, preservando as mensagens de
     commit semânticas originais — não crie um commit novo genérico que
     esconda o histórico já feito.

4. ENVIAR A BRANCH PARA O REMOTO
   git push -u origin chore/estrutura-inicial-projeto

5. ABRIR O PULL REQUEST PARA "develop"
   - Se a GitHub CLI (`gh`) estiver instalada e autenticada, abra o PR
     diretamente pelo terminal:
     gh pr create \
       --base develop \
       --head chore/estrutura-inicial-projeto \
       --title "chore: estrutura inicial do projeto ReformaTax Agent" \
       --body "## Contexto
Primeira entrega do mini-projeto ReformaTax Agent: assistente de impacto
técnico da Reforma Tributária em ERP (LangGraph).

## O que foi feito
- Estrutura de pastas do projeto (app/agent, app/tools, app/web, data,
  docs, tests)
- .gitignore para projeto Python
- README.md inicial com objetivo, escopo e instruções de instalação
- docs/escopo.md com o escopo detalhado do projeto
- docs/prompts.md com o registro dos prompts utilizados
- requirements.txt com as dependências iniciais esperadas
- .env.example com as variáveis de ambiente previstas

## Fora do escopo deste PR
- Nenhuma lógica em Python foi implementada (grafo LangGraph, ferramenta
  de consulta e interface web ficam para PRs seguintes)

## Checklist
- [x] Nenhum arquivo sensível (chave, token, .env real) foi versionado
- [x] Commits seguem o padrão semântico definido no projeto
- [x] .gitignore cobre ambiente virtual, cache e variáveis de ambiente"
   - Se o `gh` NÃO estiver disponível ou autenticado, não tente autenticar
     sozinho: apenas me informe isso e me dê o link pronto para abrir o PR
     manualmente pelo navegador, no formato:
     https://github.com/jacsontobiasbordin/reformatax-agent/compare/develop...chore/estrutura-inicial-projeto?expand=1

6. VALIDAÇÃO FINAL
   Mostre a saída de:
   - `git remote -v` (confirmando a URL do remoto)
   - `git branch -a` (confirmando a existência de main, develop e a branch
     de feature, local e remota)
   - `git log --oneline --graph --all` (confirmando o histórico e que a
     branch de feature parte de develop)
   Confirme também qual foi o resultado da etapa 5 (PR criado com sucesso
   via `gh`, ou link manual fornecido).

Não implemente código Python nesta etapa. O foco é exclusivamente a
configuração do repositório remoto, a organização de branches e a abertura
do Pull Request para develop.
```

## Prompt 3 — 2026-07-09

**Resultado:** Branch `chore/config-gemini` criada a partir de `develop`;
`requirements.txt` atualizado com as dependências do Gemini
(`langchain-google-genai`, `google-generativeai`, `pydantic-settings`,
entre outras); `.env.example` atualizado com `GOOGLE_API_KEY` e
`GEMINI_MODEL`; módulo `app/config.py` criado com `pydantic-settings` e
`get_settings()`, sem instanciar client do Gemini nem fazer chamadas de
rede; README atualizado com instruções de obtenção da API key. Nenhuma
chamada real à API do Gemini nem lógica do grafo LangGraph implementada
nesta etapa.

**Prompt integral:**

```
Vamos preparar o projeto para usar o Gemini 3 Flash (via Google AI Studio /
Gemini API) como LLM do agente. Nesta etapa, crie APENAS a configuração
necessária para acessar o modelo — NÃO implemente o grafo do LangGraph, os
nós do agente, nem faça nenhuma chamada real à API do Gemini. O único código
Python permitido aqui é um módulo de configuração que carrega variáveis de
ambiente, sem executar nenhuma requisição de rede.

Modelo definido para o projeto: gemini-3-flash
Biblioteca de integração: langchain-google-genai (LangChain + Gemini)

Crie a branch a partir de develop:
  git checkout develop
  git pull origin develop
  git checkout -b chore/config-gemini

Execute as etapas abaixo, nesta ordem:

1. ATUALIZAR O requirements.txt
   Ajuste as dependências para refletir o provedor de LLM definido
   (Gemini), removendo qualquer referência a outros provedores que não
   serão usados neste projeto (ex.: langchain-anthropic, langchain-openai)
   e adicionando:
   - langgraph
   - langchain
   - langchain-core
   - langchain-google-genai
   - google-generativeai
   - python-dotenv
   - fastapi
   - uvicorn
   - pydantic
   - pydantic-settings
   Mantenha o comentário no topo do arquivo (criado no Prompt 01) indicando
   que as versões devem ser fixadas (`==`) assim que o ambiente for testado
   pela primeira vez.

2. ATUALIZAR O .env.example
   Substitua as variáveis genéricas de provedor de LLM criadas no Prompt 01
   pelas variáveis reais que o projeto vai usar com o Gemini:
     GOOGLE_API_KEY=
     GEMINI_MODEL=gemini-3-flash
     APP_ENV=development
   Não inclua nenhuma chave real — apenas os nomes das variáveis, vazios.
   Confirme que `.env` (sem "*.example") continua listado no `.gitignore`.

3. CRIAR O MÓDULO DE CONFIGURAÇÃO (app/config.py)
   Implemente uma única classe de configurações usando `pydantic-settings`
   (`BaseSettings`), responsável apenas por:
   - Carregar `GOOGLE_API_KEY` (obrigatória) e `GEMINI_MODEL` (com valor
     padrão "gemini-3-flash") a partir do arquivo `.env`;
   - Carregar `APP_ENV` (padrão "development");
   - Expor uma função `get_settings()` que retorna a instância de
     configurações (pode usar `functools.lru_cache` para evitar recarregar
     o `.env` a cada chamada).
   Regras importantes:
   - NÃO importe nem instancie `ChatGoogleGenerativeAI` ou qualquer client
     do Gemini neste módulo — ele deve apenas ler variáveis de ambiente.
   - NÃO faça nenhuma chamada de rede.
   - Se `GOOGLE_API_KEY` não estiver definida, a criação das configurações
     deve falhar com uma mensagem de erro clara (comportamento padrão do
     pydantic-settings para campo obrigatório ausente já resolve isso).
   - Adicione um docstring curto no topo do arquivo explicando que este
     módulo é usado pelo nó de geração do agente, implementado em um
     prompt futuro (Prompt 06).

4. ATUALIZAR O README.md
   Na seção de configuração de ambiente, adicione uma instrução explicando
   como obter uma API key do Gemini (Google AI Studio) e como preenchê-la
   no arquivo `.env` local (copiado a partir de `.env.example`). Não descreva
   funcionalidades do agente que ainda não existem.

5. VALIDAÇÃO LOCAL (sem chamar a API)
   - Rode `pip install -r requirements.txt` em um ambiente virtual e
     confirme que a instalação conclui sem erros.
   - Crie um `.env` local (não versionado) com uma `GOOGLE_API_KEY` de
     teste e rode:
     python -c "from app.config import get_settings; print(get_settings())"
   - Confirme que o comando imprime as configurações carregadas (a chave
     pode aparecer no print — isso é só um teste local, não versione esse
     `.env` de forma alguma).
   - Confirme, revisando o diff, que nenhum arquivo `.env` real foi criado
     dentro da árvore versionada pelo Git.

6. COMMITS SEMÂNTICOS (um por etapa concluída)
   1. build: atualiza requirements.txt com dependências do Gemini
   2. chore: atualiza .env.example com variáveis do Gemini
   3. chore: adiciona módulo de configuração do Gemini (app/config.py)
   4. docs: atualiza README com instruções de configuração da API key

7. ENVIAR A BRANCH E ABRIR O PULL REQUEST
   git push -u origin chore/config-gemini

   Abra o PR direcionado para develop (via `gh pr create` se disponível,
   ou fornecendo o link manual de comparação, como no Prompt 02):
     Título: "chore: configuração inicial do Gemini 3 Flash"
     Corpo, no mesmo padrão do PR anterior (Contexto / O que foi feito /
     Fora do escopo / Checklist), destacando em "Fora do escopo":
       - Nenhuma chamada real à API do Gemini foi implementada
       - O grafo do LangGraph e os nós do agente ainda não existem

8. VALIDAÇÃO FINAL
   Mostre a saída de `git log --oneline --graph` e `git status`, confirmando
   que:
   - Nenhuma chave de API real foi commitada;
   - `app/config.py` não faz nenhuma chamada de rede nem importa clientes
     do Gemini;
   - Os commits seguem o padrão semântico definido no projeto.

Não implemente o grafo do LangGraph, os nós do agente ou qualquer chamada
ao modelo gemini-3-flash nesta etapa.
```

## Prompt 4 — 2026-07-14

**Resultado:** Branch `chore/multi-llm-provider` criada a partir de
`develop`; `requirements.txt` atualizado com `langchain-anthropic` e
`langchain-openai`, mantendo `langchain-google-genai`; `.env.example`
reestruturado com o seletor `LLM_PROVIDER` (gemini | anthropic | openai) e
uma seção de variáveis por provedor; `app/config.py` refatorado com o campo
`llm_provider`, campos opcionais por provedor e um validador que exige a
API key do provedor ativo; pacote `app/llm/` criado com `factory.py`
implementando `get_llm()`, único ponto do projeto que importa
`ChatGoogleGenerativeAI`, `ChatAnthropic` ou `ChatOpenAI`; README atualizado
com a seção "Provedores de LLM suportados". Validação local confirmou a
instanciação dos três clients (sem chamada de rede) e o erro claro quando a
API key do provedor selecionado está ausente. Nenhuma chamada real a
nenhum provedor foi feita, e o grafo do LangGraph e os nós do agente ainda
não existem.

**Prompt integral:**

```
O projeto está hoje acoplado ao Gemini (variáveis GOOGLE_API_KEY e
GEMINI_MODEL, hardcoded no restante do plano como o único provedor). Isso
precisa mudar: o agente deve ser capaz de rodar com Gemini, Claude
(Anthropic) ou OpenAI, trocando apenas variáveis de ambiente — sem alterar
código do grafo ou dos nós nas etapas futuras. O provedor padrão do projeto
continua sendo Gemini 3 Flash, mas o código não pode assumir isso de forma
implícita.

Nesta etapa, crie apenas a camada de abstração e configuração do LLM.
NÃO implemente o grafo do LangGraph, os nós do agente, nem faça nenhuma
chamada real à API de nenhum provedor. A única validação permitida é
instanciar o client do LLM localmente (o que não gera chamada de rede) —
nunca invocá-lo.

Crie a branch a partir de develop:
  git checkout develop
  git pull origin develop
  git checkout -b chore/multi-llm-provider

Execute as etapas abaixo, nesta ordem:

1. ATUALIZAR O requirements.txt
   Adicione os pacotes dos demais provedores, mantendo o do Gemini:
   - langchain-google-genai   (já existente — Gemini)
   - langchain-anthropic      (novo — Claude)
   - langchain-openai         (novo — OpenAI)
   Os três ficam como dependência do projeto; qual deles é efetivamente
   usado em tempo de execução é decidido por variável de ambiente, não por
   qual pacote está instalado.

2. ATUALIZAR O .env.example
   Reestruture as variáveis de ambiente para suportar múltiplos provedores,
   com um "seletor" explícito e uma seção por provedor:

     # Provedor ativo: gemini | anthropic | openai
     LLM_PROVIDER=gemini

     # Gemini (Google AI Studio)
     GOOGLE_API_KEY=
     GEMINI_MODEL=gemini-3-flash

     # Claude (Anthropic) — usado se LLM_PROVIDER=anthropic
     ANTHROPIC_API_KEY=
     ANTHROPIC_MODEL=claude-sonnet-5

     # OpenAI — usado se LLM_PROVIDER=openai
     OPENAI_API_KEY=
     OPENAI_MODEL=gpt-5.1

     APP_ENV=development

   Apenas as variáveis do provedor efetivamente ativo em LLM_PROVIDER
   precisam estar preenchidas em um `.env` real; as demais podem ficar
   vazias. Não invente nomes de modelo além dos citados sem confirmar —
   apenas documente que o nome do modelo de cada provedor é configurável.

3. REFATORAR app/config.py
   - Adicione o campo `llm_provider` (Literal["gemini", "anthropic",
     "openai"], padrão "gemini") às configurações já existentes.
   - Mantenha os campos por provedor (google_api_key, gemini_model,
     anthropic_api_key, anthropic_model, openai_api_key, openai_model),
     todos opcionais no nível do schema — a obrigatoriedade real depende de
     qual provedor está ativo, e é validada no passo 4, não aqui.
   - Adicione uma validação (validator do pydantic-settings ou função
     auxiliar) que, ao carregar as configurações, verifica se a API key do
     provedor selecionado em `llm_provider` está preenchida, e levanta um
     erro claro e específico se não estiver (ex.: "GOOGLE_API_KEY é
     obrigatória quando LLM_PROVIDER=gemini").

4. CRIAR A FÁBRICA DE LLM (app/llm/factory.py)
   - Crie o pacote `app/llm/` com `__init__.py`.
   - Implemente uma função `get_llm()` que:
     - Lê as configurações via `get_settings()` (do Prompt 03);
     - Com base em `llm_provider`, instancia e retorna o client
       correspondente, todos compatíveis com a interface `BaseChatModel`
       do LangChain:
         - "gemini"    → ChatGoogleGenerativeAI(model=gemini_model, ...)
         - "anthropic" → ChatAnthropic(model=anthropic_model, ...)
         - "openai"    → ChatOpenAI(model=openai_model, ...)
     - Levanta um erro claro se `llm_provider` tiver um valor não suportado.
   - Esta função é o único ponto do projeto que deve conhecer as classes
     específicas de cada provedor. Qualquer nó do agente, em prompts
     futuros, deve chamar apenas `get_llm()` e programar contra a interface
     genérica do LangChain — nunca importar `ChatGoogleGenerativeAI`,
     `ChatAnthropic` ou `ChatOpenAI` diretamente fora deste arquivo.
   - Não chame `.invoke()`, `.generate()` nem qualquer método que dispare
     uma requisição de rede neste prompt — apenas a instanciação do client.

5. ATUALIZAR O README.md
   Adicione uma seção "Provedores de LLM suportados" explicando:
   - Que o projeto suporta Gemini, Claude e OpenAI através da variável
     `LLM_PROVIDER`;
   - Como trocar de provedor (mudar `LLM_PROVIDER` e preencher a API key
     correspondente no `.env`);
   - Que o provedor padrão/recomendado para este mini-projeto é
     `gemini` com o modelo `gemini-3-flash`, pelo custo-benefício.

6. VALIDAÇÃO LOCAL (sem chamar nenhuma API)
   - Rode `pip install -r requirements.txt` e confirme instalação sem erros.
   - Com um `.env` local de teste, valide os três cenários apenas na
     instanciação (sem invocar o modelo), por exemplo:
     LLM_PROVIDER=gemini    python -c "from app.llm.factory import get_llm; print(get_llm())"
     LLM_PROVIDER=anthropic python -c "from app.llm.factory import get_llm; print(get_llm())"
     LLM_PROVIDER=openai    python -c "from app.llm.factory import get_llm; print(get_llm())"
   - Confirme que, faltando a API key do provedor selecionado, o erro de
     validação descrito no passo 3 aparece de forma clara.

7. COMMITS SEMÂNTICOS (um por etapa concluída)
   1. build: adiciona dependências dos provedores Claude e OpenAI
   2. chore: reestrutura .env.example para múltiplos provedores de LLM
   3. refactor: adiciona seletor de provedor e validação em app/config.py
   4. feat: adiciona fábrica de LLM multi-provedor (app/llm/factory.py)
   5. docs: documenta provedores de LLM suportados no README

8. ENVIAR A BRANCH E ABRIR O PULL REQUEST
   git push -u origin chore/multi-llm-provider

   Abra o PR direcionado para develop:
     Título: "refactor: abstração multi-LLM (Gemini, Claude, OpenAI)"
     Corpo no mesmo padrão dos PRs anteriores (Contexto / O que foi feito /
     Fora do escopo / Checklist), destacando em "Fora do escopo":
       - Nenhuma chamada real a nenhum provedor foi feita
       - O grafo do LangGraph e os nós do agente ainda não existem
       - A escolha final do provedor para a entrega continua sendo Gemini
         3 Flash; os demais existem para portabilidade, não substituição

9. VALIDAÇÃO FINAL
   Mostre `git log --oneline --graph` e `git status`, confirmando que:
   - Nenhuma chave de API real foi commitada;
   - Nenhum outro arquivo do projeto importa diretamente classes de um
     provedor específico (apenas app/llm/factory.py);
   - Os commits seguem o padrão semântico do projeto.

Não implemente o grafo do LangGraph, os nós do agente ou qualquer chamada
real a um modelo nesta etapa — isso continua para os próximos prompts, que
a partir de agora devem sempre usar app.llm.factory.get_llm() em vez de
instanciar um provedor diretamente.
```

## Prompt 5 — 2026-07-14

**Resultado:** Branch `feature/ferramenta-consulta-base-local` criada a
partir de `develop`; `app/tools/local_kb.py` implementado com
`carregar_base()` (leitura cacheada, caminho fixo resolvido a partir da
raiz do projeto, sem aceitar caminho externo), `consultar_cenario()`,
`listar_cenarios_disponiveis()` e as exceções `CenarioNaoEncontradoError` e
`BaseLocalIndisponivelError`; `tests/test_local_kb.py` criado cobrindo os
três cenários válidos, cenário inválido, arquivo ausente e listagem de
cenários (6 testes, todos passando); README atualizado com a seção
"Ferramenta: consulta à base local". Primeira lógica Python funcional do
projeto, 100% determinística — nenhuma chamada a LLM nem grafo do LangGraph
implementados nesta etapa.

**Prompt integral:**

```
Vamos implementar a ferramenta integrada do agente: a leitura e consulta ao
arquivo local data/reforma_tributaria_erp.json (base de conhecimento dos
três cenários: cadastro_produtos, emissao_nota_fiscal, calculo_impostos).
Esta ferramenta é usada pelo nó "consultar_base_local" do grafo LangGraph,
que será implementado em um prompt futuro — aqui você só cria a função em
si, testável de forma isolada, sem grafo e sem LLM envolvidos.

NÃO implemente o grafo do LangGraph, os nós do agente nem nenhuma chamada a
get_llm(). Esta etapa é puramente sobre leitura de arquivo e validação.

Crie a branch a partir de develop:
  git checkout develop
  git pull origin develop
  git checkout -b feature/ferramenta-consulta-base-local

Execute as etapas abaixo, nesta ordem:

1. IMPLEMENTAR A FERRAMENTA (app/tools/local_kb.py)
   Crie o módulo com:
   - Uma constante `CENARIOS_VALIDOS` com os três cenários suportados:
     "cadastro_produtos", "emissao_nota_fiscal", "calculo_impostos"
     (devem bater exatamente com as chaves usadas em
     data/reforma_tributaria_erp.json).
   - Uma exceção customizada `CenarioNaoEncontradoError(Exception)` para
     quando o cenário pedido não existir na base.
   - Uma exceção customizada `BaseLocalIndisponivelError(Exception)` para
     falhas de leitura do arquivo (arquivo ausente, JSON inválido).
   - Uma função `carregar_base() -> dict` que:
     - Resolve o caminho do arquivo de forma fixa, relativa à raiz do
       projeto (ex.: usando `pathlib.Path(__file__).resolve().parents[2]
       / "data" / "reforma_tributaria_erp.json"`), nunca aceitando um
       caminho vindo de fora da função — reforçando a validação do escopo
       de "evitar leitura de arquivos fora da pasta definida";
     - Usa `functools.lru_cache` (ou cache manual simples) para não reler o
       arquivo do disco a cada chamada;
     - Lança `BaseLocalIndisponivelError` com mensagem clara se o arquivo
       não existir ou se o JSON estiver malformado (capture a exceção
       original de `json.JSONDecodeError`/`FileNotFoundError` e relance
       como a exceção customizada, preservando a causa com `raise ... from
       e`).
   - Uma função `consultar_cenario(cenario: str) -> dict` que:
     - Valida se `cenario` está em `CENARIOS_VALIDOS`; se não estiver,
       lança `CenarioNaoEncontradoError` com mensagem informando os
       cenários válidos;
     - Chama `carregar_base()` e retorna o sub-dicionário correspondente a
       `cenarios.<cenario>` do JSON (resumo, pontos_reforma_relacionados,
       impactos_tecnicos_erp, pontos_atencao, checklist_tecnico);
     - Lança `CenarioNaoEncontradoError` também se, por algum motivo, a
       chave não existir dentro do JSON carregado (defesa extra, mesmo já
       validando contra `CENARIOS_VALIDOS`).
   - Uma função `listar_cenarios_disponiveis() -> list[str]` que apenas
     retorna `CENARIOS_VALIDOS` como lista — útil depois para popular os
     botões rápidos da interface web.
   - Docstrings curtas em cada função explicando o propósito.

2. ESCREVER TESTES UNITÁRIOS (tests/test_local_kb.py)
   Usando `pytest`, cubra pelo menos:
   - `consultar_cenario` retorna um dicionário com as chaves esperadas
     (`resumo`, `pontos_reforma_relacionados`, `impactos_tecnicos_erp`,
     `pontos_atencao`, `checklist_tecnico`) para cada um dos três cenários
     válidos;
   - `consultar_cenario` com um cenário inválido (ex.: "cenario_invalido")
     lança `CenarioNaoEncontradoError`;
   - `carregar_base` lança `BaseLocalIndisponivelError` quando o arquivo não
     existe (simule apontando para um caminho inexistente via monkeypatch,
     sem alterar a função para aceitar caminho externo — teste a função
     como uma unidade isolada, mockando `Path` ou o caminho interno);
   - `listar_cenarios_disponiveis` retorna exatamente os três cenários
     esperados.
   Rode `pytest tests/test_local_kb.py -v` e confirme que todos os testes
   passam.

3. ATUALIZAR O README.md
   Adicione uma seção curta "Ferramenta: consulta à base local" explicando
   o que `app/tools/local_kb.py` faz, os cenários suportados e um exemplo
   mínimo de uso:

     from app.tools.local_kb import consultar_cenario
     dados = consultar_cenario("cadastro_produtos")

   Não descreva o grafo do LangGraph nem a geração de resposta com LLM
   aqui — isso ainda não existe no projeto.

4. VALIDAÇÃO LOCAL
   - Rode `pytest tests/ -v` e confirme que todos os testes passam.
   - Rode manualmente:
     python -c "from app.tools.local_kb import consultar_cenario; import json; print(json.dumps(consultar_cenario('calculo_impostos'), indent=2, ensure_ascii=False))"
     e confirme que a saída bate com o conteúdo de
     data/reforma_tributaria_erp.json.

5. COMMITS SEMÂNTICOS (um por etapa concluída)
   1. feat: adiciona ferramenta de consulta à base local de conhecimento
   2. test: adiciona testes unitários para a ferramenta de consulta local
   3. docs: documenta o uso da ferramenta de consulta local no README

6. ENVIAR A BRANCH E ABRIR O PULL REQUEST
   git push -u origin feature/ferramenta-consulta-base-local

   Abra o PR direcionado para develop:
     Título: "feat: ferramenta de consulta à base local de conhecimento"
     Corpo no mesmo padrão dos PRs anteriores (Contexto / O que foi feito /
     Fora do escopo / Checklist), destacando em "Fora do escopo":
       - Nenhum nó do LangGraph foi criado
       - Nenhuma chamada a get_llm() ou a qualquer provedor de LLM foi feita
       - A interface web ainda não consome esta ferramenta

7. VALIDAÇÃO FINAL
   Mostre a saída de `pytest tests/ -v`, `git log --oneline --graph` e
   `git status`, confirmando que:
   - Todos os testes passam;
   - Nenhum caminho de arquivo externo à pasta `data/` pode ser lido pela
     ferramenta (a função não aceita caminho como parâmetro vindo de fora);
   - Os commits seguem o padrão semântico do projeto, todos com prefixo
     coerente com uma feature (`feat`, `test`, `docs`).

Não implemente o grafo do LangGraph, os nós do agente, nem qualquer chamada
a get_llm() nesta etapa — isso começa no Prompt 06.
```

## Prompt 6 — 2026-07-14

**Resultado:** Branch `feature/grafo-langgraph-estado` criada a partir de
`develop`; `app/agent/state.py` com o `TypedDict AgentState`;
`app/agent/nodes.py` com os nós determinísticos `validar_entrada`,
`identificar_cenario` (heurística por palavras-chave), `consultar_base_local`
(integrado com `app.tools.local_kb`), `responder_entrada_invalida` e
`responder_fora_de_escopo`; `app/agent/graph.py` com `build_graph()`
montando um `StateGraph` com arestas condicionais para entrada inválida e
cenário fora de escopo, terminando em `consultar_base_local` → END;
`tests/test_agent_graph.py` com 5 testes de ponta a ponta (11 testes no
total no projeto, todos passando). README atualizado com a seção "Grafo do
agente (LangGraph)". Nenhuma chamada a `get_llm()` ou a qualquer provedor
de LLM foi feita nesta etapa.

**Prompt integral:**

```
Vamos montar o esqueleto do grafo do agente com LangGraph: o estado
compartilhado, os nós de validação e identificação de cenário, a integração
com a ferramenta de consulta local (app/tools/local_kb.py, do Prompt 05) e
as arestas condicionais do fluxo. NÃO implemente o nó de geração de análise
com LLM nem chame app.llm.factory.get_llm() nesta etapa — isso é o Prompt
07. Os nós desta etapa devem ser 100% determinísticos.

Crie a branch a partir de develop:
  git checkout develop
  git pull origin develop
  git checkout -b feature/grafo-langgraph-estado

Execute as etapas abaixo, nesta ordem:

1. DEFINIR O ESTADO DO GRAFO (app/agent/state.py)
   Crie um `TypedDict` chamado `AgentState` com os campos definidos no
   escopo do projeto:
   - pergunta_usuario: str
   - cenario_identificado: str | None
   - dados_base_local: dict | None
   - resposta_estruturada: dict | None
   - alertas: list[str]
   Adicione um docstring explicando o propósito de cada campo. Use
   `from __future__ import annotations` e tipagem do `typing`/`typing_extensions`
   compatível com o LangGraph.

2. IMPLEMENTAR OS NÓS DETERMINÍSTICOS (app/agent/nodes.py)
   Implemente as seguintes funções, cada uma recebendo e retornando um
   `AgentState` (ou o dicionário parcial de atualização, conforme o padrão
   do LangGraph):

   a) validar_entrada(state) -> dict
      - Remove espaços extras da pergunta (`strip()`).
      - Se a pergunta estiver vazia após o strip, adiciona a `alertas` a
        mensagem: "Por favor, informe uma pergunta ou selecione um cenário."
      - Se a pergunta tiver mais que 500 caracteres, adiciona a `alertas`:
        "Sua pergunta é muito longa. Tente resumir em até 500 caracteres."
      - Não lança exceção — apenas popula `alertas`; quem decide o que
        fazer com isso é a aresta condicional do passo 4.

   b) identificar_cenario(state) -> dict
      - Implementação determinística por palavras-chave (sem LLM), usando
        listas simples de termos, case-insensitive, em português:
          cadastro_produtos: ["cadastro", "produto", "ncm",
            "classificação tributária", "cclasstrib"]
          emissao_nota_fiscal: ["nota fiscal", "nf-e", "nfe", "nfc-e",
            "emissão", "danfe"]
          calculo_impostos: ["cálculo", "calculo", "imposto", "ibs", "cbs",
            "tributo", "alíquota", "aliquota"]
      - Se nenhum termo bater, define `cenario_identificado = "fora_de_escopo"`.
      - Documente no código, com um comentário curto, que esta é uma
        heurística simples e que uma versão futura poderia usar o LLM para
        casos ambíguos — mas isso não deve ser implementado agora.

   c) consultar_base_local(state) -> dict
      - Chama `consultar_cenario(state["cenario_identificado"])` de
        `app.tools.local_kb`.
      - Guarda o resultado em `dados_base_local`.
      - Se a ferramenta lançar `CenarioNaoEncontradoError` ou
        `BaseLocalIndisponivelError`, capture a exceção e adicione uma
        mensagem amigável a `alertas` (sem deixar a exceção propagar para
        fora do nó).

   d) responder_entrada_invalida(state) -> dict
      - Monta um `resposta_estruturada` simplificado (ex.: apenas um campo
        `mensagem`) repetindo o conteúdo de `alertas`, indicando que a
        pergunta precisa ser ajustada.

   e) responder_fora_de_escopo(state) -> dict
      - Monta um `resposta_estruturada` simplificado explicando que a
        pergunta não se encaixa em nenhum dos três cenários suportados
        (cadastro de produtos, emissão de nota fiscal, cálculo de
        impostos) e sugerindo reformular a pergunta.

3. MONTAR O GRAFO (app/agent/graph.py)
   Usando `langgraph.graph.StateGraph` e `AgentState`:
   - Adicione os nós: validar_entrada, identificar_cenario,
     consultar_base_local, responder_entrada_invalida,
     responder_fora_de_escopo.
   - Defina o ponto de entrada como validar_entrada.
   - Aresta condicional após validar_entrada:
       - se `alertas` não estiver vazia → responder_entrada_invalida → END
       - caso contrário → identificar_cenario
   - Aresta condicional após identificar_cenario:
       - se `cenario_identificado == "fora_de_escopo"` →
         responder_fora_de_escopo → END
       - caso contrário → consultar_base_local
   - Aresta direta: consultar_base_local → END (temporário; no Prompt 07 este
     nó passará a apontar para o novo nó `gerar_analise` em vez de END).
   - Exponha uma função `build_graph()` que monta e retorna o grafo
     **compilado** (`.compile()`), pronta para ser usada com `.invoke()`.
   - Adicione um comentário no topo do arquivo indicando claramente que o
     nó gerar_analise (com LLM) será plugado no Prompt 07 entre
     consultar_base_local e o fim do fluxo.

4. ESCREVER TESTES DO GRAFO (tests/test_agent_graph.py)
   Usando `pytest`, cubra pelo menos estes cenários de ponta a ponta,
   chamando `build_graph().invoke({...})`:
   - Pergunta válida sobre cadastro de produtos → `cenario_identificado ==
     "cadastro_produtos"` e `dados_base_local` preenchido.
   - Pergunta válida sobre nota fiscal → mesmo padrão para
     "emissao_nota_fiscal".
   - Pergunta válida sobre cálculo de impostos → mesmo padrão para
     "calculo_impostos".
   - Pergunta vazia ou só com espaços → `resposta_estruturada` presente com
     mensagem de erro de validação, `dados_base_local` continua `None`.
   - Pergunta fora de escopo (ex.: "qual a previsão do tempo hoje?") →
     `cenario_identificado == "fora_de_escopo"` e `resposta_estruturada`
     com mensagem amigável.
   Rode `pytest tests/ -v` e confirme que todos os testes passam,
   incluindo os já existentes do Prompt 05.

5. ATUALIZAR O README.md
   Atualize a seção do fluxo do agente (que hoje está apenas descrita em
   prosa/diagrama no escopo) apontando para os arquivos reais:
   `app/agent/state.py`, `app/agent/nodes.py`, `app/agent/graph.py`. Deixe
   explícito que, nesta versão, o grafo termina em `consultar_base_local`
   e que a geração da análise com LLM entra no próximo prompt.

6. COMMITS SEMÂNTICOS (um por etapa concluída)
   1. feat: adiciona o estado do agente (AgentState)
   2. feat: implementa nós determinísticos de validação e identificação de cenário
   3. feat: monta o grafo langgraph com arestas condicionais
   4. test: adiciona testes de ponta a ponta do grafo
   5. docs: documenta a estrutura do grafo no README

7. ENVIAR A BRANCH E ABRIR O PULL REQUEST
   git push -u origin feature/grafo-langgraph-estado

   Abra o PR direcionado para develop:
     Título: "feat: estado e esqueleto do grafo LangGraph"
     Corpo no mesmo padrão dos PRs anteriores (Contexto / O que foi feito /
     Fora do escopo / Checklist), destacando em "Fora do escopo":
       - Nenhuma chamada a get_llm() ou a qualquer provedor de LLM foi feita
       - O nó gerar_analise ainda não existe; o grafo termina em
         consultar_base_local
       - A interface web ainda não consome este grafo

8. VALIDAÇÃO FINAL
   Mostre a saída de `pytest tests/ -v`, `git log --oneline --graph` e
   `git status`, confirmando que:
   - Todos os testes passam (incluindo os da ferramenta do Prompt 05);
   - Nenhum arquivo em app/agent/ importa app.llm.factory ou qualquer
     client de LLM;
   - Os commits seguem o padrão semântico do projeto.

Não implemente o nó de geração com LLM nesta etapa — isso começa no Prompt 07,
que vai inserir gerar_analise entre consultar_base_local e o fim do fluxo,
usando app.llm.factory.get_llm().
```

## Prompt 7 — 2026-07-15

**Resultado:** Branch `feature/geracao-analise-llm` criada a partir de
`develop`; `app/agent/schemas.py` com o modelo pydantic
`AnaliseEstruturada` (5 blocos, com descrições para
`with_structured_output`); `app/agent/prompts.py` com
`SYSTEM_PROMPT_ANALISE`; nó `gerar_analise` implementado em
`app/agent/nodes.py`, chamando exclusivamente `app.llm.factory.get_llm()`
e capturando qualquer falha do LLM em `GeracaoAnaliseError` (uso
interno/log) sem propagar exceção para fora do nó; grafo atualizado em
`app/agent/graph.py` com o fluxo completo `validar_entrada →
identificar_cenario → consultar_base_local → gerar_analise → fim`;
`tests/test_gerar_analise.py` com 5 testes usando mock de
`app.agent.nodes.get_llm` (grafo completo para os 3 cenários + caminho de
erro), e `tests/test_integration_llm.py` com um teste real opcional,
marcado `@pytest.mark.integration` e excluído da suíte padrão via
`pytest.ini`. README atualizado com o fluxo completo do agente. Todos os
16 testes da suíte padrão passam sem nenhuma API key configurada no
ambiente.

**Prompt integral:**

```
Vamos implementar o nó gerar_analise do grafo: ele recebe o contexto já
recuperado da base local (dados_base_local, do nó consultar_base_local) e a
pergunta do usuário, chama o LLM configurado através de
app.llm.factory.get_llm() e produz a resposta final estruturada nos 5
blocos definidos no escopo do projeto. Esta etapa NÃO deve instanciar
nenhum client de provedor diretamente (ChatGoogleGenerativeAI, ChatAnthropic,
ChatOpenAI) — sempre use get_llm().

Crie a branch a partir de develop:
  git checkout develop
  git pull origin develop
  git checkout -b feature/geracao-analise-llm

Execute as etapas abaixo, nesta ordem:

1. DEFINIR O SCHEMA DE SAÍDA ESTRUTURADA (app/agent/schemas.py)
   Crie um modelo `pydantic` chamado `AnaliseEstruturada` com os 5 blocos
   definidos no escopo (seção 8 do documento de escopo), cada um com uma
   descrição curta (`Field(..., description=...)`) para orientar o LLM:
   - cenario_analisado: str
   - pontos_reforma_relacionados: list[str]
   - impactos_tecnicos_erp: list[str]
   - pontos_atencao: list[str]
   - checklist_tecnico: list[str]
   Esse schema será usado com `with_structured_output`, então as
   descrições de cada campo importam — escreva-as claramente, alinhadas ao
   que já está documentado no escopo.

2. IMPLEMENTAR O PROMPT DE SISTEMA (app/agent/prompts.py)
   Crie uma constante `SYSTEM_PROMPT_ANALISE` (string) que instrui o LLM a:
   - Atuar como assistente técnico de apoio a desenvolvedores/analistas de
     ERP sobre a Reforma Tributária, nos cenários cadastro de produtos,
     emissão de nota fiscal e cálculo de impostos (IBS/CBS);
   - Basear a resposta SOMENTE no contexto fornecido (dados recuperados da
     base local) — nunca inventar informação tributária que não esteja no
     contexto;
   - Preencher os 5 blocos do schema `AnaliseEstruturada` de forma objetiva
     e técnica, em português;
   - Deixar claro, dentro de `pontos_atencao`, quando algo precisa de
     validação com a área fiscal/contábil;
   - Nunca apresentar a resposta como parecer jurídico, fiscal ou contábil
     definitivo.
   Não hardcode o conteúdo do JSON aqui — o contexto (dados_base_local) é
   injetado dinamicamente pelo nó, no passo 3.

3. IMPLEMENTAR O NÓ gerar_analise (em app/agent/nodes.py)
   - Importe `get_llm` de `app.llm.factory`, `AnaliseEstruturada` de
     `app.agent.schemas` e `SYSTEM_PROMPT_ANALISE` de `app.agent.prompts`.
   - Implemente `gerar_analise(state) -> dict`:
     - Monta as mensagens: uma `SystemMessage` com `SYSTEM_PROMPT_ANALISE`
       e uma `HumanMessage` contendo a pergunta do usuário
       (`state["pergunta_usuario"]`) e o contexto recuperado
       (`state["dados_base_local"]`), formatado de forma legível (ex.:
       JSON indentado ou texto estruturado);
     - Obtém o LLM com `llm = get_llm()`;
     - Usa saída estruturada: `llm.with_structured_output(AnaliseEstruturada)`;
     - Invoca o modelo com as mensagens montadas;
     - Em caso de sucesso, salva o resultado em `state["resposta_estruturada"]`
       (via `.model_dump()`);
     - Em caso de erro na chamada ao LLM (exceção de rede, timeout, resposta
       fora do formato esperado), NÃO deixe a exceção propagar: capture,
       adicione uma mensagem amigável a `alertas` (ex.: "Não foi possível
       gerar a análise no momento. Tente novamente em instantes.") e deixe
       `resposta_estruturada` como `None` — a validação final (Prompt 08)
       vai tratar esse caso.
   - Defina uma exceção customizada `GeracaoAnaliseError(Exception)` apenas
     para uso interno/log, se achar necessário — mas o nó em si não deve
     lançar exceção para fora do grafo.

4. INTEGRAR O NÓ AO GRAFO (app/agent/graph.py)
   - Adicione o nó `gerar_analise`.
   - Troque a aresta `consultar_base_local → END` (criada no Prompt 06)
     por `consultar_base_local → gerar_analise → END`.
   - Atualize o comentário que indicava "gerar_analise será plugado no
     Prompt 07" para refletir que isso já foi feito.

5. TESTES COM MOCK DO LLM (tests/test_agent_graph.py e/ou novo arquivo
   tests/test_gerar_analise.py)
   IMPORTANTE: os testes automatizados NÃO podem depender de uma API key
   real nem gastar tokens de nenhum provedor. Para isso:
   - Use `unittest.mock.patch` (ou `monkeypatch`) para substituir
     `app.llm.factory.get_llm` por uma função que retorna um objeto "fake"
     cujo `.with_structured_output(...)` retorna um objeto com `.invoke(...)`
     que devolve uma instância fixa de `AnaliseEstruturada` (dados de
     exemplo, sem chamar API nenhuma).
   - Com esse mock, teste o grafo completo de ponta a ponta para os 3
     cenários válidos, confirmando que `resposta_estruturada` chega
     preenchido com os 5 blocos esperados ao final do fluxo.
   - Teste também o caminho de erro: mock que simula uma exceção ao
     invocar o LLM, e confirme que `alertas` é populado e o grafo não
     quebra (não lança exceção para quem chamou `.invoke()`).
   - Rode `pytest tests/ -v` e confirme que TODOS os testes passam sem
     nenhuma variável de API key configurada no ambiente de teste.

6. (OPCIONAL) TESTE DE INTEGRAÇÃO REAL, ISOLADO DO RESTANTE
   Se quiser validar manualmente contra o Gemini de verdade:
   - Crie um teste separado marcado com `@pytest.mark.integration`
     (registre o marker em `pytest.ini` ou `pyproject.toml`).
   - Configure o `pytest.ini`/`pyproject.toml` para que esse marker seja
     ignorado por padrão (`addopts = -m "not integration"`), rodando
     apenas quando chamado explicitamente com `pytest -m integration`.
   - Esse teste só deve rodar localmente, manualmente, com uma
     GOOGLE_API_KEY real no `.env` — nunca em CI, para não gerar custo
     nem depender de rede.

7. ATUALIZAR O README.md
   - Marque no diagrama/descrição do fluxo do agente que o grafo agora
     está completo: validar_entrada → identificar_cenario →
     consultar_base_local → gerar_analise → fim.
   - Adicione uma nota curta avisando que gerar_analise consome a API do
     provedor configurado em LLM_PROVIDER (Gemini 3 Flash por padrão) e que
     os testes automatizados usam mock, não gastando tokens.

8. COMMITS SEMÂNTICOS (um por etapa concluída)
   1. feat: adiciona schema de saída estruturada da análise (AnaliseEstruturada)
   2. feat: adiciona prompt de sistema do nó de geração
   3. feat: implementa o nó gerar_analise usando get_llm()
   4. feat: integra gerar_analise ao grafo (fluxo completo)
   5. test: adiciona testes do grafo completo com mock do LLM
   6. docs: atualiza README com o fluxo completo do agente

9. ENVIAR A BRANCH E ABRIR O PULL REQUEST
   git push -u origin feature/geracao-analise-llm

   Abra o PR direcionado para develop:
     Título: "feat: geração de análise estruturada via LLM (gerar_analise)"
     Corpo no mesmo padrão dos PRs anteriores (Contexto / O que foi feito /
     Fora do escopo / Checklist), destacando em "Fora do escopo":
       - Validação final formal da resposta (retry em caso de formato
         inesperado) fica para o Prompt 08
       - A interface web ainda não consome este grafo
       - Nenhuma chave de API real foi usada nos testes automatizados

10. VALIDAÇÃO FINAL
    Mostre a saída de `pytest tests/ -v` (sem GOOGLE_API_KEY configurada,
    para provar que os testes não dependem de API real), `git log --oneline
    --graph` e `git status`, confirmando que:
    - Todos os testes passam sem nenhuma chave de API configurada;
    - `app/agent/nodes.py` só acessa o LLM através de `get_llm()`, nunca
      instanciando um client de provedor diretamente;
    - Os commits seguem o padrão semântico do projeto.

Não implemente a validação/retry formal da resposta final nem a interface
web nesta etapa — isso continua nos Prompts 08 e 09.
```

## Prompt 8 — 2026-07-16

**Resultado:** Branch `feature/validacao-resposta` criada a partir de
`develop`; `app/agent/state.py` com o campo `tentativas_geracao` no
`AgentState`; nó `gerar_analise` (em `app/agent/nodes.py`) ajustado para
incrementar `tentativas_geracao` a cada execução, sem alterar o restante
do comportamento do Prompt 07; novos nós `validar_resposta` (com a função
auxiliar `_resposta_e_valida`, que confere os 5 blocos do schema) e
`responder_erro_geracao` (fallback com mensagem amigável, preservando
`alertas`), com a constante `MAX_TENTATIVAS_GERACAO = 2`; grafo atualizado
em `app/agent/graph.py` com o laço `gerar_analise ⇄ validar_resposta` e a
aresta condicional final (sucesso → fim | retry | tentativas esgotadas →
`responder_erro_geracao` → fim); `tests/test_validacao_resposta.py` criado
cobrindo sucesso na 1ª tentativa, retry bem-sucedido na 2ª, esgotamento de
`MAX_TENTATIVAS_GERACAO` tentativas e ausência de loop infinito mesmo com
o LLM sempre falhando; `tests/test_gerar_analise.py` e
`tests/test_agent_graph.py` ajustados para o novo campo
`tentativas_geracao` e para o novo comportamento de fallback após esgotar
retries. Todos os 24 testes da suíte padrão passam sem nenhuma API key
configurada no ambiente. Com este prompt, o grafo do agente fica
funcionalmente completo de ponta a ponta.

**Prompt integral:**

```
Vamos implementar o nó validar_resposta, responsável por conferir se a
resposta estruturada gerada pelo LLM (Prompt 07) está completa e, se não
estiver, acionar uma nova tentativa de geração (retry) antes de desistir e
retornar uma mensagem de erro amigável. NÃO altere a lógica interna do nó
gerar_analise além do necessário para suportar o retry, e não instancie
nenhum client de provedor diretamente — continue usando get_llm().

Crie a branch a partir de develop:
  git checkout develop
  git pull origin develop
  git checkout -b feature/validacao-resposta

Execute as etapas abaixo, nesta ordem:

1. ATUALIZAR O ESTADO (app/agent/state.py)
   Adicione ao `AgentState` o campo:
   - tentativas_geracao: int
   Documente que esse campo controla quantas vezes o nó gerar_analise já
   foi executado, para permitir um número limitado de retries. O valor
   inicial, ao montar o estado de entrada do grafo (na chamada de
   `.invoke({...})`), deve ser 0 — deixe isso documentado no README também
   (passo 6).

2. AJUSTAR O NÓ gerar_analise (app/agent/nodes.py)
   - No início da função, incremente `tentativas_geracao` (trate a
     ausência da chave com `state.get("tentativas_geracao", 0) + 1`) e
     inclua o novo valor no dicionário de retorno do nó.
   - Mantenha o restante do comportamento do Prompt 07 (chamada via
     get_llm(), captura de erro sem propagar exceção).

3. IMPLEMENTAR O NÓ validar_resposta (app/agent/nodes.py)
   - Defina uma constante `MAX_TENTATIVAS_GERACAO = 2` no topo do arquivo
     (ou em app/agent/nodes.py mesmo, próximo ao nó).
   - Implemente uma função auxiliar `_resposta_e_valida(resposta: dict |
     None) -> bool` que retorna True somente se `resposta` não for `None` e
     todos os 5 campos do schema (`cenario_analisado`,
     `pontos_reforma_relacionados`, `impactos_tecnicos_erp`,
     `pontos_atencao`, `checklist_tecnico`) estiverem presentes e não
     vazios (strings não em branco, listas com pelo menos 1 item).
   - Implemente `validar_resposta(state) -> dict`:
     - Verifica `_resposta_e_valida(state.get("resposta_estruturada"))`;
     - Não precisa alterar o estado se a resposta for válida — apenas
       repassa adiante (esse nó existe principalmente para a decisão de
       roteamento do passo 4, e pode adicionar um alerta informativo se
       quiser logar que a validação passou).

4. IMPLEMENTAR O NÓ DE FALLBACK (app/agent/nodes.py)
   - `responder_erro_geracao(state) -> dict`:
     - Monta um `resposta_estruturada` de fallback (mesmo formato
       simplificado usado em responder_entrada_invalida/
       responder_fora_de_escopo do Prompt 06), com uma mensagem como:
       "Não foi possível concluir a análise após múltiplas tentativas.
       Tente novamente em instantes ou reformule sua pergunta."
     - Preserva os `alertas` já acumulados, para fins de diagnóstico.

5. AJUSTAR O GRAFO (app/agent/graph.py)
   - Adicione os nós validar_resposta e responder_erro_geracao.
   - Troque a aresta gerar_analise → END (do Prompt 07) por
     gerar_analise → validar_resposta.
   - Adicione a aresta condicional após validar_resposta:
       - se a resposta for válida → END;
       - se for inválida E tentativas_geracao < MAX_TENTATIVAS_GERACAO →
         volta para gerar_analise (retry);
       - se for inválida E tentativas_geracao >= MAX_TENTATIVAS_GERACAO →
         responder_erro_geracao → END.
   - Atualize os comentários do arquivo para refletir que o fluxo completo
     agora é:
     validar_entrada → identificar_cenario → consultar_base_local →
     gerar_analise ⇄ validar_resposta → (END | responder_erro_geracao → END)

6. ATUALIZAR O README.md
   - Atualize o diagrama/descrição do fluxo do agente incluindo o laço de
     retry entre gerar_analise e validar_resposta, com o limite de
     MAX_TENTATIVAS_GERACAO tentativas.
   - Documente que o estado inicial esperado ao chamar o grafo deve incluir
     `tentativas_geracao: 0` (ou que o código já trata a ausência do campo
     como 0 na primeira execução).

7. TESTES (tests/test_agent_graph.py ou novo tests/test_validacao_resposta.py)
   Usando mock de get_llm() (nunca chamando API real), cubra:
   - Resposta válida na primeira tentativa → grafo encerra com
     resposta_estruturada completo e tentativas_geracao == 1.
   - Resposta inválida na primeira tentativa, válida na segunda (mock com
     `side_effect`/sequência de retornos) → grafo encerra com sucesso e
     tentativas_geracao == 2.
   - Resposta inválida em todas as tentativas (até MAX_TENTATIVAS_GERACAO)
     → grafo encerra via responder_erro_geracao, com resposta_estruturada
     contendo a mensagem de fallback e alertas preenchidos.
   - Confirme que o grafo nunca entra em loop infinito (ou seja, o limite
     de tentativas é respeitado mesmo se o mock sempre falhar).
   Rode `pytest tests/ -v` e confirme que todos os testes passam sem
   nenhuma API key configurada.

8. COMMITS SEMÂNTICOS (um por etapa concluída)
   1. feat: adiciona controle de tentativas ao estado do agente
   2. feat: implementa validar_resposta e responder_erro_geracao
   3. feat: adiciona laço de retry entre gerar_analise e validar_resposta
   4. test: adiciona testes de retry e fallback do grafo completo
   5. docs: atualiza README com o comportamento de validação e retry

9. ENVIAR A BRANCH E ABRIR O PULL REQUEST
   git push -u origin feature/validacao-resposta

   Abra o PR direcionado para develop:
     Título: "feat: validação da resposta final com retry"
     Corpo no mesmo padrão dos PRs anteriores (Contexto / O que foi feito /
     Fora do escopo / Checklist), destacando em "Fora do escopo":
       - A interface web ainda não consome este grafo (fica para o
         Prompt 09)
       - Nenhuma chave de API real foi usada nos testes automatizados

10. VALIDAÇÃO FINAL
    Mostre a saída de `pytest tests/ -v` (sem GOOGLE_API_KEY configurada),
    `git log --oneline --graph` e `git status`, confirmando que:
    - Todos os testes passam, incluindo o cenário de esgotamento de
      tentativas;
    - O grafo sempre termina (nenhum caminho de execução resulta em loop
      infinito);
    - Os commits seguem o padrão semântico do projeto.

Com este prompt, o grafo do agente fica funcionalmente completo de ponta a
ponta (entrada → validação → identificação → consulta → geração →
validação final). O próximo prompt (09) implementa a interface web que
consome esse grafo.
```

## Prompt 9 — 2026-07-16

**Resultado:** Branch `feature/interface-web` criada a partir de
`develop`; `app/web/schemas.py` com `PerguntaRequest` e `AnaliseResponse`;
`app/web/main.py` com `get_graph()` (cacheado via `lru_cache`), `GET
/api/cenarios` (usando `listar_cenarios_disponiveis()`) e `POST
/api/analisar` (monta o estado inicial do grafo, incluindo
`tentativas_geracao: 0`, chama `.invoke()` e retorna `AnaliseResponse`;
exceções inesperadas viram HTTP 500 genérico, sem vazar stack trace),
montando os arquivos estáticos por último; `app/web/static/index.html`,
`style.css` e `app.js` implementando a tela sem nenhum framework
front-end (cabeçalho, campo de pergunta, botões rápidos por cenário,
botão "Analisar impacto", indicador de progresso simples, os 5 cards do
resultado e as ações "Copiar resposta"/"Baixar relatório", via
`navigator.clipboard` e `Blob`); `tests/test_web.py` criado com
`TestClient` e mock de `get_llm`, cobrindo `GET /`, `GET /api/cenarios`,
pergunta válida, pergunta vazia (validação leve do schema e validação do
grafo) e pergunta fora de escopo (6 testes); README atualizado com a
seção "Interface web (FastAPI)" e o comando `uvicorn app.web.main:app
--reload`. Todos os 30 testes da suíte padrão passam sem nenhuma API key
configurada. Com este prompt, o mini-projeto fica funcionalmente completo:
entrada pela interface web → grafo do agente → resposta estruturada
exibida em tela.

**Prompt integral:**

```
Vamos implementar a interface web do ReformaTax Agent: uma API em FastAPI
que expõe o grafo já implementado (build_graph, do Prompt 08) e uma tela
estática (HTML/CSS/JS puro, sem framework front-end) que segue o layout do
mockup já aprovado: nome do projeto, descrição, campo de pergunta, botões
rápidos para os 3 cenários, botão "Analisar impacto", indicação de
progresso, resultado em cards e ações de copiar/baixar.

NÃO altere a lógica do grafo, dos nós ou do LLM nesta etapa — a interface
web é apenas uma camada de apresentação sobre o que já existe. NÃO
implemente streaming de progresso passo a passo do grafo (isso exigiria
Server-Sent Events e acompanhamento granular de cada nó, o que está fora do
escopo do mini-projeto); a indicação de progresso pode ser um indicador
simples de "carregando" enquanto a requisição está em andamento.

Crie a branch a partir de develop:
  git checkout develop
  git pull origin develop
  git checkout -b feature/interface-web

Execute as etapas abaixo, nesta ordem:

1. CRIAR OS SCHEMAS DA API (app/web/schemas.py)
   - `PerguntaRequest` (pydantic): campo `pergunta: str`, com validação de
     tamanho mínimo/máximo compatível com a já existente em
     validar_entrada (não duplique a regra de negócio, apenas evite
     payloads absurdos, ex.: `max_length=1000`).
   - `AnaliseResponse` (pydantic): campos `cenario_identificado: str |
     None`, `resposta_estruturada: dict | None`, `alertas: list[str]`.

2. IMPLEMENTAR A API (app/web/main.py)
   - Crie a instância do FastAPI.
   - Implemente uma função `get_graph()` com `functools.lru_cache` que
     chama `build_graph()` uma única vez (evita reconstruir o grafo a cada
     requisição).
   - Rota `GET /api/cenarios`: retorna a lista de cenários suportados,
     usando `listar_cenarios_disponiveis()` de `app.tools.local_kb`
     (evita duplicar essa lista no front-end).
   - Rota `POST /api/analisar`: recebe `PerguntaRequest`, monta o estado
     inicial do grafo:
       {
         "pergunta_usuario": payload.pergunta,
         "cenario_identificado": None,
         "dados_base_local": None,
         "resposta_estruturada": None,
         "alertas": [],
         "tentativas_geracao": 0,
       }
     chama `get_graph().invoke(estado_inicial)` e retorna um
     `AnaliseResponse` com os campos relevantes do estado final.
   - Trate exceções inesperadas do `.invoke()` (que não deveriam
     acontecer, já que os nós tratam seus próprios erros — mas proteja
     mesmo assim) retornando HTTP 500 com uma mensagem genérica amigável,
     sem vazar stack trace para o cliente.
   - Monte os arquivos estáticos da etapa 3 com
     `app.mount("/", StaticFiles(directory="app/web/static", html=True),
     name="static")`, registrado por último (depois das rotas /api/*).

3. CRIAR A INTERFACE ESTÁTICA (app/web/static/)
   Crie três arquivos — index.html, style.css, app.js — implementando a
   tela conforme o mockup já validado:
   - index.html:
     - Cabeçalho com nome do projeto e descrição curta;
     - Textarea para a pergunta do usuário;
     - Três botões rápidos (um por cenário). Ao clicar em um botão rápido,
       preencha a textarea com uma pergunta de exemplo representativa
       daquele cenário (não crie um campo separado de "cenário forçado" —
       o backend continua identificando o cenário a partir do texto da
       pergunta, como já implementado no Prompt 06);
     - Botão "Analisar impacto";
     - Uma área de status/progresso simples (ex.: texto "Analisando..."
       com um spinner ou barra indeterminada), visível apenas enquanto a
       requisição está em andamento;
     - Área de resultado, inicialmente vazia, com os 5 cards (mesmos
       títulos usados no schema: Cenário analisado, Pontos da reforma
       relacionados, Impactos técnicos no ERP, Pontos de atenção,
       Checklist técnico);
     - Botões "Copiar resposta" e "Baixar relatório", habilitados somente
       depois que houver um resultado.
   - style.css: estilos simples e limpos, coerentes com uma "ferramenta
     interna de apoio técnico" (não precisa reproduzir pixel a pixel o
     mockup, mas deve manter a mesma estrutura de elementos e hierarquia
     visual).
   - app.js, sem nenhum framework, implementando:
     - Ao carregar a página, buscar `GET /api/cenarios` (opcional, só se
       quiser popular dinamicamente os textos/labels dos botões);
     - Ao clicar em "Analisar impacto": desabilitar o botão, mostrar a
       área de progresso, chamar `POST /api/analisar` com
       `{ "pergunta": <valor da textarea> }`;
     - Ao receber a resposta:
       - Se `alertas` não estiver vazio e `resposta_estruturada` for nulo
         ou parcial, exibir os alertas como mensagem amigável (não como
         cards);
       - Se `resposta_estruturada` vier completo, preencher os 5 cards
         (listas devem ser renderizadas como `<ul><li>`, não como texto
         corrido);
       - Esconder a área de progresso e reabilitar o botão em qualquer
         caso (sucesso ou erro).
     - Botão "Copiar resposta": monta uma versão em texto plano de todos
       os blocos e usa `navigator.clipboard.writeText`;
     - Botão "Baixar relatório": monta o mesmo texto plano e dispara o
       download de um arquivo `.txt` (ou `.md`) usando `Blob` + link
       temporário — sem depender de nenhuma biblioteca externa nem gerar
       PDF nesta versão.

4. ATUALIZAR O requirements.txt (se necessário)
   Confirme que `fastapi` e `uvicorn` já estão presentes (adicionados no
   Prompt 01/03); não é necessário adicionar Jinja2 ou outro motor de
   templates, já que o front-end é servido como arquivos estáticos.

5. ATUALIZAR O README.md
   - Adicione uma seção "Como executar a interface web", com o comando
     `uvicorn app.web.main:app --reload` e a URL local
     (`http://127.0.0.1:8000`);
   - Deixe claro que a indicação de progresso é simplificada (spinner/
     texto), sem acompanhamento granular de cada nó do grafo nesta versão
     — cite isso como uma possível evolução futura;
   - Adicione uma captura de tela (pode referenciar o arquivo
     `reformatax_tela_interacao.png` já existente) ou descreva brevemente
     a tela.

6. TESTES (tests/test_web.py)
   Usando `fastapi.testclient.TestClient` e o mesmo padrão de mock do LLM
   usado nos Prompts 07/08 (nunca chamando API real):
   - `GET /` retorna 200 e contém o nome do projeto no HTML;
   - `GET /api/cenarios` retorna os 3 cenários esperados;
   - `POST /api/analisar` com uma pergunta válida (mock do LLM retornando
     uma AnaliseEstruturada de exemplo) retorna 200 com
     `resposta_estruturada` completo;
   - `POST /api/analisar` com pergunta vazia retorna `alertas` preenchido
     e `resposta_estruturada` nulo ou com mensagem de validação;
   - `POST /api/analisar` com uma pergunta fora de escopo retorna o
     comportamento esperado do nó responder_fora_de_escopo.
   Rode `pytest tests/ -v` e confirme que todos os testes passam sem
   nenhuma API key configurada.

7. COMMITS SEMÂNTICOS (um por etapa concluída)
   1. feat: adiciona API FastAPI que expõe o grafo do agente
   2. feat: adiciona interface web estática (HTML/CSS/JS)
   3. feat: implementa ações de copiar resposta e baixar relatório
   4. test: adiciona testes da API web com mock do LLM
   5. docs: documenta como executar a interface web no README

8. ENVIAR A BRANCH E ABRIR O PULL REQUEST
   git push -u origin feature/interface-web

   Abra o PR direcionado para develop:
     Título: "feat: interface web (FastAPI) consumindo o grafo do agente"
     Corpo no mesmo padrão dos PRs anteriores (Contexto / O que foi feito /
     Fora do escopo / Checklist), destacando em "Fora do escopo":
       - Progresso passo a passo em tempo real (SSE/streaming) do grafo
       - Geração de relatório em PDF (o download é em texto simples/.md)
       - Autenticação/login de usuários

9. VALIDAÇÃO FINAL
   Mostre a saída de `pytest tests/ -v` (sem GOOGLE_API_KEY configurada),
   `git log --oneline --graph` e `git status`, confirmando que:
   - Todos os testes passam;
   - Nenhuma chave de API é exposta no HTML/JS servido ao navegador (o
     acesso ao LLM continua acontecendo apenas no backend, via
     app.llm.factory.get_llm());
   - Os commits seguem o padrão semântico do projeto.

Com este prompt, o mini-projeto fica funcionalmente completo: entrada pela
interface web → grafo do agente → resposta estruturada exibida em tela. O
próximo prompt (10) foca em testes finais, exemplos de entrada/saída no
README e revisão do checklist de entrega.
```

## Prompt 10 — 2026-07-16

**Resultado:** Branch `chore/revisao-final-entrega` criada a partir de
`develop`. Cobertura de testes formalizada em `pytest.ini`
(`--cov=app --cov-report=term-missing` nos `addopts`, além do marker
`integration` e `-m "not integration"` já existentes desde o Prompt 07);
corrigido `tests/test_agent_graph.py`, que nunca mockava `get_llm()` e
passou a fazer chamadas reais ao Gemini assim que uma API key válida
existiu no `.env` local — adicionada uma fixture `autouse` que mocka
`get_llm`, garantindo que a suíte padrão nunca dependa de nenhuma API key
(suíte completa caiu de ~45s para ~5s). `requirements.txt` com as versões
fixadas via `pip freeze` (incluindo `pytest`/`pytest-cov`). Corrigido um
bug encontrado em teste manual: o modelo padrão do projeto
(`gemini-3-flash`) nunca existiu na API do Gemini (confirmado via
`ListModels`, retornava 404) — atualizado para `gemini-3.5-flash` em
`.env.example`, `app/config.py` e no README. README atualizado com
exemplos reais de entrada/saída (um por cenário, obtidos manualmente via
chamada real ao LLM, nunca em teste automatizado), seção "Limitações da
solução", seção "Principais decisões tomadas" (exigida pelo checklist
oficial e que ainda não existia), e revisão de trechos desatualizados
(Status, descrição do problema, estrutura de pastas, menções residuais ao
nome de modelo antigo). Placeholder `docs/apresentacao/.gitkeep` removido
— `reformatax_apresentacao.pptx` (2 slides, confirmado via inspeção do
zip do `.pptx`) já ocupa o lugar dele. Checklist oficial de entrega
conferido: nenhuma chave/token versionado em nenhum commit do histórico,
`.gitignore` cobre `.env`/`__pycache__`/ambientes virtuais/relatórios de
cobertura, `.env.example` atualizado com as variáveis reais de multi-LLM,
e o README contém todas as seções exigidas. Fora desta branch, também foi
aberta separadamente a branch `fix/spinner-e-botoes-invisiveis` (a partir
de `develop`), corrigindo dois bugs de UI encontrados em teste manual da
interface web do Prompt 09 (spinner de progresso sempre visível por causa
de `display` fixo sobrescrevendo o atributo `hidden`; texto invisível nos
botões "Copiar resposta"/"Baixar relatório" no modo escuro do sistema).
Todos os 30 testes da suíte padrão passam em ~5s, sem nenhuma API key
configurada.

**Prompt integral:**

```
Vamos fechar o mini-projeto: revisar a cobertura de testes, fixar as
dependências, documentar exemplos reais de entrada/saída, conferir o
checklist oficial de entrega e preparar a branch main para a submissão
final. Esta etapa NÃO deve alterar a lógica do agente, dos nós ou da API —
é uma etapa de consolidação e documentação sobre o que já foi implementado
nos Prompts 01 a 09.

Crie a branch a partir de develop:
  git checkout develop
  git pull origin develop
  git checkout -b chore/revisao-final-entrega

Execute as etapas abaixo, nesta ordem:

1. FORMALIZAR CONFIGURAÇÃO DO PYTEST (pyproject.toml ou pytest.ini)
   - Registre o marker "integration" (do teste opcional criado no
     Prompt 07) para não gerar warning.
   - Configure `addopts = -m "not integration"` como padrão, para que
     `pytest` (sem argumentos) NUNCA tente chamar uma API real.
   - Se estiver usando pytest-cov, adicione `--cov=app --cov-report=term-missing`
     aos addopts (opcional) e adicione `pytest-cov` ao requirements.txt.
   - Rode `pytest tests/ -v` e confirme que:
     - Todos os testes dos Prompts 05 a 09 continuam passando juntos, sem
       conflito entre eles (ex.: cache do `get_graph()`/`get_settings()`
       vazando estado de um teste para outro — se isso acontecer, ajuste
       os testes para resetar caches entre execuções, ex.: com
       `get_settings.cache_clear()` em um fixture);
     - Nenhum teste depende de GOOGLE_API_KEY (ou de qualquer outra chave)
       estar configurada no ambiente.

2. FIXAR AS VERSÕES DO requirements.txt
   - Em um ambiente virtual limpo, rode `pip install -r requirements.txt`.
   - Gere as versões efetivamente instaladas (`pip freeze`) e atualize o
     requirements.txt fixando a versão exata de cada dependência direta
     já listada (langgraph, langchain, langchain-core,
     langchain-google-genai, langchain-anthropic, langchain-openai,
     python-dotenv, pydantic, pydantic-settings, fastapi, uvicorn,
     pytest, pytest-cov), no formato `pacote==versão`.
   - Substitua o comentário antigo ("fixar versões após o primeiro teste")
     por um comentário indicando a data em que as versões foram fixadas.

3. ADICIONAR EXEMPLOS REAIS DE ENTRADA E SAÍDA NO README
   Esta é a única etapa de todo o roadmap em que uma chamada REAL ao LLM é
   necessária — feita manualmente por você, uma única vez por cenário,
   nunca dentro de um teste automatizado:
   - Configure um `.env` local com uma GOOGLE_API_KEY válida (não
     versionado).
   - Rode a interface web localmente (ou chame `POST /api/analisar`
     diretamente via curl/httpie) com uma pergunta real para cada um dos 3
     cenários.
   - Copie as respostas reais obtidas e adicione ao README.md, na seção
     "Exemplos de entrada e saída", um exemplo por cenário, no formato:
     pergunta enviada → JSON (ou resumo estruturado) da resposta recebida.
   - Adicione também um exemplo de requisição via curl, por exemplo:
     curl -X POST http://127.0.0.1:8000/api/analisar \
       -H "Content-Type: application/json" \
       -d '{"pergunta": "Quais impactos no cadastro de produtos do ERP?"}'
   - Não deixe nenhuma chave de API nesses exemplos.

4. ADICIONAR SEÇÃO "LIMITAÇÕES DA SOLUÇÃO" NO README
   Com base na seção "fora do escopo" do docs/escopo.md, resuma no
   README as limitações desta primeira versão, por exemplo:
   - Suporta apenas 3 cenários (cadastro de produtos, emissão de NF-e,
     cálculo de IBS/CBS);
   - Sem busca semântica/RAG — a base local é consultada por chave exata
     de cenário;
   - Identificação de cenário por palavras-chave simples, não por LLM;
   - Sem histórico persistente de consultas nem login de usuários;
   - Progresso da análise exibido de forma simplificada (sem streaming
     passo a passo);
   - Máximo de 2 tentativas de geração antes de retornar erro amigável;
   - Não substitui parecer jurídico, fiscal ou contábil.

5. REVISAR docs/prompts.md
   Confirme que os 10 prompts (deste roadmap, do 01 ao 10) estão
   registrados em ordem, cada um com pelo menos: número, título curto,
   branch usada e data (ou apenas a ordem, se preferir não usar datas).
   Se algum prompt executado anteriormente não foi registrado, adicione-o
   agora.

6. ORGANIZAR ARTEFATOS DE APRESENTAÇÃO
   - Confirme que a apresentação em slides (arquivo .pptx com até 2
     slides) está dentro de docs/apresentacao/, substituindo o
     placeholder .gitkeep criado no Prompt 01.
   - Se a imagem do mockup da tela (reformatax_tela_interacao.png) ainda
     não estiver no repositório, adicione-a em docs/ (ex.:
     docs/tela-interacao.png) e referencie-a na seção de interface web do
     README.

7. CONFERIR O CHECKLIST OFICIAL DE ENTREGA
   Percorra item a item o checklist final do documento do mini-projeto
   (repositório e organização; agente e implementação; ferramentas,
   contexto e validação; README.md e prompts; apresentação; submissão) e
   corrija qualquer item pendente. Em especial, confirme:
   - Nenhuma chave, token ou informação sensível está versionada;
   - .gitignore continua cobrindo .env, __pycache__, ambientes virtuais;
   - .env.example está atualizado com todas as variáveis realmente usadas
     pelo projeto (incluindo as de multi-LLM do Prompt 04);
   - README.md contém: nome do projeto, descrição do problema, objetivo do
     agente, explicação do fluxo com LangGraph, ferramenta utilizada,
     instruções para executar o projeto, exemplo de entrada, exemplo de
     saída, principais decisões tomadas e limitações da solução.

8. COMMITS SEMÂNTICOS (um por etapa concluída)
   1. test: adiciona configuração de cobertura e marcadores do pytest
   2. build: fixa versões das dependências no requirements.txt
   3. docs: adiciona exemplos reais de entrada e saída no README
   4. docs: adiciona seção de limitações da solução no README
   5. chore: organiza apresentação e mockup dentro de docs/
   6. docs: revisa docs/prompts.md com o histórico completo de prompts

9. ENVIAR A BRANCH E ABRIR O PULL REQUEST PARA DEVELOP
   git push -u origin chore/revisao-final-entrega

   Abra o PR direcionado para develop:
     Título: "chore: revisão final e preparação para entrega"
     Corpo no mesmo padrão dos PRs anteriores (Contexto / O que foi feito /
     Checklist), marcando explicitamente no checklist do PR os itens do
     checklist oficial do mini-projeto conferidos no passo 7.

10. RELEASE FINAL: PR DE develop PARA main
    Só execute este passo depois que este PR (e todos os anteriores) já
    estiverem revisados e mesclados em develop:
      git checkout develop
      git pull origin develop
      git checkout main
      git pull origin main
    Abra o PR final:
      gh pr create --base main --head develop \
        --title "release: v1.0.0 — entrega do mini-projeto ReformaTax Agent" \
        --body "Versão final do mini-projeto avaliativo, consolidando os
    10 prompts registrados em docs/prompts.md: estrutura inicial,
    configuração multi-LLM (Gemini 3 Flash como padrão), ferramenta de
    consulta à base local, grafo LangGraph completo com validação/retry, e
    interface web."
    Se preferir, após o merge, crie uma tag `v1.0.0` na branch main para
    marcar a entrega.

11. VALIDAÇÃO FINAL
    Mostre a saída de `pytest tests/ -v`, `git log --oneline --graph
    --all` e `git status`, confirmando que:
    - Todos os testes passam, sem nenhuma API key configurada;
    - O link do repositório está acessível e a branch main reflete a
      versão final, caso o passo 10 já tenha sido concluído;
    - Nada sensível foi versionado em nenhum momento do histórico.

Este é o último prompt do roadmap principal. Qualquer melhoria adicional
(RAG, busca semântica, histórico de consultas, novos cenários,
integrações externas) fica para uma evolução futura fora deste
mini-projeto, conforme já registrado na seção 15 do escopo.
```
