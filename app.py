"""Interface Streamlit para gerar contexto compacto ao Claude App."""

from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv

from src.chunker import chunk_text
from src.cleaner import clean_text
from src.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    INDEX_DB_PATH,
    MAX_INPUT_CHARS_DIRECT,
    MAX_SELECTED_CHUNKS,
)
from src.content_collector import collect_contents
from src.indexer import ChunkIndexer
from src.intent_router import INTENT_OPTIONS, resolve_intent_instruction
from src.markdown_writer import save_markdown
from src.searcher import search_chunks
from src.summarizer import summarize_content

load_dotenv()

st.set_page_config(page_title="codex-context-bridge", layout="wide")
st.title("codex-context-bridge")
st.caption("Compacte contexto técnico localmente antes de enviar ao Claude App.")

manual_text = st.text_area("1) Cole texto manualmente", height=280, placeholder="Cole aqui logs, respostas do Codex, diffs, decisões, etc.")
uploaded_files = st.file_uploader(
    "2) Upload de arquivos",
    type=["txt", "md", "json", "log", "py", "js", "ts", "tsx", "jsx", "yml", "yaml"],
    accept_multiple_files=True,
)
local_abs_path = st.text_input("3) Caminho local absoluto no Mac", placeholder="/Users/seu-usuario/projeto")
github_url = st.text_input(
    "4) URL de repositório GitHub público ou arquivo específico",
    placeholder="https://github.com/owner/repo ou https://github.com/owner/repo/blob/main/arquivo.md",
)
intent = st.selectbox("5) Intenção", options=INTENT_OPTIONS)
additional_instruction = st.text_area("6) Instrução adicional", height=100)

if "generated_markdown" not in st.session_state:
    st.session_state.generated_markdown = ""

if st.button("7) Gerar contexto compacto", type="primary"):
    try:
        sources = collect_contents(manual_text, uploaded_files, local_abs_path, github_url)
        if not sources:
            st.error("Nenhuma fonte informada. Forneça ao menos texto, arquivo, caminho local ou URL GitHub.")
        else:
            cleaned_records = []
            for source, content in sources:
                cleaned = clean_text(content)
                if cleaned:
                    cleaned_records.append((source, cleaned))

            if not cleaned_records:
                st.error("As fontes foram lidas, mas não houve conteúdo útil após limpeza.")
            else:
                original_size = sum(len(content) for _, content in sources)
                cleaned_text = "\n\n".join(f"### Fonte: {src}\n{txt}" for src, txt in cleaned_records)

                selected_text = cleaned_text
                sent_size = len(cleaned_text)
                if len(cleaned_text) > MAX_INPUT_CHARS_DIRECT:
                    chunks = chunk_text(cleaned_text, CHUNK_SIZE, CHUNK_OVERLAP)
                    indexer = ChunkIndexer(INDEX_DB_PATH)
                    records = [(f"chunk_{i+1}", chunk) for i, chunk in enumerate(chunks)]
                    indexer.add_chunks(records)

                    query = resolve_intent_instruction(intent) + " " + (additional_instruction or "")
                    selected = search_chunks(INDEX_DB_PATH, query, MAX_SELECTED_CHUNKS)
                    indexer.close()

                    if selected:
                        selected_text = "\n\n".join(f"### {src}\n{txt}" for src, txt in selected)
                        sent_size = len(selected_text)

                summary = summarize_content(
                    intent_instruction=resolve_intent_instruction(intent),
                    additional_instruction=additional_instruction,
                    content=selected_text,
                )

                final_size = len(summary)
                reduction_pct = 0.0 if original_size == 0 else ((original_size - final_size) / original_size) * 100
                compression_note = (
                    f"\n\n---\n\n[metrica] original≈{original_size} chars | enviado≈{sent_size} chars "
                    f"| final≈{final_size} chars | reducao≈{reduction_pct:.2f}%"
                )
                markdown_final = summary + compression_note
                file_path = save_markdown(markdown_final)

                st.session_state.generated_markdown = markdown_final
                st.success(f"Contexto compacto gerado com sucesso em: {file_path}")

    except Exception as exc:
        st.error(f"Erro ao gerar contexto compacto: {exc}")

st.subheader("8) Markdown final")
st.markdown(st.session_state.generated_markdown or "_Ainda não gerado._")

if st.session_state.generated_markdown:
    st.download_button(
        "9) Baixar Markdown gerado",
        data=st.session_state.generated_markdown.encode("utf-8"),
        file_name="contexto_compactado.md",
        mime="text/markdown",
    )

st.divider()
st.caption("Execute localmente em: http://localhost:8501")
