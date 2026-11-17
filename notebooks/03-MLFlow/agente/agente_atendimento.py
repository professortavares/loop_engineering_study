"""Agente de atendimento versionado com MLflow (models from code).

O código fica neste arquivo, versionado no git. A instrução (o prompt já formatado)
e o modelo chegam pelo `model_config` no momento do registro, então cada versão do
agente guarda exatamente o prompt que foi usado.
"""

import os

from mlflow.models import set_model
from mlflow.pyfunc import ChatModel
from mlflow.types.llm import ChatChoice, ChatCompletionResponse, ChatMessage, ChatParams
from openai import OpenAI


class AgenteAtendimento(ChatModel):
    def load_context(self, context):
        config = context.model_config or {}
        self.instrucao = config["instrucao"]
        self.modelo = config.get("modelo", "gpt-5-mini")
        self.cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def predict(self, context, messages: list[ChatMessage], params: ChatParams) -> ChatCompletionResponse:
        historico = [{"role": "system", "content": self.instrucao}]
        historico += [{"role": m.role, "content": m.content} for m in messages]

        resposta = self.cliente.chat.completions.create(model=self.modelo, messages=historico)
        texto = resposta.choices[0].message.content

        return ChatCompletionResponse(
            choices=[ChatChoice(message=ChatMessage(role="assistant", content=texto))]
        )


set_model(AgenteAtendimento())
