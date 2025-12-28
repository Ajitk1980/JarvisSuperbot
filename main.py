import streamlit as st
import uuid
from src.api_client import JarvisClient

# --- Page Config ---
st.set_page_config(
    page_title="Jarvis Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Initialization ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

client = JarvisClient()

# --- Sidebar: Knowledge Management ---
with st.sidebar:
    st.title("📚 Knowledge Base")
    st.info(f"Session ID: {st.session_state.session_id[:8]}")
    
    # Optimise For option for knowledge base
    kb_optimise_for = st.radio(
        "Optimise For",
        options=["Cost", "Power"],
        index=0,  # Default to "Cost"
        key="kb_optimise_for"
    )
    
    tab_file, tab_url = st.tabs(["📄 File", "🔗 URL"])
    
    with tab_file:
        uploaded_file = st.file_uploader("Add Context", type=['pdf', 'docx', 'txt', 'csv'])
        if st.button("Ingest Document", use_container_width=True):
            if uploaded_file:
                with st.spinner("Processing document..."):
                    success = client.upload_document(uploaded_file, optimize_for=kb_optimise_for.lower())
                    if success:
                        st.success("Document indexed successfully.")
            else:
                st.warning("Please select a file.")

    with tab_url:
        url_input = st.text_input("Article URL")
        if st.button("Ingest URL", use_container_width=True):
            if url_input:
                with st.spinner("Scraping and indexing..."):
                    success = client.ingest_url(url_input, optimize_for=kb_optimise_for.lower())
                    if success:
                        st.success("URL indexed successfully.")
            else:
                st.warning("Please enter a URL.")
    
    st.divider()
    if st.button("Clear Chat History", type="secondary"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4()) # New Session ID = New Memory
        st.rerun()

# --- Main Interface ---
st.title("Jarvis Professional Assistant")

# Optimise For option for chat
chat_optimise_for = st.radio(
    "Optimise For",
    options=["Cost", "Power"],
    index=0,  # Default to "Cost"
    key="chat_optimise_for",
    horizontal=True
)

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle Input
if prompt := st.chat_input("How can I help you?"):
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing knowledge base..."):
            response_text = client.send_message(prompt, st.session_state.session_id, optimize_for=chat_optimise_for.lower())
            st.markdown(response_text)
            
    # 3. Save Context
    st.session_state.messages.append({"role": "assistant", "content": response_text})