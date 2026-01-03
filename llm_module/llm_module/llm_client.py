

import google.generativeai as genai
import time
from typing import Dict, Any, Tuple


def call_gemini(api_key: str, prompt: str, model: str = "gemini-2.5-flash") -> Tuple[str, Dict[str, Any]]:
    """
    Make a raw API call to Gemini with tracing.
    
    This is the simplest possible API interaction:
    1. Configure with API key
    2. Create model instance
    3. Send prompt
    4. Return response text + metadata
    
    Args:
        api_key: Your Gemini API key
        prompt: The text to send to the model (should already include format instructions)
        model: Which Gemini model to use
        
    Returns:
        Tuple of (response_text, metadata_dict) where metadata contains:
        - prompt_length: Length of the prompt sent
        - response_length: Length of response received
        - latency_ms: Time taken for API call
        - timestamp: When the call was made
        - raw_response: Full response object for inspection
        
    Raises:
        Exception: If the API call fails (caller should handle with retry logic)
    
    IMPORTANT: This function does NOT validate output format.
    That is the responsibility of the caller (parser.py).
    The caller must check that the response matches the expected format.
    """
    # Step 1: Tell genai library about our API key
    genai.configure(api_key=api_key)
    
    # Step 2: Create a model instance
    llm_model = genai.GenerativeModel(model)
    
    # Step 3: Send prompt and get response
    start_time = time.time()
    response = llm_model.generate_content(prompt)
    latency_ms = (time.time() - start_time) * 1000
    
    # Step 4: Extract text and build metadata
    response_text = response.text
    
    metadata = {
        "prompt_length": len(prompt),
        "response_length": len(response_text),
        "latency_ms": round(latency_ms, 2),
        "model": model,
        "timestamp": time.time(),
    }
    
    return response_text, metadata
