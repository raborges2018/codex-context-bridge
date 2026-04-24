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

PRIORITY_TERMS = [
    "error", "exception", "failed", "traceback", "todo", "fixme", "modified", "created", "deleted",
    "commit", "pr", "branch", "build", "test", "lint",
]
