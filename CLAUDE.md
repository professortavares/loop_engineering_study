# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Comandos

Ambiente (Python 3.13, gerenciado com uv):

```bash
uv sync --frozen          # instala as dependências do uv.lock
uv add <pacote>           # adiciona dependência (atualiza pyproject.toml e uv.lock)
uv run jupyter lab        # abre o Jupyter Lab
```

Executar um notebook sem abrir a interface (útil para checar se ele roda do início ao fim):

```bash
cd notebooks/01-LLMs
uv run --project ../.. jupyter nbconvert --to notebook --execute --stdout "02-Chamada simples - Langchain.ipynb"
```

Rode a partir da pasta do notebook: o `05` grava `historico_chat.db` no diretório atual.

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

Cada notebook é independente. A configuração do modelo é repetida em cada um, sem módulo compartilhado. Ao criar um notebook novo, siga o mesmo padrão em vez de extrair código comum, a menos que o usuário peça.

Os notebooks estão em português e os títulos e explicações seguem esse idioma. O kernel é `python3` do ambiente `.venv`, exibido como `loop-engineering-study`.

Dependências declaradas em `pyproject.toml`: `langchain`, `langchain-openai`, `langgraph`, `openai`, `jupyterlab`, `jupyter-code-server` e `python-dotenv`.
