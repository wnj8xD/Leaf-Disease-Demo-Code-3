# AI chuẩn đoán bệnh & cách chữa

import os
from openai import OpenAI
from dotenv import load_dotenv

# 🔥 Load biến môi trường từ file .env
load_dotenv()

# 🔑 Lấy API Key từ biến môi trường
api_key = os.getenv("OPENROUTER_API_KEY")

# ⚠️ Báo lỗi nếu không có API key
if not api_key:
    raise ValueError("⚠️ OPENROUTER_API_KEY is missing in .env or not loaded properly")

# ✅ Khởi tạo client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

def get_disease_info(disease_name: str, plant_type: str) -> str:
    prompt = f"""
    You are a plant disease expert helping farmers.
    For the disease '{disease_name}' on plant '{plant_type}', please write a short explanation (no more than 80 words) including:

    - Cause
    - Symptoms
    - Treatment and prevention tips

    Use simple language and return the result in this format:

    📌 Disease: ...
    💥 Cause: ...
    😷 Symptoms: ...
    💊 Treatment & Prevention: ...
    """

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",  # miễn phí
        messages=[
            {"role": "system", "content": "You are a plant disease assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
