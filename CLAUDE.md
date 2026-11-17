# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Comandos

Ambiente (Python 3.13, gerenciado com uv):

```bash
uv sync --frozen          # instala as dependências do uv.lock
uv add <pacote>           # adiciona dependência (atualiza pyproject.toml e uv.lock)
uv run jupyter lab        # abre o Jupyter Lab
uv run --project ../.. mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000   # interface do MLflow; rode em notebooks/03-MLFlow
```

Executar um notebook sem abrir a interface (útil para checar se ele roda do início ao fim):

```bash
cd notebooks/01-LLMs
uv run --project ../.. jupyter nbconvert --to notebook --execute --stdout "02-Chamada simples - Langchain.ipynb"
```

Rode a partir da pasta do notebook: o `05` de `01-LLMs` grava `historico_chat.db`, e os notebooks de `03-MLFlow` gravam `mlflow.db` no diretório atual.

Não há build, lint nem suíte de testes configurados. Não invente esses comandos.

## Configuração

- `.env` na raiz (ignorado pelo git) com `OPENAI_API_KEY` e `OPENAI_MODEL`. `.env.example` é o modelo.
- Os notebooks leem o `.env` com `load_dotenv(find_dotenv())`, que sobe pelas pastas até achar o arquivo. O modelo padrão é `gpt-5-mini`.
- `main.py` é um placeholder e não é usado pelos notebooks.

## Arquitetura

O repositório é uma série de estudos sobre LLMs, não uma aplicação. O código útil está em `notebooks/01-LLMs/`, numerado em ordem de complexidade:

1. `01` chama a API da OpenAI direto com o pacote `openai` (Responses API).
2. `02` faz a mesma chamada com LangChain (`ChatOpenAI` do `langchain-openai`).
3. `03` usa templates (`ChatPromptTemplate`), composição LCEL com `|`, `batch`, saída estruturada (`with_structured_output` com Pydantic) e `PydanticOutputParser`.
4. `04` adiciona memória com `RunnableWithMessageHistory`, `MessagesPlaceholder` e `InMemoryChatMessageHistory`, com isolamento por `session_id`.
5. `05` troca o histórico em memória por uma classe `HistoricoSQLite` que herda de `BaseChatMessageHistory` e persiste em SQLite com `sqlite3` da biblioteca padrão.
6. `06` usa tool calling com `@tool` e `bind_tools`.

`notebooks/02-Langgraph/` estuda LangGraph, também numerado em ordem de complexidade:

1. `01` chamada simples com `StateGraph`.
2. `02` memória entre turnos com `MessagesState`.
3. `03` estado próprio e nós.
4. `04` agente com ferramentas: `ToolNode` e aresta condicional.
5. `05` human-in-the-loop com `interrupt`, `Command(resume=...)` e `MemorySaver`.
6. `06` subgrafos: um coordenador delega a agentes que são grafos compilados.
7. `07` RAG: recuperação, avaliação, reescrita da consulta e geração com citação.

`notebooks/03-MLFlow/` versiona prompts em YAML no MLflow. Usa `sqlite:///mlflow.db`, porque o Prompt Registry não funciona com `mlruns`. A pasta `prompts/` guarda o YAML gerado pelo notebook; o `.gitkeep` mantém a pasta no git.

Cada notebook é independente. A configuração do modelo é repetida em cada um, sem módulo compartilhado. Ao criar um notebook novo, siga o mesmo padrão em vez de extrair código comum, a menos que o usuário peça.

Os notebooks estão em português e os títulos e explicações seguem esse idioma. O kernel é `python3` do ambiente `.venv`, exibido como `loop-engineering-study`.

Dependências declaradas em `pyproject.toml`: `langchain`, `langchain-openai`, `langgraph`, `openai`, `mlflow`, `jupyterlab`, `jupyter-code-server` e `python-dotenv`.
