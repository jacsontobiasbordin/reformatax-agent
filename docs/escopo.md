# Escopo do Mini-Projeto Avaliativo — ReformaTax Agent

**Disciplina:** IA para Desenvolvedores [T2] — Módulo 2, Semana 05/06
**Assistente de Impacto Técnico da Reforma Tributária em ERP**
**Prazo de entrega:** 20/07/2026 às 22h (via AVA, link do repositório GitHub)
**Peso:** 30% da nota do módulo

---

## 1. Contextualização e alinhamento com a orientação do professor

Este mini-projeto segue a recomendação do professor de tratar o agente como um **"Assistente de Impacto Técnico da Reforma Tributária em ERP"**, com escopo controlado a três cenários — cadastro de produtos, emissão de nota fiscal e cálculo de impostos — em vez de tentar cobrir toda a Reforma Tributária.

O foco desta entrega não é a abrangência do conteúdo tributário, e sim demonstrar de forma sólida os requisitos técnicos do mini-projeto: agente com objetivo claro, entrada definida, fluxo implementado com LangGraph (estado, nós e conexões), ferramenta integrada real e resposta final estruturada.

## 2. Problema escolhido

Com a Reforma Tributária, empresas que utilizam sistemas ERP precisam revisar cadastros, regras fiscais, cálculos e documentos fiscais. Desenvolvedores e analistas de sistemas têm dificuldade em identificar rapidamente quais partes do ERP são impactadas. O ReformaTax Agent apoia essa primeira análise técnica, organizando as informações de forma simples e objetiva.

## 3. Objetivo do agente

Analisar uma dúvida ou cenário informado pelo usuário, relacionado à Reforma Tributária em ERP, e retornar uma resposta estruturada com os possíveis impactos técnicos, pontos de atenção e um checklist prático.

O agente **não** tem como objetivo fornecer parecer jurídico, fiscal ou contábil definitivo — é um apoio técnico inicial para equipes de desenvolvimento e análise de sistemas.

## 4. Escopo da primeira versão (mini-projeto)

Limitado a três cenários, conforme orientação do professor:

1. **Cadastro de produtos** — impactos em NCM, classificação tributária (cClassTrib/CST), parametrizações e informações usadas no cálculo dos impostos.
2. **Emissão de nota fiscal** — impactos na geração de documentos fiscais eletrônicos, campos de IBS/CBS, validações e integração com o leiaute da NF-e/NFC-e.
3. **Cálculo de impostos (IBS/CBS)** — impactos nas regras de cálculo, não cumulatividade, base de cálculo, regras de transição e validações fiscais.

## 5. Fora do escopo desta entrega

Conforme o comentário do professor, os itens abaixo ficam para a evolução do **projeto final do módulo**, não fazendo parte do mini-projeto:

- Cobertura completa de toda a legislação da Reforma Tributária;
- Busca semântica e RAG sobre a base de conhecimento;
- Consulta automática à internet / integração com APIs externas;
- Histórico persistente de consultas e login de usuários;
- Integração com sistemas ERP reais;
- Parecer jurídico, contábil ou fiscal definitivo;
- Suporte a cenários fiscais além dos três definidos.

Manter esse recorte é o que garante que o mini-projeto fique **simples, funcional e bem documentado**, atendendo aos critérios de avaliação sem se estender além do prazo.

## 6. Entrada esperada (requisito 1 do documento oficial)

O usuário informa uma pergunta em linguagem natural ou seleciona um dos três cenários pré-definidos. Exemplos:

- "Quais impactos da Reforma Tributária no cadastro de produtos do ERP?"
- "Tenho uma rotina de emissão de NF-e que calcula ICMS, PIS e COFINS. O que devo revisar?"
- "Como o cálculo de impostos do ERP pode ser afetado pela CBS e IBS?"

## 7. Saída esperada (resposta final estruturada)

O agente retorna uma resposta organizada nos seguintes blocos, atendendo ao requisito de "geração de respostas estruturadas":

1. **Cenário analisado** — resumo da dúvida/situação informada.
2. **Pontos da Reforma Tributária relacionados** — conceitos da base local pertinentes ao cenário.
3. **Possíveis impactos técnicos no ERP** — pontos do sistema que podem exigir revisão.
4. **Pontos de atenção** — itens que precisam de validação com a área fiscal/contábil.
5. **Checklist técnico** — lista prática de verificação para o desenvolvedor/analista.

## 8. Fluxo do agente com LangGraph (estado, nós e conexões)

```
Entrada do usuário
        ↓
Validação da entrada (não vazia, tamanho máximo, tema permitido)
        ↓
Identificação do cenário (cadastro / nota fiscal / cálculo de impostos)
        ↓
Consulta à base local (ferramenta) → data/reforma_tributaria_erp.json
        ↓
Preparação do contexto (montagem do estado com os dados recuperados)
        ↓
Geração da análise (chamada ao LLM com o contexto)
        ↓
Validação da resposta final (estrutura, blocos obrigatórios)
        ↓
Exibição da resposta estruturada na interface web
```

**Estado do grafo (compartilhado entre os nós):**

