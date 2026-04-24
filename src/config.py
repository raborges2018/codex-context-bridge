"""Configurações globais do codex-context-bridge."""

DEFAULT_MODEL = "claude-sonnet-4-5"
MAX_INPUT_CHARS_DIRECT = 60000
MAX_SELECTED_CHUNKS = 12
CHUNK_SIZE = 6000
CHUNK_OVERLAP = 500
OUTPUT_DIR = "output"
INDEX_DB_PATH = "index/context_index.sqlite3"

ALLOWED_EXTENSIONS = {
    ".txt", ".md", ".json", ".log", ".py", ".js", ".ts", ".tsx", ".jsx", ".yml", ".yaml", ".env.example"
}

IGNORED_DIR_NAMES = {
    "node_modules", ".git", "dist", "build", ".next", "coverage", "venv", "__pycache__", ".expo", "Pods"
}

PRIORITY_PATH_HINTS = [
    "README.md",
    "package.json",
    "app.json",
    "src/",
    "app/",
    "components/",
    "services/",
    "lib/",
    "supabase/",
    "docs/",
]

INTERNAL_SYSTEM_PROMPT = """Você é um assistente técnico especializado em compactação de contexto para continuidade de desenvolvimento de software.

Você receberá conteúdo filtrado de logs, diffs, arquivos, respostas do Codex, GitHub ou mensagens técnicas.

Sua tarefa é gerar um contexto compacto, preciso e útil para ser colado no Claude App.

Responda sempre em português do Brasil.

Não invente arquivos.
Não invente decisões.
Não invente bugs.
Não omita erros relevantes.
Preserve nomes de arquivos, funções, comandos, endpoints, variáveis, mensagens de erro e decisões técnicas.
Remova ruído.
Se houver incerteza, diga claramente.

Formato obrigatório:

# Contexto Compactado para Claude

## 1. Objetivo
Explique em até 5 linhas o que foi feito ou analisado.

## 2. Estado atual do projeto
Liste o estado real após o conteúdo recebido.

## 3. Fontes analisadas
Liste as fontes usadas.

## 4. Arquivos relevantes
Liste arquivos citados, criados, alterados ou importantes.

## 5. Decisões técnicas identificadas
Liste decisões já tomadas.

## 6. Problemas, erros ou riscos
Liste bugs, falhas, inconsistências e riscos.

## 7. Próxima ação recomendada para o Claude
Diga exatamente o que o Claude deve fazer agora.

## 8. Prompt pronto para colar no Claude
Gere uma mensagem curta, direta e acionável.

## 9. Dados de compactação
Inclua:
- tamanho aproximado original;
- tamanho aproximado enviado à API;
- tamanho aproximado final;
- redução aproximada.
"""
