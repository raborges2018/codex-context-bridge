"""Mapeia intenção da UI para instruções objetivas ao resumo offline."""

INTENT_OPTIONS = [
    "Continuar desenvolvimento no Claude",
    "Explicar alterações feitas pelo Codex",
    "Encontrar bugs e riscos",
    "Preparar prompt para próxima tarefa",
    "Resumir decisões técnicas",
    "Gerar contexto mínimo",
    "Análise livre",
]

_INTENT_QUERY_MAP = {
    "Continuar desenvolvimento no Claude": "next steps TODO FIXME implementação build test",
    "Explicar alterações feitas pelo Codex": "modified created deleted commit PR branch arquivos",
    "Encontrar bugs e riscos": "ERROR Exception failed traceback warning risco bug",
    "Preparar prompt para próxima tarefa": "next step TODO action task prompt",
    "Resumir decisões técnicas": "decisão decisão técnica arquitetura padrão estratégia",
    "Gerar contexto mínimo": "resumo essencial objetivo estado atual",
    "Análise livre": "overview contexto técnico",
}

_INTENT_ACTION_MAP = {
    "Continuar desenvolvimento no Claude": "Continue o desenvolvimento a partir do estado atual e implemente o próximo passo técnico mais crítico.",
    "Explicar alterações feitas pelo Codex": "Explique objetivamente as alterações realizadas, com foco em impacto técnico e arquivos envolvidos.",
    "Encontrar bugs e riscos": "Faça uma revisão focada em bugs, exceções, falhas de build/teste e riscos de regressão.",
    "Preparar prompt para próxima tarefa": "Transforme o estado atual em uma próxima tarefa clara, curta e executável.",
    "Resumir decisões técnicas": "Consolide as decisões técnicas já evidenciadas e destaque implicações práticas.",
    "Gerar contexto mínimo": "Use apenas o mínimo contexto necessário para permitir continuidade segura da tarefa.",
    "Análise livre": "Analise o contexto de forma geral e proponha o próximo passo mais útil.",
}


def resolve_intent_query(intent: str) -> str:
    return _INTENT_QUERY_MAP.get(intent, _INTENT_QUERY_MAP["Análise livre"])


def resolve_next_action(intent: str) -> str:
    return _INTENT_ACTION_MAP.get(intent, _INTENT_ACTION_MAP["Análise livre"])
