# Loop engineering study
Estudos sobre Loop Engineering

## Pré-requisitos

- Python 3.13 (definido em `.python-version`)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) para gerenciar o ambiente e as dependências

## Instalação do ambiente

Clone o repositório e entre na pasta do projeto:

```bash
git clone <url-do-repositorio>
cd loop_engineering_study
```

Instale as dependências a partir do `uv.lock`:

```bash
uv sync --frozen
```

Isso cria o ambiente virtual em `.venv/` com as dependências do `pyproject.toml`
(`jupyterlab`, `langchain`, `langgraph` e `mlflow`), sem alterar o `uv.lock`.

## Iniciando o Jupyter Lab

Dentro da pasta do projeto, rode:

```bash
uv run jupyter lab
```

O Jupyter Lab abre no navegador. Se não abrir sozinho, copie a URL com token que aparece no terminal
(algo como `http://localhost:8888/lab?token=...`) e cole no navegador.

Para parar o servidor, pressione `Ctrl+C` no terminal e confirme com `y`.

## Interface do MLflow

Os notebooks de `notebooks/03-MLFlow/` gravam os prompts num banco SQLite, `mlflow.db`, na pasta do notebook. Para ver os prompts no navegador:

1. Rode o notebook `01-Prompts versionados - MLflow.ipynb` pelo menos uma vez, para criar o banco.
2. Abra um terminal na pasta `notebooks/03-MLFlow` (o caminho do banco é relativo a ela) e rode:

   ```bash
   uv run --project ../.. mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
   ```

3. Abra `http://127.0.0.1:5000` e procure a seção **Prompts**.
4. Pressione `Ctrl+C` no terminal para parar.

Se a porta 5000 estiver ocupada, use outra, como `--port 5055`. O `mlflow.db` e as pastas `mlruns/` e `mlartifacts/` estão no `.gitignore`.

## Servidor MCP de exemplo (notebook 08 do LangGraph)

O notebook `notebooks/02-Langgraph/08-MCP - Langgraph.ipynb` consome um servidor MCP de exemplo, `servidor_mcp_clima.py`, que informa a temperatura de algumas cidades. O servidor precisa estar no ar antes de rodar o notebook.

1. Abra um terminal na pasta `notebooks/02-Langgraph` (o caminho do servidor é relativo a ela) e rode:

   ```bash
   uv run --project ../.. python servidor_mcp_clima.py
   ```

2. Deixe o terminal aberto. O servidor fica disponível em `http://127.0.0.1:8000/mcp`.
3. Rode o notebook. A célula de verificação informa se o servidor está respondendo.
4. Pressione `Ctrl+C` no terminal para parar o servidor.

Se a porta 8000 estiver ocupada, feche o processo que a está usando antes de iniciar o servidor. Para o modo em que o cliente inicia o servidor sozinho, use `--transporte stdio`, mas nesse caso o notebook precisa ser ajustado.

## VS Code Web no Jupyter Lab (jupyter-code-server)

O plugin [`jupyter-code-server`](https://pypi.org/project/jupyter-code-server/) abre o VS Code Web
(via [code-server](https://github.com/coder/code-server)) dentro do Jupyter Lab. Ele já está listado
em `pyproject.toml`, então é instalado junto com `uv sync`.

### Requisito: code-server

O plugin não instala o code-server, então ele precisa estar disponível no sistema.
Siga a [documentação oficial de instalação](https://coder.com/docs/code-server/install).
Para conferir:

```bash
code-server --version
```

### Descobrir a senha

Por padrão, o code-server usa login por senha. A senha fica no arquivo de configuração
`~/.config/code-server/config.yaml`. Para vê-la:

```bash
grep '^password:' ~/.config/code-server/config.yaml
```

Para trocar a senha, edite a linha `password:` nesse arquivo e reinicie o Jupyter Lab.

### Usar

1. Inicie o Jupyter Lab com `uv run jupyter lab`.
2. No Launcher, clique no ícone **VSCode Web IDE**.
3. Informe a senha encontrada acima.

Por padrão, o VS Code Web abre na sua pasta `HOME`. Para mudar a pasta, defina a variável
`CODE_WORKING_DIRECTORY` antes de iniciar o Jupyter Lab, por exemplo:

```bash
CODE_WORKING_DIRECTORY=/caminho/da/pasta uv run jupyter lab
```

Para desativar o login por senha (apenas em ambientes confiáveis), defina `CODE_DISABLE_PASSWORD=true`.
