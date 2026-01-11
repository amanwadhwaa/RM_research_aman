"""Retry logic and failure handling."""

import time
from typing import Callable, Any, Optional


def retry_on_failure(
    func: Callable,
    args: tuple = (),
    kwargs: dict = None,
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
) -> Optional[Any]:
    """
    Retry a function call if it fails.
    
    Args:
        func: The function to call
        args: Positional arguments to pass
        kwargs: Keyword arguments to pass
        max_attempts: How many times to try
        delay: Wait this many seconds between attempts
        backoff: Multiply delay by this after each failure
        
    Returns:
        The function's result if successful, or None if all attempts fail
        
    Example:
        result = retry_on_failure(api_call, args=(prompt,), max_attempts=3)
    """
    if kwargs is None:
        kwargs = {}
    
    current_delay = delay
    last_error = None
    
    for attempt in range(1, max_attempts + 1):
        try:
            # Try to call the function
            return func(*args, **kwargs)
        except Exception as e:
            last_error = e
            
            # If this was the last attempt, stop trying
            if attempt == max_attempts:
                print(f"❌ Failed after {max_attempts} attempts. Last error: {e}")
                return None
            
            # Otherwise, wait and retry
            print(f"⚠️  Attempt {attempt} failed: {e}")
            print(f"   Retrying in {current_delay}s...")
            time.sleep(current_delay)
            current_delay *= backoff


def call_with_fallback(
    func: Callable,
    args: tuple = (),
    kwargs: dict = None,
    fallback_value: Any = None,
) -> Any:
    """
    Call a function and return a fallback value if it fails.
    
    Args:
        func: The function to call
        args: Positional arguments
        kwargs: Keyword arguments
        fallback_value: Return this if the function fails
        
    Returns:
        The function's result, or fallback_value if it fails
        
    Example:
        response = call_with_fallback(
            api_call,
            args=(prompt,),
            fallback_value="I don't know"
        )
    """
    if kwargs is None:
        kwargs = {}
    
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"⚠️  Function failed: {e}. Using fallback: {fallback_value}")
        return fallback_value


def call_with_retry_and_fallback(
    func: Callable,
    args: tuple = (),
    kwargs: dict = None,
    fallback_value: Any = None,
    max_attempts: int = 3,
) -> Any:
    """
    Retry a function, and use a fallback if all retries fail.
    
    This combines both strategies:
    1. First, retry the function multiple times
    2. If all retries fail, return a sensible default
    
    Args:
        func: The function to call
        args: Positional arguments
        kwargs: Keyword arguments
        fallback_value: Return this if all retries fail
        max_attempts: How many times to try
        
    Returns:
        The function's result, or fallback_value if all attempts fail
    """
    if kwargs is None:
        kwargs = {}
    
    result = retry_on_failure(
        func,
        args=args,
        kwargs=kwargs,
        max_attempts=max_attempts,
    )
    
    if result is None:
        return fallback_value
    
    return result
