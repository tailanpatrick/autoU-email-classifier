from dotenv import load_dotenv
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
import io
import openai

load_dotenv()  
openai.api_key = os.getenv("OPENAI_API_KEY")


# Classifica o email em Produtivo ou Improdutivo
def classify_email(text: str) -> str:
    prompt = f"""
Classifique este email como 'Produtivo' ou 'Improdutivo'.
Regras:
- Produtivo: Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).
- Improdutivo: Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos).
Email: "{text}"
Responda apenas com a palavra Produtivo ou Improdutivo.
"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10
    )
    categoria = response.choices[0].message.content.strip()
    return categoria


# Gera uma resposta automática para o email com base na categoria e texto.
def generate_response(category: str, text: str) -> str:
    if category == "Produtivo":
        prompt = f"O email: {text}\n\nFoi classificado como Produtivo. Gere uma resposta curta e profissional para o remetente."
    else:
        prompt = f"O email: {text}\n\nFoi classificado como Improdutivo. Gere uma resposta curta e educada para o remetente."

    prompt += " A resposta deve ter no máximo 50 palavras, não cortar palavras, e NÃO deve incluir '[Seu nome]' em hipótese alguma. E NÂO incluir se é PRODUTIVO OU IMPRODUTIVO"

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250
    )
    return response.choices[0].message.content.strip()

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://auto-u-email-classifier.vercel.app",
        "https://auto-u-email-classifier-n0d077zsj-tailanpatricks-projects.vercel.app"
    ],
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
        raise HTTPException(status_code=400, detail="Nenhum texto ou arquivo enviado.")


    category = classify_email(email_text)
    response_text = generate_response(category, email_text)

    return JSONResponse(content={
        "categoria": category,
        "resposta": response_text
    })
    
    
from mangum import Mangum

handler = Mangum(app)

