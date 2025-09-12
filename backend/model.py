import os
from dotenv import load_dotenv
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

    prompt+= "a resposta deve ter no máximo 50 palavras sem cortar palavras"
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content.strip()
