// Interface estática do ReformaTax Agent — HTML/CSS/JS puro, sem
// framework. Toda a lógica do agente (LLM, grafo) roda no backend; este
// arquivo só consome a API em /api/cenarios e /api/analisar.

const CENARIO_INFO = {
  cadastro_produtos: {
    label: "Cadastro de produtos",
    exemplo:
      "Quais impactos da Reforma Tributária no cadastro de produtos do ERP?",
  },
  emissao_nota_fiscal: {
    label: "Emissão de nota fiscal",
    exemplo:
      "Tenho uma rotina de emissão de NF-e que calcula ICMS, PIS e COFINS. O que devo revisar?",
  },
  calculo_impostos: {
    label: "Cálculo de impostos",
    exemplo:
      "Como o cálculo de impostos do ERP pode ser afetado pela CBS e IBS?",
  },
};

const elPergunta = document.getElementById("pergunta");
const elBotoesRapidos = document.getElementById("botoes-rapidos");
const elBtnAnalisar = document.getElementById("btn-analisar");
const elAreaProgresso = document.getElementById("area-progresso");
const elAreaResultado = document.getElementById("area-resultado");
const elAreaAlerta = document.getElementById("area-alerta");
const elCards = document.getElementById("cards");
const elBtnCopiar = document.getElementById("btn-copiar");
const elBtnBaixar = document.getElementById("btn-baixar");

const elCardCenario = document.getElementById("card-cenario");
const elCardPontosReforma = document.getElementById("card-pontos-reforma");
const elCardImpactosErp = document.getElementById("card-impactos-erp");
const elCardPontosAtencao = document.getElementById("card-pontos-atencao");
const elCardChecklist = document.getElementById("card-checklist");

let ultimoRelatorioTexto = "";

async function carregarCenarios() {
  try {
    const resposta = await fetch("/api/cenarios");
    if (!resposta.ok) return;
    const cenarios = await resposta.json();

    cenarios.forEach((cenario) => {
      const info = CENARIO_INFO[cenario] || { label: cenario, exemplo: "" };
      const botao = document.createElement("button");
      botao.type = "button";
      botao.className = "botao-cenario";
      botao.textContent = info.label;
      botao.addEventListener("click", () => {
        elPergunta.value = info.exemplo;
        elPergunta.focus();
      });
      elBotoesRapidos.appendChild(botao);
    });
  } catch (erro) {
    // Botões rápidos são apenas um atalho de UX; se a listagem falhar,
    // o usuário ainda pode digitar a pergunta livremente.
    console.warn("Não foi possível carregar os cenários rápidos.", erro);
  }
}

function preencherLista(elementoUl, itens) {
  elementoUl.innerHTML = "";
  (itens || []).forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    elementoUl.appendChild(li);
  });
}

function montarTextoRelatorio(analise) {
  const linhas = [
    "ReformaTax Agent — Análise de Impacto\n",
    "Cenário analisado:",
    analise.cenario_analisado,
    "",
    "Pontos da reforma relacionados:",
    ...analise.pontos_reforma_relacionados.map((item) => `- ${item}`),
    "",
    "Impactos técnicos no ERP:",
    ...analise.impactos_tecnicos_erp.map((item) => `- ${item}`),
    "",
    "Pontos de atenção:",
    ...analise.pontos_atencao.map((item) => `- ${item}`),
    "",
    "Checklist técnico:",
    ...analise.checklist_tecnico.map((item) => `- ${item}`),
  ];
  return linhas.join("\n");
}

function exibirAlerta(mensagens) {
  elAreaAlerta.textContent = mensagens.join(" ");
  elAreaAlerta.hidden = false;
  elCards.hidden = true;
  elBtnCopiar.disabled = true;
  elBtnBaixar.disabled = true;
  ultimoRelatorioTexto = "";
}

function exibirCards(analise) {
  elCardCenario.textContent = analise.cenario_analisado;
  preencherLista(elCardPontosReforma, analise.pontos_reforma_relacionados);
  preencherLista(elCardImpactosErp, analise.impactos_tecnicos_erp);
  preencherLista(elCardPontosAtencao, analise.pontos_atencao);
  preencherLista(elCardChecklist, analise.checklist_tecnico);

  elAreaAlerta.hidden = true;
  elCards.hidden = false;

  ultimoRelatorioTexto = montarTextoRelatorio(analise);
  elBtnCopiar.disabled = false;
  elBtnBaixar.disabled = false;
}

function respostaEhAnaliseCompleta(respostaEstruturada) {
  return (
    respostaEstruturada &&
    Array.isArray(respostaEstruturada.pontos_reforma_relacionados)
  );
}

async function analisar() {
  const pergunta = elPergunta.value.trim();

  elBtnAnalisar.disabled = true;
  elAreaProgresso.hidden = false;
  elAreaResultado.hidden = true;

  try {
    const resposta = await fetch("/api/analisar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pergunta }),
    });

    const dados = await resposta.json();
    elAreaResultado.hidden = false;

    if (!resposta.ok) {
      exibirAlerta([
        dados.detail || "Não foi possível processar sua pergunta no momento.",
      ]);
      return;
    }

    if (respostaEhAnaliseCompleta(dados.resposta_estruturada)) {
      exibirCards(dados.resposta_estruturada);
    } else if (dados.resposta_estruturada && dados.resposta_estruturada.mensagem) {
      exibirAlerta([dados.resposta_estruturada.mensagem]);
    } else if (dados.alertas && dados.alertas.length > 0) {
      exibirAlerta(dados.alertas);
    } else {
      exibirAlerta(["Não foi possível gerar uma resposta para sua pergunta."]);
    }
  } catch (erro) {
    elAreaResultado.hidden = false;
    exibirAlerta(["Não foi possível conectar ao servidor. Tente novamente."]);
  } finally {
    elAreaProgresso.hidden = true;
    elBtnAnalisar.disabled = false;
  }
}

async function copiarResposta() {
  if (!ultimoRelatorioTexto) return;
  try {
    await navigator.clipboard.writeText(ultimoRelatorioTexto);
  } catch (erro) {
    console.warn("Não foi possível copiar para a área de transferência.", erro);
  }
}

function baixarRelatorio() {
  if (!ultimoRelatorioTexto) return;
  const blob = new Blob([ultimoRelatorioTexto], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "reformatax-analise.txt";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

elBtnAnalisar.addEventListener("click", analisar);
elBtnCopiar.addEventListener("click", copiarResposta);
elBtnBaixar.addEventListener("click", baixarRelatorio);

carregarCenarios();
