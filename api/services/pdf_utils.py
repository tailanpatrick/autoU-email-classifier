from PyPDF2 import PdfReader
import io

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    text = ""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()
