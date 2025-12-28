import streamlit as st
import uuid
from src.api_client import JarvisClient

# --- Page Config ---
st.set_page_config(
    page_title="Jarvis AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# --- Custom CSS for Kuki-style Styling ---
st.markdown("""
    <style>
    /* Import clean sans-serif font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1400px;
    }
    
    /* Sidebar styling - clean white background */
    .css-1d391kg {
        padding-top: 2rem;
        background-color: #FFFFFF;
    }
    
    .sidebar .sidebar-content {
        background-color: #FFFFFF;
    }
    
    /* Profile image container */
    .profile-image {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        margin: 0 auto;
        display: block;
        border: 3px solid #E3F2FD;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Sidebar buttons - light blue style */
    .sidebar-button {
        background-color: #E3F2FD !important;
        color: #1976D2 !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        margin-bottom: 0.75rem !important;
    }
    
    .sidebar-button:hover {
        background-color: #BBDEFB !important;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(25, 118, 210, 0.2) !important;
    }
    
    /* Chat message bubbles - light blue */
    .stChatMessage {
        padding: 0.75rem 1rem;
        border-radius: 18px;
        margin-bottom: 0.75rem;
    }
    
    /* User messages */
    div[data-testid="stChatMessage"][data-message="user"] {
        background-color: #F5F5F5;
    }
    
    /* Assistant messages - light blue */
    div[data-testid="stChatMessage"][data-message="assistant"] {
        background-color: #E3F2FD;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 24px;
        border: 1px solid #E0E0E0;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #90CAF9;
        box-shadow: 0 0 0 2px rgba(144, 202, 249, 0.2);
    }
    
    /* File uploader styling */
    .stFileUploader {
        border-radius: 12px;
        border: 2px dashed #BBDEFB;
        background-color: #FAFAFA;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 12px;
        font-weight: 500;
        transition: all 0.2s ease;
        font-size: 0.9rem;
    }
    
    .stButton > button[type="primary"] {
        background-color: #2196F3;
        color: white;
    }
    
    .stButton > button[type="primary"]:hover {
        background-color: #1976D2;
        box-shadow: 0 4px 12px rgba(33, 150, 243, 0.3);
    }
    
    /* Hide radio button labels */
    .stRadio > label {
        font-weight: 400;
        font-size: 0.85rem;
    }
    
    /* Section headers */
    h3 {
        font-weight: 600;
        font-size: 1.1rem;
        color: #424242;
        margin-bottom: 0.5rem;
    }
    
    /* Caption styling */
    .stCaption {
        color: #757575;
        font-size: 0.8rem;
    }
    
    /* Chat input */
    .stChatInputContainer {
        border-top: 1px solid #E0E0E0;
        padding-top: 1rem;
    }
    
    /* Remove margins from headers in sidebar */
    .sidebar h3 {
        margin-top: 0;
        text-align: center;
        font-size: 1rem;
        font-weight: 500;
        color: #616161;
    }
    
    /* Knowledge section styling */
    .knowledge-section {
        background-color: #F5F5F5;
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    /* Sidebar button styling - light blue like Kuki */
    .sidebar button {
        background-color: #E3F2FD !important;
        color: #1976D2 !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    
    .sidebar button:hover {
        background-color: #BBDEFB !important;
        box-shadow: 0 2px 8px rgba(25, 118, 210, 0.2) !important;
    }
    
    /* Primary buttons in sidebar keep their style */
    .sidebar button[data-baseweb="button"][kind="primary"] {
        background-color: #2196F3 !important;
        color: white !important;
    }
    
    .sidebar button[data-baseweb="button"][kind="primary"]:hover {
        background-color: #1976D2 !important;
    }
    </style>
    """, unsafe_allow_html=True)

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
        if st.button("Upload & Index", use_container_width=True, type="primary", key="upload_btn"):
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
        if st.button("Index URL", use_container_width=True, type="primary", key="url_btn"):
            if url_input:
                with st.spinner("Scraping and indexing..."):
                    success = client.ingest_url(url_input, optimize_for=kb_optimise_for.lower())
                    if success:
                        st.success("URL indexed successfully!")
                        st.session_state.show_knowledge_section = False
            else:
                st.warning("Please enter a valid URL")
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- Main Chat Interface ---
# Header with performance mode (top right corner style)
col1, col2 = st.columns([5, 1])

with col1:
    st.markdown("")  # Empty space for alignment

with col2:
    chat_optimise_for = st.radio(
        "",
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