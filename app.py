import traceback
import hashlib
import streamlit as st
from src.api_client import upload_document, ask_question

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="RAG Document Q&A",
    page_icon="📚",
    layout="wide",
)

# ----------------------------------------------------
# SESSION STATE INITIALIZATION
# ----------------------------------------------------

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "processed_files" not in st.session_state:
    st.session_state["processed_files"] = {}

st.title("📚 RAG-Based Document Q&A System")

st.markdown(
    "Upload your PDF documents and ask questions."
    "Get AI-generated answers grounded in your documents."
)


# ---------------------------------------------------
# SIDEBAR: DOCUMENT UPLOAD
# ---------------------------------------------------

with st.sidebar:

    st.header("📁 Document Management")

    uploaded_files = st.file_uploader(
        "Upload your PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if st.button("Process Documents", use_container_width=True):

        if not uploaded_files:
            st.warning("Please upload at least one PDF documents.")

        else:

            for uploaded_file in uploaded_files:

                file_content = uploaded_file.getvalue()

                file_hash = hashlib.sha256(
                    file_content
                ).hexdigest()

                if file_hash in st.session_state["processed_files"]:
                    st.info(
                        f"{uploaded_file.name} is already processed."
                    )
                    continue

                try:

                    with st.spinner(
                        f"processing {uploaded_file.name}..."
                    ):

                        result = upload_document(uploaded_file)

                        st.session_state["processed_files"][
                            file_hash
                        ] = uploaded_file.name

                        st.success(
                            f"Processed {result['filename']} "
                            f"{result['chunks_stored']} chunks stored."
                        )
                except Exception as error:
                    st.error(
                        f"Failed to process {uploaded_file.name}: {error}"
                    )

    st.divider()

    st.subheader("📄 Processed Documents")

    if st.session_state["processed_files"]:

        for file_hash, filename in st.session_state["processed_files"].items():
            st.write(f"✅ {filename}")
            st.caption(f"Document ID: {file_hash[:12]}")

    else:
        st.caption("No documents processed in this session yet.")

    if st.button("clear Chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()


# ------------------------------------------------------------
# CHAT INTERFACE
# ------------------------------------------------------------

st.subheader("💬 Ask Your Documents")

# Display previous messages.
for message in st.session_state["messages"]:

    with st.chat_message(message["role"]):

        st.markdown(message['content'])

        if message.get('sources'):

            with st.expander("📚 View Sources"):

                for source in message['sources']:

                    st.write(
                        f"**Document:** {source['source']}"
                    )

                    st.write(
                        f"**Chunk:** {source['chunk_index']}"
                    )

                    st.write(
                        f"**Similarity Score:** "
                        f"{source['score']:.4f}"
                    )

                    st.divider()

# Accept new question
question = st.chat_input(
    "Ask a question about your uploaded documents..."
)

if question:

    # Display user question.
    st.session_state['messages'].append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Generate answer.
    with st.chat_message('assistant'):

        with st.spinner("Searching documents and generating answer..."):

            try:

                result = ask_question(question)

                answer = result["answer"]
                sources = result['sources']

                st.markdown(answer)

                if sources:

                    with st.expander("📚 View Sources"):

                        for source in sources:

                            st.write(
                                f"**Document:** {source['source']}"
                            )

                            st.write(
                                f"**Chunk:** {source['chunk_index']}"
                            )

                            st.write(
                                f"**Similarity Score:** "
                                f"{source['score']:.4f}"
                            )

                            st.divider()

                st.session_state["messages"].append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )

            except Exception as error:

                error_message = (
                    f'Something went wrong: {error}'
                )

                st.error(error_message)

                st.session_state["message"].append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )