"""Agente LangGraph versionado com MLflow (models from code).

O grafo tem três nós:
- classificar: escolhe a categoria da pergunta (usa o prompt `langgraph-classificador`);
- responder: responde à pergunta de devolução ou entrega (usa o prompt `langgraph-responder`);
- fora_do_escopo: responde com uma mensagem fixa quando a pergunta não é atendida.

As URIs dos prompts ficam fixas aqui, então cada versão do agente usa versões conhecidas.
O `autolog` do LangChain grava um trace a cada invocação.
"""

import os

import mlflow
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph
from mlflow.models import set_model

PROMPT_CLASSIFICADOR = "prompts:/langgraph-classificador/1"
PROMPT_RESPONDER = "prompts:/langgraph-responder/1"
NOME_LOJA = "Loja Exemplo"
CATEGORIAS_ATENDIDAS = ("devolucao", "entrega")

mlflow.langchain.autolog()

llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-5-mini"), api_key=os.getenv("OPENAI_API_KEY"))

prompt_classificador = mlflow.genai.load_prompt(PROMPT_CLASSIFICADOR)
prompt_responder = mlflow.genai.load_prompt(PROMPT_RESPONDER)


class Estado(MessagesState):
    categoria: str


def pergunta_atual(estado: Estado) -> str:
    return estado["messages"][-1].content


def classificar(estado: Estado) -> dict:
    mensagens = prompt_classificador.format(pergunta=pergunta_atual(estado))
    categoria = llm.invoke(mensagens).content.strip().lower()
    if categoria not in CATEGORIAS_ATENDIDAS:
        categoria = "outro"
    return {"categoria": categoria}


def responder(estado: Estado) -> dict:
    mensagens = prompt_responder.format(
        nome_loja=NOME_LOJA,
        categoria=estado["categoria"],
        pergunta=pergunta_atual(estado),
    )
    resposta = llm.invoke(mensagens)
    return {"messages": [AIMessage(content=resposta.content)]}


def fora_do_escopo(estado: Estado) -> dict:
    texto = "Só consigo ajudar com devoluções e entregas. Vou encaminhar sua pergunta a um atendente."
    return {"messages": [AIMessage(content=texto)]}


def rotear(estado: Estado) -> str:
    return "responder" if estado["categoria"] in CATEGORIAS_ATENDIDAS else "fora_do_escopo"


construtor = StateGraph(Estado)
construtor.add_node("classificar", classificar)
construtor.add_node("responder", responder)
construtor.add_node("fora_do_escopo", fora_do_escopo)

construtor.add_edge(START, "classificar")
construtor.add_conditional_edges("classificar", rotear, ["responder", "fora_do_escopo"])
construtor.add_edge("responder", END)
construtor.add_edge("fora_do_escopo", END)

grafo_agente = construtor.compile()

set_model(grafo_agente)
