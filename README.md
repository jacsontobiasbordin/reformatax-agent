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

## Próximos passos

- Implementação do grafo do agente com LangGraph (`app/agent`).
- Implementação da ferramenta de consulta à base local (`app/tools`).
- Implementação da interface web (`app/web`).
- Escrita dos testes automatizados (`tests`).

Essas etapas serão realizadas em prompts futuros.
