import requests
import streamlit as st
from typing import Optional, Dict, Any

class JarvisClient:
    def __init__(self):
        # Load config from Streamlit secrets
        try:
            self.chat_url = st.secrets["n8n"]["chat_webhook"]
            self.ingest_url = st.secrets["n8n"]["ingest_webhook"]
        except FileNotFoundError:
            st.error("Configuration file (.streamlit/secrets.toml) is missing.")
            st.stop()

    def send_message(self, message: str, session_id: str) -> str:
        """Sends a prompt to the Chat workflow."""
        payload = {
            "chatInput": message,
            "sessionId": session_id
        }
        try:
            response = requests.post(self.chat_url, json=payload, timeout=30)
            response.raise_for_status()
            
            # Handle n8n Agent response formats
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return data[0].get('output', "No output received.")
            return data.get('output', str(data))
            
        except requests.exceptions.RequestException as e:
            return f"⚠️ Error communicating with Brain: {str(e)}"

    def upload_document(self, file_obj: Any, optimize_for: str = "power") -> bool:
        """Uploads a file to the Ingestion workflow."""
        files = {"data": (file_obj.name, file_obj, file_obj.type)}
        data = {"optimise_for": optimize_for}
        
        try:
            response = requests.post(self.ingest_url, files=files, data=data, timeout=60)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            st.error(f"Upload failed: {str(e)}")
            return False

    def ingest_url(self, url: str, optimize_for: str = "power") -> bool:
        """Sends a URL to the Ingestion workflow."""
        payload = {"url": url, "optimise_for": optimize_for}
        try:
            response = requests.post(self.ingest_url, json=payload, timeout=30)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            st.error(f"URL ingestion failed: {str(e)}")
            return False