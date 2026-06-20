import streamlit as st
import os
import json
import tempfile
import sys
from PIL import Image

# Add project root to sys.path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.core import extract_structured_data, ask_question, summarize_form, analyze_multiple_forms

# Set up page configurations
st.set_page_config(
    page_title="Intelligent Form Agent",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main {
        background-color: #0d1117;
        color: #e6edf3;
    }
    
    /* Headers */
    h1 {
        font-weight: 700;
        background: linear-gradient(90deg, #17b978 0%, #1e3d59 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    h2, h3 {
        font-weight: 600;
        color: #17b978;
    }
    
    /* Card design */
    .feature-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .feature-card:hover {
        transform: translateY(-2px);
        border-color: #17b978;
    }
    
    /* Custom tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161b22;
        padding: 6px;
        border-radius: 8px;
        border: 1px solid #30363d;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 6px;
        color: #8b949e;
        font-weight: 600;
        border: none;
        padding: 0 16px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #17b978;
        background-color: #21262d;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #17b978 !important;
        color: #ffffff !important;
    }
    
    /* Chat bubbles */
    .user-bubble {
        background-color: #1f2937;
        color: #e6edf3;
        padding: 10px 15px;
        border-radius: 15px 15px 0px 15px;
        margin: 5px 0 5px auto;
        max-width: 80%;
        width: fit-content;
        border: 1px solid #374151;
    }
    .agent-bubble {
        background-color: #0f172a;
        color: #e6edf3;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0px;
        margin: 5px auto 5px 0;
        max-width: 80%;
        width: fit-content;
        border: 1px solid #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State variables
if 'temp_files' not in st.session_state:
    st.session_state.temp_files = {}  # original_name -> temp_file_path
if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = {}  # filename -> json_data
if 'summaries' not in st.session_state:
    st.session_state.summaries = {}  # filename -> markdown_summary
if 'chat_histories' not in st.session_state:
    st.session_state.chat_histories = {}  # filename -> list of dicts: {'role': '...', 'text': '...'}
if 'active_file' not in st.session_state:
    st.session_state.active_file = None

def save_uploaded_file(uploaded_file):
    """Saves uploaded file to a temporary location and returns the path."""
    try:
        ext = os.path.splitext(uploaded_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
            temp_file.write(uploaded_file.read())
            return temp_file.name
    except Exception as e:
        st.error(f"Error saving uploaded file: {e}")
        return None

# App header
st.title("📄 Intelligent Form Agent")
st.markdown("##### *Read, Extract, and Explain Structured and Unstructured Documents using Gemini API*")
st.write("---")

# Sidebar Configuration
st.sidebar.image("https://img.icons8.com/clouds/100/document.png", width=80)
st.sidebar.markdown("### Agent Configuration")

# API Key input
env_key = os.getenv("GEMINI_API_KEY", "")
api_key = st.sidebar.text_input(
    "Enter Gemini API Key",
    type="password",
    value=env_key,
    placeholder="AIzaSy...",
    help="Provided in .env, or input here to override."
)

if api_key:
    st.sidebar.success("Gemini API Key configured! ✅")
else:
    st.sidebar.warning("Gemini API Key is missing. ⚠️")
    st.sidebar.info("Get a key from Google AI Studio and paste it above, or add `GEMINI_API_KEY` to your `.env` file.")

# File Uploader
st.sidebar.markdown("### Document Upload")
uploaded_files = st.sidebar.file_uploader(
    "Upload forms (PDF or Images)",
    type=["pdf", "png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True
)

# Button to load sample forms
st.sidebar.markdown("---")
st.sidebar.markdown("### Demo Workspace")
if st.sidebar.button("💡 Load Pre-Generated Sample Forms"):
    sample_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    samples = ["sample_invoice.png", "sample_medical.png", "sample_rental.png"]
    
    loaded_any = False
    for filename in samples:
        path = os.path.join(sample_dir, filename)
        if os.path.exists(path):
            st.session_state.temp_files[filename] = path
            loaded_any = True
        else:
            st.sidebar.error(f"Sample not found: {filename}. Run data/generate_samples.py first.")
            
    if loaded_any:
        st.sidebar.success("Sample forms loaded successfully! 🎉")
        st.rerun()

# Handle uploaded files
if uploaded_files:
    for file in uploaded_files:
        if file.name not in st.session_state.temp_files:
            temp_path = save_uploaded_file(file)
            if temp_path:
                st.session_state.temp_files[file.name] = temp_path

# Main Logic Layout
if not st.session_state.temp_files:
    # No documents uploaded yet - show clean landing layout
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <h3>🔍 Structured Info Extraction</h3>
                <p>Upload form templates, bills, receipts, or medical charts. The Intelligent Form Agent extracts structured information (metadata, line items, totals, dates, names) directly into clean JSON formats.</p>
            </div>
            <div class="feature-card">
                <h3>💬 Intelligent Form Chat (Q&A)</h3>
                <p>Ask direct questions about any document. The agent reads the context and responds instantly. E.g., <em>"What is the late fee policy?"</em> or <em>"Is the tenant signature present?"</em></p>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <h3>📝 Comprehensive Summarizer</h3>
                <p>Generate styled Markdown summaries that outline document scope, key financial metrics, dates, and terms, saving you the trouble of reading full forms manually.</p>
            </div>
            <div class="feature-card">
                <h3>📊 Multi-Document Comparative Analytics</h3>
                <p>Load multiple forms to compare terms or check totals. E.g., <em>"Compare the monthly rent across all lease agreements"</em> or <em>"Summarize patient symptoms across these records."</em></p>
            </div>
            """, unsafe_allow_html=True
        )
    
    st.info("👈 Upload your own documents in the sidebar or click **Load Pre-Generated Sample Forms** to get started instantly!")

else:
    # Documents are available
    file_list = list(st.session_state.temp_files.keys())
    
    # Active document selector
    if st.session_state.active_file not in file_list:
        st.session_state.active_file = file_list[0]
        
    active_filename = st.selectbox(
        "Select Active Document to Analyze:",
        options=file_list,
        index=file_list.index(st.session_state.active_file)
    )
    st.session_state.active_file = active_filename
    active_path = st.session_state.temp_files[active_filename]
    
    # Visual side-by-side
    v_col1, v_col2 = st.columns([2, 3])
    
    with v_col1:
        st.markdown("### Document Preview")
        ext = os.path.splitext(active_filename)[1].lower()
        if ext in ['.png', '.jpg', '.jpeg', '.webp']:
            try:
                img = Image.open(active_path)
                st.image(img, use_container_width=True)
            except Exception as e:
                st.error(f"Could not render image: {e}")
        elif ext == '.pdf':
            st.info(f"📄 PDF Document: **{active_filename}**\n\n*(Natively parsed via Gemini API)*")
            # PDF icon/status card
            st.markdown(
                f"""
                <div style="background-color: #1e3d59; border-radius: 8px; padding: 20px; text-align: center;">
                    <h1 style="-webkit-text-fill-color: white; margin: 0;">PDF</h1>
                    <p style="color: #cccccc; margin-top: 10px;">{active_filename}</p>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.info(f"📄 Document: **{active_filename}**")
            
    with v_col2:
        st.markdown("### Agent Actions")
        
        # Tabs for actions
        tab_extract, tab_qa, tab_summary = st.tabs([
            "🔍 Structured JSON",
            "💬 Chat / Q&A",
            "📝 Executive Summary"
        ])
        
        # TAB 1: Structured JSON Extraction
        with tab_extract:
            st.write("Automatically extract form metadata, checkboxes, tables, and details.")
            if not api_key:
                st.error("Please provide a Gemini API Key in the sidebar to run extraction.")
            else:
                if active_filename not in st.session_state.extracted_data:
                    if st.button("🚀 Run Structured Extraction", key=f"btn_ext_{active_filename}"):
                        with st.spinner("Analyzing form layout and extracting details..."):
                            try:
                                data = extract_structured_data(active_path, api_key=api_key)
                                st.session_state.extracted_data[active_filename] = data
                                st.success("Extraction complete!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Extraction failed: {e}")
                
                if active_filename in st.session_state.extracted_data:
                    extracted_json = st.session_state.extracted_data[active_filename]
                    st.json(extracted_json)
                    
                    # Download JSON button
                    json_str = json.dumps(extracted_json, indent=2)
                    st.download_button(
                        label="📥 Download JSON Data",
                        data=json_str,
                        file_name=f"{os.path.splitext(active_filename)[0]}_extracted.json",
                        mime="application/json"
                    )
        
        # TAB 2: Interactive Chat/QA
        with tab_qa:
            st.write(f"Ask details specific to **{active_filename}**:")
            if not api_key:
                st.error("Please provide a Gemini API key in the sidebar.")
            else:
                # Initialize chat history for this specific file
                if active_filename not in st.session_state.chat_histories:
                    st.session_state.chat_histories[active_filename] = []
                    
                history = st.session_state.chat_histories[active_filename]
                
                # Show history
                for chat in history:
                    if chat['role'] == 'user':
                        st.markdown(f'<div class="user-bubble"><strong>You:</strong><br>{chat["text"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="agent-bubble"><strong>Agent:</strong><br>{chat["text"]}</div>', unsafe_allow_html=True)
                
                # Chat input
                user_msg = st.text_input("Ask a question about this form...", key=f"chat_input_{active_filename}")
                if st.button("Send", key=f"btn_send_{active_filename}"):
                    if user_msg:
                        # Append user msg
                        history.append({'role': 'user', 'text': user_msg})
                        
                        with st.spinner("Agent is thinking..."):
                            try:
                                response = ask_question(active_path, user_msg, api_key=api_key)
                                history.append({'role': 'agent', 'text': response})
                                st.rerun()
                            except Exception as e:
                                st.error(f"QA Call failed: {e}")
                                
                if history and st.button("Clear Chat", key=f"btn_clear_{active_filename}"):
                    st.session_state.chat_histories[active_filename] = []
                    st.rerun()
                    
        # TAB 3: Summary
        with tab_summary:
            st.write("Generate a formatted summary highlighting key stakeholders, financials, and terms.")
            if not api_key:
                st.error("Please provide a Gemini API Key in the sidebar.")
            else:
                if active_filename not in st.session_state.summaries:
                    if st.button("📝 Generate Summary", key=f"btn_sum_{active_filename}"):
                        with st.spinner("Summarizing document..."):
                            try:
                                summary = summarize_form(active_path, api_key=api_key)
                                st.session_state.summaries[active_filename] = summary
                                st.success("Summary generated!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Summarization failed: {e}")
                                
                if active_filename in st.session_state.summaries:
                    st.markdown(st.session_state.summaries[active_filename])
                    
                    st.download_button(
                        label="📥 Download Markdown Summary",
                        data=st.session_state.summaries[active_filename],
                        file_name=f"{os.path.splitext(active_filename)[0]}_summary.md",
                        mime="text/markdown"
                    )

    # Section 3: Cross-Document Analytics
    st.write("---")
    st.markdown("### 📊 Cross-Form Comparative Analytics")
    st.write("Analyze and compare multiple forms simultaneously. Select the documents to include, then write a query.")
    
    selected_docs = st.multiselect(
        "Select documents for comparison:",
        options=file_list,
        default=file_list
    )
    
    analysis_query = st.text_area(
        "Enter your cross-document query:",
        placeholder="e.g. Compare the dates, key values, and names of all parties across these lease agreements. Represent the output as a Markdown table.",
        value="Compare the main parties, dates, and financial metrics across all of these documents. Place key comparison details in a Markdown summary table."
    )
    
    if st.button("🔍 Run Multi-Document Analysis"):
        if not api_key:
            st.error("Please provide a Gemini API Key in the sidebar.")
        elif not selected_docs:
            st.warning("Please select at least one document for comparison.")
        elif not analysis_query:
            st.warning("Please write an analysis query.")
        else:
            with st.spinner("Analyzing selected documents in parallel..."):
                try:
                    paths = [st.session_state.temp_files[name] for name in selected_docs]
                    analysis_result = analyze_multiple_forms(paths, analysis_query, api_key=api_key)
                    st.markdown("#### Analysis Report")
                    st.markdown(analysis_result)
                except Exception as e:
                    st.error(f"Multi-document analysis failed: {e}")
