from llm.prompts import build_prompt
from llm.llm_client import call_llm
from llm.parser import parse_and_validate, OutputValidationError

def run(question: str):
    prompt = build_prompt(question)

    for attempt in range(2):
        raw_output = call_llm(prompt)
        try:
            return parse_and_validate(raw_output)
        except OutputValidationError:
            if attempt == 1:
                raise

if __name__ == "__main__":
    while True:
        user_question = input("You: ")
        if user_question.lower() in ("exit", "quit"):
            break

        try:
            result = run(user_question)
            print("Assistant:", result["answer"])
        except OutputValidationError as e:
            print("Assistant error:", e)
