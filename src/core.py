import os
import json
import mimetypes
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# Load env variables from .env file
load_dotenv()

# Default Gemini model
DEFAULT_MODEL = "gemini-2.5-flash"

def configure_client(api_key=None):
    """Configures the google-generativeai client using the provided key or env variable."""
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError(
            "Gemini API key not found. Please set GEMINI_API_KEY in your environment, "
            "provide a .env file, or pass the key explicitly."
        )
    genai.configure(api_key=key)

def load_file_for_gemini(file_path):
    """Loads a file (Image, PDF, Text) and returns a format acceptable by the Gemini SDK."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    ext = os.path.splitext(file_path)[1].lower()
    
    # Process Images
    if ext in ['.png', '.jpg', '.jpeg', '.webp']:
        try:
            return Image.open(file_path)
        except Exception as e:
            raise ValueError(f"Failed to open image file {file_path}: {e}")
            
    # Process PDFs
    elif ext == '.pdf':
        try:
            with open(file_path, "rb") as f:
                pdf_bytes = f.read()
            return {
                "mime_type": "application/pdf",
                "data": pdf_bytes
            }
        except Exception as e:
            raise ValueError(f"Failed to read PDF file {file_path}: {e}")
            
    # Process Text/CSV/JSON/HTML
    elif ext in ['.txt', '.csv', '.json', '.html']:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return f"Content of {os.path.basename(file_path)}:\n\n{content}"
        except Exception as e:
            raise ValueError(f"Failed to read text file {file_path}: {e}")
            
    # Fallback/Generic binary or documents
    else:
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = "application/octet-stream"
            return {
                "mime_type": mime_type,
                "data": data
            }
        except Exception as e:
            raise ValueError(f"Failed to load file {file_path}: {e}")

def extract_structured_data(file_path, api_key=None, model_name=DEFAULT_MODEL):
    """Extracts structured key-value data from a document in JSON format."""
    configure_client(api_key)
    model = genai.GenerativeModel(model_name)
    
    file_part = load_file_for_gemini(file_path)
    
    prompt = (
        "You are an expert document parsing agent.\n"
        "Analyze the provided document and extract all available key-value pairs, metadata, "
        "tabular data, checkboxes, dates, and signature statuses.\n"
        "Organize the output into logical JSON objects (e.g. document_type, sender, recipient, "
        "dates, line_items, values, metadata, checklist_items, signature_details).\n"
        "Ensure all keys are descriptive snake_case strings. Return ONLY valid JSON format.\n"
    )
    
    response = model.generate_content(
        [file_part, prompt],
        generation_config={"response_mime_type": "application/json"}
    )
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        # Fallback if model didn't return pure JSON (e.g. if wrapped in codeblocks)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())

def ask_question(file_path, question, api_key=None, model_name=DEFAULT_MODEL):
    """Answers a question about a single document."""
    configure_client(api_key)
    model = genai.GenerativeModel(model_name)
    
    file_part = load_file_for_gemini(file_path)
    
    prompt = (
        f"Analyze this document and answer the following question as accurately and "
        f"concisely as possible.\n\n"
        f"Question: {question}\n\n"
        f"Provide your answer with references to specific parts of the document if possible. "
        f"If the answer cannot be found in the document, state 'Information not found in the document'."
    )
    
    response = model.generate_content([file_part, prompt])
    return response.text.strip()

def summarize_form(file_path, api_key=None, model_name=DEFAULT_MODEL):
    """Generates a concise markdown summary highlighting key aspects of a form."""
    configure_client(api_key)
    model = genai.GenerativeModel(model_name)
    
    file_part = load_file_for_gemini(file_path)
    
    prompt = (
        "You are an expert document summarizer.\n"
        "Generate a structured, professional Markdown summary of the provided document.\n"
        "Your summary must include the following sections:\n"
        "1. **Document Overview**: 2-3 sentences explaining what this document is (type, date, purpose).\n"
        "2. **Primary Parties**: Names and details of stakeholders involved (e.g., Landlord/Tenant, Patient, Vendor/Client).\n"
        "3. **Key Financials / Critical Values**: Highlight dates, monetary figures, fees, IDs, or crucial numeric metrics.\n"
        "4. **Important Terms / Highlights**: Outline core policies, checklists, allergies, notes, or contract clauses.\n"
        "5. **Execution Status**: Mention if signatures, dates, or checkboxes are completed or empty.\n\n"
        "Use clean spacing, bold text, and clear bullet points."
    )
    
    response = model.generate_content([file_part, prompt])
    return response.text.strip()

def analyze_multiple_forms(file_paths, query, api_key=None, model_name=DEFAULT_MODEL):
    """Analyzes multiple documents together to answer cross-form queries."""
    configure_client(api_key)
    model = genai.GenerativeModel(model_name)
    
    contents = []
    for idx, path in enumerate(file_paths):
        filename = os.path.basename(path)
        contents.append(f"\n=== DOCUMENT {idx+1}: {filename} ===")
        contents.append(load_file_for_gemini(path))
        
    prompt = (
        f"\n\nBased on all the documents provided above, please answer the following analysis query:\n"
        f"Query: {query}\n\n"
        f"Identify common patterns, compare values, or extract aggregated values across the documents. "
        f"Provide a structured response using Markdown tables or lists to compare findings where appropriate."
    )
    contents.append(prompt)
    
    response = model.generate_content(contents)
    return response.text.strip()
