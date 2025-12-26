import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")
print("LLM: Hello! How can I assist you today? (Type 'exit' to quit)")
while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("LLM: Goodbye 👋")
        break

    response = model.generate_content(user_input)
    print("LLM:", response.text)
