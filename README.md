# codex-context-bridge

Ferramenta local para macOS que compacta contexto técnico e gera um texto pronto para colar no Claude App.

## 100% offline
- Sem Anthropic API
- Sem OpenAI API
- Sem Gemini API
- Sem API paga de IA
- Sem chave obrigatória em `.env`

> Observação: a leitura de GitHub público usa `requests` apenas para baixar conteúdo informado.

## Modos automáticos de saída
A ferramenta detecta automaticamente o tipo de entrada:

1. **Modo pergunta simples**
   - Para entradas curtas com estrutura de dúvida.
   - Gera prompt direto e objetivo para resposta prática.

2. **Modo contexto técnico**
   - Para logs, diffs, erros, stack traces, caminhos de arquivos, saída de terminal etc.
   - Gera prompt técnico compacto com trechos essenciais preservados.

## Saída simplificada (única)
A saída final contém apenas:

```text
--- PROMPT PARA CLAUDE ---
<texto>

--- DADOS DE COMPACTAÇÃO ---
<dados>
```

## Requisitos
- macOS
- Python 3.11+

## Instalação
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução
```bash
python -m streamlit run app.py
```
Acesse em: `http://localhost:8501`

## Como funciona
1. Coleta uma ou mais fontes (texto manual, upload, caminho local, GitHub público).
2. Limpa ruído (linhas repetidas, progresso, warnings duplicados etc.).
3. Se necessário, faz chunking + indexação SQLite FTS5 + seleção por intenção.
4. Detecta automaticamente o tipo de entrada (pergunta ou contexto técnico).
5. Gera saída simplificada e salva em `output/contexto_compactado_YYYYMMDD_HHMMSS.md`.

## Limitações
Por ser heurístico e offline:
- não faz compreensão semântica avançada como um LLM;
- pode perder nuances em conteúdos muito ambíguos;
- em troca, reduz ruído e organiza o essencial com baixo custo operacional.
