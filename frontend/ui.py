import streamlit as st
import requests
import os

# --- CONFIGURATION ---
# This uses the environment variable if it exists (Docker), 
# otherwise defaults to local (VS Code).
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/api/v1")
PAGE_TITLE = "Hippocratic AI - Healthcare Generative AI"
PAGE_ICON = "🛡️"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# --- BACKEND HEALTH CHECK ---
def check_backend():
    try:
        # We try to ping your FastAPI docs or a root endpoint
        response = requests.get(f"{API_URL.replace('/api/v1', '')}/docs", timeout=1)
        return response.status_code == 200
    except:
        return False

# --- SIDEBAR STATUS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
    st.title("System Status")
    
    if check_backend():
        st.success("● Backend Connected")
    else:
        st.error("○ Backend Offline")
        st.info("Check: Did you run `uvicorn` in the second terminal?")
    
    st.divider()
# --- CUSTOM CSS & DESIGN INJECTION ---
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(to bottom, #ffffff, #f9fdfb);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header & Navbar */
    .nav-wrapper {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 50px;
        background: white;
        border-bottom: 1px solid #eee;
        position: fixed;
        top: 0; left: 0; right: 0; z-index: 1000;
    }
    .nav-logo { font-weight: 700; color: #000; display: flex; align-items: center; gap: 8px; }
    .nav-logo span { color: #666; font-size: 0.8rem; font-weight: 400; }
    .nav-links { display: flex; gap: 25px; color: #333; font-size: 0.9rem; font-weight: 600; }
    .btn-meeting {
        background-color: #10b981; color: white !important;
        padding: 8px 20px; border-radius: 50px; text-decoration: none; font-weight: 600;
    }

    /* Announcement Banner */
    .banner {
        background-color: #34d399; color: white;
        text-align: center; padding: 10px; font-size: 0.85rem;
        margin-top: 70px; font-weight: 600;
    }

    /* Hero Section */
    .hero-container { padding: 80px 20px; text-align: center; }
    .hero-title {
        color: #10b981; font-size: 4rem; font-weight: 800;
        line-height: 1.1; margin-bottom: 40px;
    }
    .section-subtitle { font-size: 1.8rem; font-weight: 700; color: #111; margin-bottom: 30px; }

    /* Pill Buttons Styling */
    div.stButton > button {
        border-radius: 50px; border: 1px solid #ddd;
        background-color: white; color: #444; font-weight: 600;
        padding: 10px 25px; transition: 0.3s;
    }
    div.stButton > button:hover { border-color: #10b981; color: #10b981; background: #f0fdf4; }
    
    /* Icon Grid Styles */
    .icon-box { text-align: center; padding: 10px; cursor: pointer; }
    .icon-circle {
        width: 60px; height: 60px; background: white; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        font-size: 1.5rem; border: 1px solid #eee;
    }
    .icon-label { font-size: 0.8rem; color: #555; font-weight: 600; }

    /* Chat Styling */
    .stChatInputContainer { padding-bottom: 50px; }
</style>
""", unsafe_allow_html=True)

# --- 1. NAVIGATION BAR ---
st.markdown("""
    <div class="nav-wrapper">
        <div class="nav-logo">
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="30">
            Hippocratic AI <span>Do No Harm</span>
        </div>
        <div class="nav-links">
            <span>Safety</span><span>LLM</span><span>Research</span><span>Create an AI</span><span>Company</span>
        </div>
        <a href="#" class="btn-meeting">Book a Meeting</a>
    </div>
""", unsafe_allow_html=True)

# --- 2. ANNOUNCEMENT BANNER ---
st.markdown('<div class="banner">📢 Haris AI Selected to Collaborate in CMS Health Tech Ecosystem Initiative</div>', unsafe_allow_html=True)

# --- 3. HERO SECTION ---
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Safety Focused Generative<br>AI for Healthcare</h1>
        <h2 class="section-subtitle">Choose an AI Agent to Get Started</h2>
    </div>
""", unsafe_allow_html=True)

# --- 4. PILL FILTERS (Horizontal) ---
# Aligning these in columns to center them
_, p1, p2, p3, p4, p5, _ = st.columns([2, 1, 1, 1, 1, 1, 2])
with p1: st.button("All", key="btn_all")
with p2: st.button("Payor", key="btn_payor")
with p3: st.button("Pharma", key="btn_pharma")
with p4: st.button("Dental", key="btn_dental")
with p5: st.button("Provider", key="btn_provider")

st.write("") # Spacer

# --- 5. ICON GRID (Agents) ---
# We use columns to replicate the 9-icon grid from your screenshot
cols = st.columns(9)
agents = [
    ("💬", "All"), ("🩺", "Pre-op"), ("📄", "Discharge"), 
    ("💓", "Chronic"), ("📋", "Question"), ("🛡️", "VBC/Risk"),
    ("🔬", "Trials"), ("💊", "Pharmacy"), ("🌿", "Natural")
]

for i, (icon, label) in enumerate(agents):
    with cols[i]:
        st.markdown(f"""
            <div class="icon-box">
                <div class="icon-circle">{icon}</div>
                <div class="icon-label">{label}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br><hr><br>", unsafe_allow_html=True)

# --- 6. INTEGRATED RAG CHAT LOGIC ---
# Using the session state logic from your previous code

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask a medical or enterprise question..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call your existing API
    with st.spinner("AI Agent is analyzing..."):
        try:
            # Placeholder session ID (you can link this to the icons later)
            session_id = "healthcare_demo"
            payload = {"question": prompt, "session_id": session_id}
            response = requests.post(f"{API_URL}/chat", data=payload)
            
            if response.status_code == 200:
                answer = response.json().get("answer", "I couldn't find a specific answer in the documents.")
            else:
                answer = f"Error: {response.text}"
        except Exception as e:
            answer = f"Connection failed: {e}"

    # Display Assistant Message
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

# --- SIDEBAR (Optional Admin Panel) ---
with st.sidebar:
    st.subheader("🛡️ Admin Controls")
    uploaded_file = st.file_uploader("Ingest Document", type=["pdf"])
    if st.button("Process Document"):
        if uploaded_file:
            # Existing upload logic
            files = {"file": uploaded_file}
            res = requests.post(f"{API_URL}/upload", files=files, data={"session_id": "healthcare_demo"})
            st.success("Document added to Knowledge Base")