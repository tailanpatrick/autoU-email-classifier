from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
import uvicorn
import io
import model

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para produção, coloque apenas o domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Extrair texto de um PDF
def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    text = ""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

# Endpoint 
@app.post("/process-email")
async def process_email(
    text: str = Form(None),
    file: UploadFile = File(None)
):
    email_text = ""

    if text and text.strip():
        email_text = text.strip()


    if file:
        file_bytes = await file.read()
        file_text = ""
        if file.filename.endswith(".txt"):
            file_text = file_bytes.decode("utf-8").strip()
        elif file.filename.endswith(".pdf"):
            file_text = extract_text_from_pdf_bytes(file_bytes)
        else:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado. Use .txt ou .pdf")
  
  
        email_text = (email_text + "\n" + file_text).strip() if email_text else file_text

    if not email_text:
        raise HTTPException(status_code=400, error="Nenhum texto ou arquivo enviado.")


    category = model.classify_email(email_text)
    response_text = model.generate_response(category, email_text)

    return JSONResponse(content={
        "categoria": category,
        "resposta": response_text
    })

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
