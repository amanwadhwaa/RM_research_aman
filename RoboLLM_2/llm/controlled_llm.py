from llm.llm_client import call_llm
from llm.parser import parse_and_validate
from llm.prompts import build_prompt

class ControlledLLM:
    def __init__(self, max_retries=2):
        self.max_retries = max_retries

    def generate(self, user_prompt: str):
        last_error = None

        for attempt in range(self.max_retries):
            try:
                prompt = build_prompt(user_prompt)
                raw = call_llm(prompt)
                return parse_and_validate(raw)
            except Exception as e:
                last_error = e

        raise RuntimeError(f"LLM failed after retries: {last_error}")