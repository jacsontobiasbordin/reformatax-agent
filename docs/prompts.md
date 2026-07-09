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
