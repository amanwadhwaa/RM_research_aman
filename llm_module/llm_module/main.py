"""Glue code: Put it all together for a simple demo."""

import os
from llm_client import call_gemini
from prompts import format_prompt
from parser import parse_json, validate_choice, ParseResult
from safety import retry_on_failure, call_with_retry_and_fallback
from logger import get_logger


logger = get_logger(enabled=True)


def main():
    """Demo: Interactive chatbot showing all components."""
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY environment variable not set!")
        return
    
    logger.info("Initializing chatbot...")
    
    # Simple interactive loop
    print("\n" + "="*60)
    print("LLM Chatbot Demo - Type 'exit' to quit")
    print("="*60 + "\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            logger.info("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Example 1: Simple Q&A with retry
        logger.debug(f"User asked: {user_input}")
        
        # Format a prompt using templates
        prompt = format_prompt("qa", question=user_input)
        logger.debug(f"Formatted prompt: {prompt[:50]}...")
        
        # Call API with retry and fallback
        response = call_with_retry_and_fallback(
            call_gemini,
            args=(api_key, prompt),
            fallback_value="Sorry, I couldn't generate a response.",
            max_attempts=2,
        )
        
        logger.success("Got response")
        print(f"LLM: {response}\n")


def demo_parsing():
    """Show what parsing looks like."""
    print("\n" + "="*60)
    print("Demo: Output Parsing")
    print("="*60 + "\n")
    
    # Parse JSON
    json_text = 'The answer is {"name": "Alice", "age": 30}'
    result = parse_json(json_text)
    print(f"JSON parsing: {result}")
    
    # Validate choice
    choice_result = validate_choice("yes", ["yes", "no", "maybe"])
    print(f"Choice validation: {choice_result}")
    
    # Failed choice
    failed_choice = validate_choice("maybe", ["yes", "no"])
    print(f"Invalid choice: {failed_choice}")


if __name__ == "__main__":
    # Uncomment to see parsing demo
    # demo_parsing()
    
    # Run the interactive chatbot
    main()
