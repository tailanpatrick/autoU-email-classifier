from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os


sys.path.append(os.path.dirname(__file__))

from services.classifier import classify_email, generate_response
from services.pdf_utils import extract_text_from_pdf_bytes

app = Flask(__name__)
CORS(app, origins=[
    "https://auto-u-email-classifier.vercel.app",
    "https://auto-u-email-classifier-n0d077zsj-tailanpatricks-projects.vercel.app"
])

@app.route("/api/process-email", methods=["POST"])
def process_email():
    try:
        email_text = ""


        text = request.form.get("text")
        if text and text.strip():
            email_text = text.strip()


        file = request.files.get("file")
        if file:
            file_bytes = file.read()
            if file.filename.endswith(".txt"):
                file_text = file_bytes.decode("utf-8").strip()
            elif file.filename.endswith(".pdf"):
    
                file_text = extract_text_from_pdf_bytes(file_bytes)
            else:
                return jsonify({"error": "Formato de arquivo não suportado. Use .txt ou .pdf"}), 400

            email_text = (email_text + "\n" + file_text).strip() if email_text else file_text

        if not email_text:
            return jsonify({"error": "Nenhum texto ou arquivo enviado."}), 400


        category = classify_email(email_text)
        response_text = generate_response(category, email_text)

        return jsonify({"categoria": category, "resposta": response_text})

    except Exception as e:
        import traceback
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500
