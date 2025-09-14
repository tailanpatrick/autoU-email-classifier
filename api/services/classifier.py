import os
import openai
from flask import abort

def classify_email(text: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        abort(500, description="OPENAI_API_KEY não definido")
    openai.api_key = api_key

    prompt = f"""
Classifique este email como 'Produtivo' ou 'Improdutivo'.

**Categorias de Classificação**

- **Produtivo:** Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).
- **Improdutivo:** Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos).
Email: "{text}"
Responda apenas com 'Produtivo' ou 'Improdutivo'.
"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10
    )
    return response.choices[0].message.content.strip()


def generate_response(category: str, text: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key

    if category == "Produtivo":
        prompt = f"O email: {text}\n\nGere uma resposta curta e profissional."
    else:
        prompt = f"O email: {text}\n\nGere uma resposta curta e educada."
    prompt += " Máx 50 palavras, não cortar palavras, NÃO incluir '[Seu nome]' ou categoria."

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250
    )
    return response.choices[0].message.content.strip()
