import streamlit as st
import uuid
from src.api_client import JarvisClient

# --- Page Config ---
st.set_page_config(
    page_title="Hey! You can ask me anything. I am not shy.",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# --- Custom CSS for Kuki-style Styling ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    load_css("src/assets/style.css")
except FileNotFoundError:
    st.warning("⚠️ CSS file not found. UI might look unstyled.")


# --- Initialization ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_knowledge_section" not in st.session_state:
    st.session_state.show_knowledge_section = False

client = JarvisClient()

# --- Sidebar: Profile and Knowledge Management ---
with st.sidebar:
    # Profile Image and Name (similar to Kuki interface)
    st.markdown("<h3>@jarvis_ai</h3>", unsafe_allow_html=True)
    
    # Profile image - using a placeholder image URL
    profile_image_url = "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=400&fit=crop&crop=faces&auto=format&q=80"
    st.markdown(f'<img src="{profile_image_url}" class="profile-image" alt="Jarvis AI">', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # "Update My Knowledge" Button (replacing Discord/Video Chat buttons)
    if st.button("📚 Update My Knowledge", use_container_width=True, key="update_knowledge_btn"):
        st.session_state.show_knowledge_section = not st.session_state.show_knowledge_section
    
    # Knowledge Base Section (collapsible)
    if st.session_state.show_knowledge_section:
        st.markdown('<div class="knowledge-section">', unsafe_allow_html=True)
        
        # Performance Mode Selection
        st.markdown("**Performance Mode**")
        kb_optimise_for = st.radio(
            "Select optimization mode",
            options=["Cost", "Power"],
            index=0,
            key="kb_optimise_for",
            label_visibility="collapsed"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        
        # File Upload
        st.markdown("**Upload Document**")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'docx', 'txt', 'csv'],
            label_visibility="collapsed",
            key="file_uploader"
        )
        if st.button("📤 Upload & Index", use_container_width=True, type="primary", key="upload_btn"):
            if uploaded_file:
                with st.spinner("Processing document..."):
                    success = client.upload_document(uploaded_file, optimize_for=kb_optimise_for.lower())
                    if success:
                        st.success("Document indexed successfully!")
                        st.session_state.show_knowledge_section = False
            else:
                st.warning("Please select a file first")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # URL Input
        st.markdown("**Or Enter URL**")
        url_input = st.text_input(
            "Enter URL",
            placeholder="https://example.com/article",
            label_visibility="collapsed",
            key="url_input"
        )
        if st.button("🔗 Index URL", use_container_width=True, type="primary", key="url_btn"):
            if url_input:
                with st.spinner("Scraping and indexing..."):
                    success = client.ingest_url(url_input, optimize_for=kb_optimise_for.lower())
                    if success:
                        st.success("URL indexed successfully!")
                        st.session_state.show_knowledge_section = False
            else:
                st.warning("Please enter a valid URL")
        
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Clear Chat Button
    if st.button("🗑️ Clear Chat", use_container_width=True, key="clear_chat_btn"):
        st.session_state.messages = []
        st.rerun()

# --- Main Chat Interface ---
# Header with performance mode (top right corner style)
col1, col2 = st.columns([5, 1])

with col1:
    st.markdown("")  # Empty space for alignment

with col2:
    chat_optimise_for = st.radio(
        "Chat Optimization Mode",
        options=["Cost", "Power"],
        index=0,
        key="chat_optimise_for",
        horizontal=True,
        label_visibility="collapsed"
    )

# Chat Container
chat_container = st.container()

with chat_container:
    # Display Chat History
    if st.session_state.messages:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    else:
        # Welcome messages (similar to Kuki style)
        with st.chat_message("assistant"):
            st.markdown("Hi there, I'm Jarvis 👋")
        
        with st.chat_message("assistant"):
            st.markdown("I'm a friendly AI assistant, here to help you 24/7")
        
        with st.chat_message("assistant"):
            st.markdown("We could start by getting to know each other if you like 🥰. What would you like to know?")

# Handle Input
if prompt := st.chat_input("Type your message..."):
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text = client.send_message(prompt, st.session_state.session_id, optimize_for=chat_optimise_for.lower())
            st.markdown(response_text)
            
    # 3. Save Context
    st.session_state.messages.append({"role": "assistant", "content": response_text})