| Campo | Descrição |
|---|---|
| `pergunta_usuario` | Texto original informado |
| `cenario_identificado` | Um dos três cenários, ou `fora_de_escopo` |
| `dados_base_local` | Trecho do JSON recuperado pela ferramenta |
| `resposta_estruturada` | Resposta final gerada pelo agente |
| `alertas` | Mensagens de validação (ex.: pergunta fora do escopo) |

**Nós principais:** `validar_entrada`, `identificar_cenario`, `consultar_base_local` (ferramenta), `montar_contexto`, `gerar_analise`, `validar_resposta`.

**Conexões:** fluxo sequencial, com desvio condicional em `identificar_cenario` — se o cenário não for reconhecido, o grafo segue para um nó de resposta amigável de "fora de escopo" em vez de seguir para a consulta e geração.

## 9. Ferramenta integrada (requisito obrigatório)

Ferramenta simples e real: leitura do arquivo local `data/reforma_tributaria_erp.json`, que contém as informações resumidas dos três cenários (conceitos, impactos técnicos, pontos de atenção e checklist). A ferramenta recebe o cenário identificado e retorna o trecho correspondente do JSON, que alimenta o estado do agente para a geração da resposta final.

## 10. Contexto/memória durante a execução

Durante a execução de uma única consulta, o agente mantém no estado: a pergunta original, o cenário identificado, os dados recuperados da base local, a resposta gerada e os alertas de validação. Essa memória de curto prazo (dentro da execução do grafo) é suficiente para o escopo do mini-projeto — não há persistência entre sessões nesta versão.

## 11. Validações e segurança básica

- Impedir pergunta vazia;
- Limitar tamanho máximo da entrada;
- Verificar se a pergunta está relacionada a um dos três cenários permitidos, retornando mensagem amigável quando estiver fora do escopo;
- Restringir a ferramenta à leitura do arquivo `data/reforma_tributaria_erp.json`, sem acesso a outros caminhos;
- Não versionar chaves, tokens ou informações sensíveis (uso de `.gitignore` e `.env.example`).

## 12. Interface web

Interface simples com: nome do projeto, breve descrição, campo de pergunta, botões rápidos para os três cenários, botão "Analisar impacto", indicação de progresso, resultado em blocos/cards e opção de copiar a resposta.

## 13. Entregáveis do repositório (conforme requisitos oficiais)

- `README.md` completo (problema, objetivo do agente, fluxo com LangGraph, ferramenta utilizada, instruções de execução, exemplo de entrada/saída, decisões tomadas, limitações);
- Código-fonte do agente implementado com LangGraph;
- Ferramenta integrada (`data/reforma_tributaria_erp.json` + função de consulta);
- Interface web simples;
- `docs/prompts.md` com os principais prompts usados para planejar, implementar, corrigir e melhorar o agente;
- Exemplos de entrada e saída da execução;
- `.gitignore`;
- `.env.example` (se necessário, apenas com nomes de variáveis);
- Apresentação da ideia em até 2 slides (problema, agente, entrada, saída, ferramenta, fluxo geral).

## 14. Mapeamento com os critérios de avaliação

| Critério oficial | Como o escopo atende |
|---|---|
| Versionamento com branches e commits semânticos (1,0) | Commits incrementais durante o desenvolvimento das etapas do fluxo |
| Contribuição individual e produtividade (1,0) | Rastreável via commits, mesmo em projeto individual |
| Organização dos arquivos, documentação e prompts (2,0) | README.md, `docs/prompts.md`, exemplos de entrada/saída completos |
| Ideia do projeto e apresentação (1,0) | Slides com problema, agente, entrada, saída e fluxo |
| Implementação do agente com LangGraph (1,0) | StateGraph com os nós e conexões descritos na seção 8 |
| Uso de ferramenta integrada (1,0) | Leitura real do `data/reforma_tributaria_erp.json` |
| Cuidados básicos de segurança (1,0) | `.gitignore`, `.env.example`, validação de escopo do arquivo lido |
| Contexto, memória e validação básica (2,0) | Estado do grafo (seção 10) + validações da seção 11 |

## 15. Possíveis evoluções (projeto final do módulo)

Conforme indicado pelo professor, após esta primeira versão a solução pode evoluir para: base de conhecimento maior, busca semântica/RAG, histórico persistente de consultas, novos cenários fiscais, integração com APIs externas e conexão com módulos reais de ERP.

## 16. Checklist final de entrega (uso interno da equipe)

- [ ] Repositório criado e acessível no GitHub
- [ ] Código-fonte do agente com LangGraph
- [ ] Estado, nós e conexões implementados e funcionais
- [ ] Ferramenta integrada lendo `data/reforma_tributaria_erp.json`
- [ ] Validações básicas de entrada implementadas
- [ ] Resposta final estruturada nos 5 blocos definidos
- [ ] `README.md` completo
- [ ] `docs/prompts.md` com os prompts principais
- [ ] Exemplos de entrada e saída documentados
- [ ] `.gitignore` e `.env.example` (se aplicável) sem dados sensíveis
- [ ] Slides (até 2) prontos
- [ ] Link do repositório testado antes da submissão no AVA
- [ ] Entrega feita antes de 20/07/2026
