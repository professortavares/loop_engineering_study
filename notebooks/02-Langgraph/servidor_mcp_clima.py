"""Servidor MCP mínimo de exemplo: consulta de temperatura de cidades.

Usado pelo notebook 08-MCP - Langgraph.ipynb.

Modos de execução:
- http (padrão): o servidor fica no ar em http://127.0.0.1:8000/mcp.
  Rode em um terminal separado e deixe aberto enquanto usa o notebook.
- stdio: o cliente inicia o servidor como subprocesso e conversa pela entrada e saída padrão.

Os dados são simulados em um dicionário para o exemplo não depender de internet.

Atenção: no transporte stdio, o stdout é o canal do protocolo. Não use print() aqui.
"""

import argparse
import json

from mcp.server.fastmcp import FastMCP

TEMPERATURAS = {
    "são paulo": {"temperatura_c": 24.5, "condicao": "parcialmente nublado"},
    "rio de janeiro": {"temperatura_c": 29.0, "condicao": "ensolarado"},
    "curitiba": {"temperatura_c": 16.2, "condicao": "chuva fraca"},
    "porto alegre": {"temperatura_c": 19.8, "condicao": "nublado"},
}

mcp = FastMCP("clima", host="127.0.0.1", port=8000)


@mcp.tool()
def obter_temperatura(cidade: str) -> str:
    """Retorna a temperatura atual, em graus Celsius, e a condição do tempo de uma cidade brasileira."""
    dados = TEMPERATURAS.get(cidade.lower().strip())
    if dados is None:
        return json.dumps({"cidade": cidade, "erro": "cidade não encontrada"}, ensure_ascii=False)
    return json.dumps({"cidade": cidade, **dados}, ensure_ascii=False)


@mcp.tool()
def listar_cidades() -> str:
    """Lista as cidades disponíveis para consulta de temperatura."""
    return json.dumps(sorted(TEMPERATURAS), ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor MCP de clima de exemplo.")
    parser.add_argument(
        "--transporte",
        choices=["http", "stdio"],
        default="http",
        help="http: servidor sempre no ar (padrão). stdio: iniciado pelo cliente.",
    )
    args = parser.parse_args()

    if args.transporte == "http":
        print("Servidor MCP em http://127.0.0.1:8000/mcp (Ctrl+C para encerrar)", flush=True)
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")
