import requests
import json
import streamlit as st
from typing import Optional, Dict, Any

class JarvisClient:
    def __init__(self):
        try:
            # FIX: Rename these variables to avoid conflict with method names
            self.chat_webhook_url = st.secrets["n8n"]["chat_webhook"]
            self.ingest_webhook_url = st.secrets["n8n"]["ingest_webhook"]
        except FileNotFoundError:
            st.error("Configuration file (.streamlit/secrets.toml) is missing.")
            st.stop()

    def send_message(self, message: str, session_id: str, optimize_for: str = "cost") -> str:
        payload = {
            "chatInput": message,
            "sessionId": session_id,
            "optimise_for": optimize_for
        }
        try:
            # FIX: Use the new variable name here
            response = requests.post(self.chat_webhook_url, json=payload, timeout=30)
            
            if response.status_code != 200:
                try:
                    error_msg = response.json().get('output', response.text)
                except (ValueError, json.JSONDecodeError):
                    error_msg = f"Error {response.status_code}: {response.text[:200]}"
                return f"❌ System Error: {error_msg}"

            # Check if response is empty
            if not response.text or not response.text.strip():
                return "⚠️ Error: Received empty response from server"
            
            try:
                data = response.json()
            except (ValueError, json.JSONDecodeError) as e:
                return f"⚠️ Error: Invalid JSON response from server. Response: {response.text[:200]}"
            
            # Check for error messages in the response (even if status is 200)
            if isinstance(data, dict):
                # Check common error fields
                if 'error' in data:
                    return f"❌ Error: {data.get('error', 'Unknown error')}"
                if 'message' in data and 'error' in str(data.get('message', '')).lower():
                    return f"❌ Error: {data.get('message', 'Unknown error')}"
            
            # Handle list or dict return types from n8n
            if isinstance(data, list) and data:
                # Check first item for errors
                first_item = data[0]
                if isinstance(first_item, dict):
                    if 'error' in first_item:
                        return f"❌ Error: {first_item.get('error', 'Unknown error')}"
                return first_item.get('output', "No output")
            
            # For dict responses, check for output field
            if isinstance(data, dict):
                # Check if there's an error message in the output
                output = data.get('output', str(data))
                if isinstance(output, str) and ('error' in output.lower() or 'does not support' in output.lower()):
                    return f"❌ Error: {output}"
                return output
            
            return str(data)
            
        except requests.exceptions.RequestException as e:
            return f"⚠️ Network Error: {str(e)}"

    def upload_document(self, file_obj: Any, optimize_for: str = "cost") -> bool:
        files = {"data": (file_obj.name, file_obj, file_obj.type)}
        data = {"optimise_for": optimize_for}
        
        try:
            # FIX: Use the new variable name here
            response = requests.post(self.ingest_webhook_url, files=files, data=data, timeout=60)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            st.error(f"Upload failed: {str(e)}")
            return False

    def ingest_url(self, url: str, optimize_for: str = "cost") -> bool:
        payload = {"url": url, "optimise_for": optimize_for}
        try:
            # FIX: Use the new variable name here
            response = requests.post(self.ingest_webhook_url, json=payload, timeout=30)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            st.error(f"URL ingestion failed: {str(e)}")
            return False