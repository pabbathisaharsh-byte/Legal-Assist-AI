import os
from pypdf import PdfReader
import docx

def parse_document(uploaded_file) -> str:
    """
    Extracts text from an uploaded file (PDF, DOCX, or TXT).
    uploaded_file: a Streamlit UploadedFile object.
    """
    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        reader = PdfReader(uploaded_file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text

    elif ext == ".docx":
        document = docx.Document(uploaded_file)
        text = "\n".join(para.text for para in document.paragraphs)
        return text

    elif ext == ".txt":
        return uploaded_file.read().decode("utf-8")

    else:
        raise ValueError(f"Unsupported file type: {ext}")