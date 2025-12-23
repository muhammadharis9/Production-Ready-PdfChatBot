import streamlit as st
import requests

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000/api/v1"
PAGE_TITLE = "DocuMind Enterprise"
PAGE_ICON = "🛡️"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# --- CUSTOM CSS (To mimic the clean design) ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #ffffff;
    }
    /* Header Styling */
    h1 {
        color: #2E7D32; /* Green like the screenshot */
        font-family: 'Helvetica', sans-serif;
        text-align: center;
    }
    h3 {
        text-align: center;
        color: #555;
    }
    /* Button Styling */
    .stButton>button {
        background-color: #E8F5E9;
        color: #2E7D32;
        border-radius: 20px;
        border: 1px solid #2E7D32;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2E7D32;
        color: white;
    }
    /* Chat Message Styling */
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
    }
    .chat-message.user {
        background-color: #f0f2f6;
    }
    .chat-message.bot {
        background-color: #e8f5e9;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (For "Book a Meeting" / Admin stuff) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
    st.title("Admin Panel")
    st.write("Upload new knowledge bases here.")
    
    # File Uploader connecting to your API
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    session_id = st.text_input("Session/User ID", value="demo_user")
    
    if st.button("Upload to Knowledge Base"):
        if uploaded_file:
            with st.spinner("Ingesting document..."):
                files = {"file": uploaded_file.getvalue()}
                data = {"session_id": session_id}
                try:
                    res = requests.post(f"{API_URL}/upload", files={"file": uploaded_file}, data=data)
                    if res.status_code == 200:
                        st.success("Document added successfully!")
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

# --- MAIN PAGE (The "Hero" Section) ---
st.title("Safety Focused Generative AI for Enterprise")
st.markdown("### Choose a Knowledge Base to Get Started")

# The "Pills" / Filter Bar
col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.button("All")
with col2: st.button("HR Policy")
with col3: st.button("IT Support")
with col4: st.button("Finance")
with col5: st.button("Legal")

st.markdown("---")

# --- CHAT INTERFACE ---
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question about your documents..."):
    # 1. Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get answer from API
    with st.spinner("Thinking..."):
        try:
            payload = {"question": prompt, "session_id": session_id}
            response = requests.post(f"{API_URL}/chat", data=payload)
            
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer found.")
            else:
                answer = f"Error: {response.text}"
        except Exception as e:
            answer = f"Connection failed: {e}"

    # 3. Display Assistant Message
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)