"""Mapeia intenção da UI para instruções objetivas ao modelo."""

INTENT_OPTIONS = [
    "Continuar desenvolvimento no Claude",
    "Explicar alterações feitas pelo Codex",
    "Encontrar bugs e riscos",
    "Preparar prompt para próxima tarefa",
    "Resumir decisões técnicas",
    "Gerar contexto mínimo",
    "Análise livre",
]

_INTENT_MAP = {
    "Continuar desenvolvimento no Claude": "Priorize continuidade de implementação e próximos passos acionáveis.",
    "Explicar alterações feitas pelo Codex": "Explique com clareza o que foi alterado e por quê.",
    "Encontrar bugs e riscos": "Foque em falhas, riscos técnicos e inconsistências.",
    "Preparar prompt para próxima tarefa": "Entregue um prompt pronto para avançar a próxima atividade.",
    "Resumir decisões técnicas": "Extraia e destaque decisões técnicas já tomadas.",
    "Gerar contexto mínimo": "Seja extremamente conciso, mantendo apenas o essencial para continuidade.",
    "Análise livre": "Faça uma síntese equilibrada e fiel das informações.",
}


def resolve_intent_instruction(intent: str) -> str:
    return _INTENT_MAP.get(intent, _INTENT_MAP["Análise livre"])
