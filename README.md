# codex-context-bridge

Utilitário local para macOS que compacta contexto técnico para você copiar e colar no Claude App.

## Objetivo
O `codex-context-bridge` coleta conteúdo técnico (texto, arquivos locais e GitHub público), remove ruído, seleciona os trechos mais úteis por intenção e gera um Markdown compacto.

## Inspiração no context-mode
O projeto foi inspirado no conceito do `mksglu/context-mode` (somente conceito):
- manter conteúdo bruto fora do chat;
- reduzir volume de contexto;
- preservar informações técnicas relevantes.

## Diferença para o context-mode original
- implementação própria, em Python + Streamlit;
- pipeline local com chunking + SQLite FTS5;
- foco em organização prática para continuidade no Claude App;
- resumo por heurísticas **100% offline** (sem chamadas de IA).

## 100% offline
Este projeto agora funciona sem APIs de IA externas:
- não usa Anthropic API;
- não usa OpenAI API;
- não usa Gemini API;
- não exige chave no `.env`.

> Observação: a leitura de GitHub público usa `requests` para baixar conteúdo do repositório/arquivo informado.

## Limitações
Como é offline e heurístico:
- não faz resumo semântico avançado como um LLM;
- pode perder nuances complexas de contexto;
- ainda assim reduz ruído e organiza contexto técnico de forma prática.

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
Aplicação disponível em: `http://localhost:8501`

## Como funciona
1. Coleta uma ou mais fontes:
   - texto manual;
   - upload de arquivo;
   - caminho local absoluto;
   - URL de repositório/arquivo GitHub público.
2. Limpa ruído:
   - logs repetidos;
   - warnings/stack traces duplicados;
   - linhas vazias excessivas;
   - progresso de download.
3. Se conteúdo for grande:
   - quebra em chunks com overlap;
   - indexa em SQLite FTS5;
   - busca chunks relevantes por intenção.
4. Gera Markdown final estruturado e salva em:
   - `output/contexto_compactado_YYYYMMDD_HHMMSS.md`

## Exemplos de uso
1. **Colar texto do Codex** para consolidar estado da tarefa.
2. **Ler arquivo local** (ex.: logs, markdown, código).
3. **Ler repositório GitHub público** para extrair contexto técnico.
4. **Gerar contexto mínimo** para reduzir tokens.
5. **Preparar próxima tarefa para Claude** com instrução objetiva.
