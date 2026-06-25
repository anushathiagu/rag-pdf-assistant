import streamlit as st
from rag_engine import get_pdf_text, get_text_chunks, get_answer

st.set_page_config(
    page_title="AI PDF Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0f0f1a; }
    .stApp { background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%); }
    h1 { color: #a855f7 !important; text-align: center; font-size: 2.5rem !important; }
    .subtitle { text-align: center; color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem; }
    .answer-box { background: #1e1b4b; border-left: 4px solid #a855f7;
        padding: 1.5rem; border-radius: 10px; color: #e2e8f0; margin-top: 1rem; }
    .stTextInput input { background-color: #1e1b4b !important; color: white !important;
        border: 1px solid #a855f7 !important; border-radius: 8px !important; }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🤖 AI PDF Question Answering Assistant")
st.markdown('<p class="subtitle">Upload any PDF and ask questions — powered by Google Gemini AI</p>',
            unsafe_allow_html=True)
st.divider()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    st.markdown("### 📌 How to Use")
    st.markdown("1. 📄 Upload your PDF file")
    st.markdown("2. ⏳ Wait for processing")
    st.markdown("3. ❓ Type your question")
    st.markdown("4. 🤖 Get AI answer!")
    st.divider()
    st.markdown("### 🛠 Built With")
    st.markdown("- 🐍 Python")
    st.markdown("- 🔗 LangChain")
    st.markdown("- 🤖 Google Gemini AI")
    st.markdown("- 🎈 Streamlit")
    st.divider()
    st.markdown("**Made by Anusha** ")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📄 Upload Your PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file:
        with st.spinner("🔍 Reading and processing your PDF..."):
            text = get_pdf_text(uploaded_file)
            chunks = get_text_chunks(text)
        st.success(f"✅ PDF processed! {len(chunks)} sections found.")
        st.session_state['chunks'] = chunks
        st.session_state['filename'] = uploaded_file.name

with col2:
    st.markdown("### ❓ Ask Your Question")
    if 'chunks' in st.session_state:
        question = st.text_input("Type your question here:", 
                                  placeholder="e.g. What is the main topic?")
        if question:
            with st.spinner("🤖 AI is thinking..."):
                answer = get_answer(st.session_state['chunks'], question)
            st.markdown("### 💡 Answer:")
            st.markdown(f'<div class="answer-box">{answer}</div>',
                       unsafe_allow_html=True)

            # Chat history
            if 'history' not in st.session_state:
                st.session_state['history'] = []
            st.session_state['history'].append((question, answer))
    else:
        st.info("👈 Please upload a PDF first!")

# Chat history section
if 'history' in st.session_state and len(st.session_state['history']) > 0:
    st.divider()
    st.markdown("### 🕐 Previous Questions")
    for i, (q, a) in enumerate(reversed(st.session_state['history'])):
        with st.expander(f"Q{len(st.session_state['history'])-i}: {q}"):
            st.write(a)
