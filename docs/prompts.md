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
