

import google.generativeai as genai
import time
from logger import get_logger

logger = get_logger(enabled=True)


def call_gemini(api_key: str, prompt: str, model: str = "gemini-2.5-flash") -> str:
    """
    Make a raw API call to Gemini.
    
    This is the simplest possible API interaction:
    1. Configure with API key
    2. Create model instance
    3. Send prompt
    4. Return response text
    
    Args:
        api_key: Your Gemini API key
        prompt: The text to send to the model (should already include format instructions)
        model: Which Gemini model to use
        
    Returns:
        The model's response text as a string
        
    Raises:
        Exception: If the API call fails (caller should handle with retry logic)
    
    IMPORTANT: This function does NOT validate output format.
    That is the responsibility of the caller (parser.py).
    The caller must check that the response matches the expected format.
    
    NOTE: Logging and tracing happen as side effects only.
    """
    # Step 1: Tell genai library about our API key
    genai.configure(api_key=api_key)
    
    # Step 2: Create a model instance
    llm_model = genai.GenerativeModel(model)
    
    # Step 3: Send prompt and get response (with tracing as side effect)
    start_time = time.time()
    response = llm_model.generate_content(prompt)
    latency_ms = (time.time() - start_time) * 1000
    
    # Step 4: Extract text
    response_text = response.text
    
    # Logging as side effect only
    logger.info(f"API call completed in {latency_ms:.0f}ms")
    
    return response_text
