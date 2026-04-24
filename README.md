# codex-context-bridge

Utilitário local para macOS que reduz volume de contexto técnico (tokens/caracteres) antes de colar no Claude App.

## Objetivo
O `codex-context-bridge` coleta conteúdos técnicos de múltiplas fontes, remove ruído, seleciona os trechos mais relevantes por intenção e gera um **Markdown compacto** para continuidade de desenvolvimento no Claude.

## Inspiração no context-mode
Este projeto é inspirado no conceito do `mksglu/context-mode`:
- manter conteúdo bruto fora do chat;
- consolidar contexto técnico em uma saída curta e útil;
- facilitar continuidade sem desperdiçar janela de contexto.

## Diferenças para o context-mode original
- implementação local em **Python + Streamlit**;
- pipeline com **SQLite FTS5** para seleção de chunks relevantes;
- foco em fluxo de trabalho com **Claude App** e saída em português (pt-BR);
- sem dependência de serviços externos além da API da Anthropic;
- sem Docker, sem banco externo, sem autenticação.

## Requisitos
- macOS
- Python 3.11+
- chave de API Anthropic

## Instalação
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuração do ambiente
1. Copie o arquivo de exemplo:
```bash
cp .env.example .env
```
2. Preencha sua chave:
```env
ANTHROPIC_API_KEY=sua_chave_real
```

## Execução
```bash
python -m streamlit run app.py
```
Aplicação disponível em: `http://localhost:8501`

## Como funciona
1. Coleta conteúdo de uma ou mais fontes simultaneamente:
   - texto manual;
   - upload de arquivo;
   - caminho local absoluto;
   - URL de repositório/arquivo GitHub público.
2. Limpa ruído (logs repetidos, warnings duplicados, progresso, etc.).
3. Se conteúdo for pequeno, envia direto para API.
4. Se for grande, realiza:
   - chunking com sobreposição;
   - indexação SQLite FTS5;
   - busca de chunks por intenção.
5. Gera Markdown final e salva em `output/contexto_compactado_YYYYMMDD_HHMMSS.md`.

## Exemplos de uso
1. **Colando texto do Codex**
   - Cole respostas brutas no campo de texto.
   - Selecione intenção: `Explicar alterações feitas pelo Codex`.

2. **Lendo arquivo local**
   - Informe `/Users/.../projeto/logs/build.log`.
   - Gere contexto para análise de falhas.

3. **Lendo repositório GitHub**
   - Informe `https://github.com/owner/repo`.
   - O app prioriza arquivos como README, package.json e diretórios centrais.

4. **Gerando contexto mínimo**
   - Escolha intenção: `Gerar contexto mínimo`.
   - Resultado tende a ser mais enxuto e acionável.

5. **Preparando próxima tarefa para Claude**
   - Escolha intenção: `Preparar prompt para próxima tarefa`.
   - Adicione instruções extras específicas do próximo passo.

## Estrutura
```
/
  README.md
  requirements.txt
  .env.example
  app.py
  input/.gitkeep
  output/.gitkeep
  index/.gitkeep
  src/
```

## Observações
- não há chave hardcoded no código;
- indexação é local em SQLite (`index/context_index.sqlite3`);
- projeto feito para rodar 100% local no Mac.
