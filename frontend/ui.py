import streamlit as st
import requests
import os
import base64

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/api/v1")
PAGE_TITLE = "DocuMind - Enterprise AI"
LOGO_PATH = "frontend/logo.png" 

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Adding the logo
try:
    img_base64 = get_base64_of_bin_file(LOGO_PATH)
    logo_html = f"data:image/png;base64,{img_base64}"
except FileNotFoundError:
    logo_html = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png" # Fallback

st.set_page_config(page_title=PAGE_TITLE, page_icon=logo_html, layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = "All"

def check_backend():
    try:
        response = requests.get(f"{API_URL.replace('/api/v1', '')}/docs", timeout=1)
        return response.status_code == 200
    except: return False

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    
    .stApp {{
        background: #F8FAFC;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    
    /* Navbar Styles */
    .nav-wrapper {{
        display: flex; justify-content: space-between; align-items: center;
        padding: 0.8rem 4rem; background: white;
        border-bottom: 1px solid #E2E8F0; position: fixed;
        top: 0; left: 0; right: 0; z-index: 1000;
    }}
    .nav-logo-container {{ display: flex; align-items: center; gap: 12px; }}
    .nav-logo-img {{ height: 25px; width: auto; }}
    .nav-logo-text {{ font-weight: 100; color: #1E3A8A; font-size: 1.25rem; }}

    .btn-access {{
        background: #2563EB; color: white !important;
        padding: 8px 24px; border-radius: 8px; text-decoration: none; font-weight: 600;
    }}

    /* Hero & Spacing */
    .hero-container {{ padding: 110px 20px 30px; text-align: center; }}
    .hero-title {{ color: #1E3A8A; font-size: 3rem; font-weight: 800; margin-bottom: 8px; }}
    .hero-subtitle {{ color: #64748B; font-size: 1rem; }}
    
    /* Button Customization */
    div.stButton > button {{
        transition: 0.2s all;
        border-radius: 10px;
    }}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="nav-wrapper">
        <div class="nav-logo-container">
            <img src="{logo_html}" class="nav-logo-img">
            <span class="nav-logo-text">DocuMind AI</span>
        </div>
        <a href="#" class="btn-access">Request Access</a>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Enterprise Knowledge Intelligence</h1>
        <p class="hero-subtitle">Securely chat with your documents using specialized AI agents.</p>
    </div>
""", unsafe_allow_html=True)

agents = [
    ("💬", "All"), ("⚖️", "Legal"), ("📊", "Finance"), 
    ("🧬", "R&D"), ("🛠️", "Support"), ("🤝", "HR")
]

st.write("### 🤖 Select specialized agent")
cols = st.columns(len(agents))

for i, (icon, label) in enumerate(agents):
    with cols[i]:
        b_type = "primary" if st.session_state.selected_agent == label else "secondary"
        if st.button(f"{icon} {label}", key=f"agent_{label}", use_container_width=True, type=b_type):
            st.session_state.selected_agent = label
            st.rerun()

st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(f"Ask {st.session_state.selected_agent} anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Processing..."):
        try:
            payload = {
                "question": prompt, 
                "session_id": "documind_demo",
                "agent_type": st.session_state.selected_agent
            }
            response = requests.post(f"{API_URL}/chat", json=payload)
            answer = response.json().get("answer") if response.status_code == 200 else "Service error."
        except:
            answer = "Backend is unreachable. Please check connection."

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

with st.sidebar:
    # Logo for the Sidebar
    st.image(logo_html, width=200)
    st.markdown("### System Hub")
    if check_backend():
        st.success("Network: Connected")
    else:
        st.error("Network: Disconnected")
    
    st.divider()
    st.markdown("### 📁 Data Ingestion")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    if st.button("Ingest Document", use_container_width=True, type="primary"):
        if uploaded_file:
            with st.spinner("Ingesting..."):
                files = {"file": uploaded_file}
                requests.post(f"{API_URL}/upload", files=files, data={"session_id": "documind_demo"})
                st.toast("Document Ready!", icon="✅")