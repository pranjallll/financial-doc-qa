import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
from utils import ask_ollama, cached_chunks_and_index, retrieve_relevant_chunks

st.set_page_config(page_title="📊 Financial Document Q&A Assistant", layout="wide")

st.title("📊 Financial Document Q&A Assistant")
st.markdown("Upload a **PDF** or **Excel** file to preview financial data and ask questions interactively.")

uploaded_file = st.file_uploader("Upload a financial document", type=["pdf", "xlsx"])

if uploaded_file is not None:
    file_name = uploaded_file.name

    # Extract content
    text, excel_data = "", {}

    if file_name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text() or ""
        # Chunk + embed PDF text
        chunks, index, embeddings = cached_chunks_and_index(text)

    elif file_name.endswith(".xlsx"):
        excel_data = pd.read_excel(uploaded_file, sheet_name=None)
        # Flatten Excel into text
        context = "\n\n".join(
            [f"Sheet: {name}\n{df.head(50).to_string()}" for name, df in excel_data.items()]
        )
        chunks, index, embeddings = cached_chunks_and_index(context)

    # Initialize conversation memory
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    # Tabs
    tab1, tab2 = st.tabs(["📑 Preview Document", "💬 Ask Questions"])

    # --- Preview Tab ---
    with tab1:
        st.subheader("📑 Document Preview")
        if file_name.endswith(".pdf"):
            st.text_area("Extracted Text", text[:3000], height=400)
        else:
            for sheet, df in excel_data.items():
                st.write(f"**Sheet: {sheet}**")
                st.dataframe(df.head(20))

    # --- Q&A Tab ---
    with tab2:
        st.subheader("💬 Ask Questions about your Document")
        user_q = st.text_input("Type your financial question here...")

        if user_q:
            with st.spinner("Thinking..."):
                # Retrieve relevant chunks
                relevant_chunks = retrieve_relevant_chunks(user_q, chunks, index, embeddings, top_k=3)
                context = "\n\n".join(relevant_chunks)

                # Include previous conversation for context
                previous_context = "\n".join(
                    [f"Q: {q}\nA: {a}" for q, a in st.session_state.conversation]
                )
                full_context = previous_context + "\n\n" + context if previous_context else context

                # Ask Ollama
                answer = ask_ollama(user_q, full_context)

                # Save conversation
                st.session_state.conversation.append((user_q, answer))

            st.success("Answer:")
            st.write(answer)

        # Show conversation history
        if st.session_state.conversation:
            st.markdown("### 📝 Conversation History")
            for q, a in st.session_state.conversation:
                st.markdown(f"**Q:** {q}")
                st.markdown(f"**A:** {a}\n")

        # Clear conversation button
        if st.button("Clear Conversation"):
            st.session_state.conversation = []
            st.experimental_rerun()
