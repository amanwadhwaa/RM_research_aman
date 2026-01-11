import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")

def call_llm(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text
