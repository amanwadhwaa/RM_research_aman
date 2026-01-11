"""
Simplified LLM Module - Core Concepts Only

This module teaches the 5 core concepts of working with LLMs:

1. llm_client.py   - Raw API calls
2. prompts.py      - Prompt templates & formatting
3. parser.py       - Parse & validate output
4. safety.py       - Retry & fallback handling
5. logger.py       - Simple logging
"""

# Raw API
from .llm_client import call_gemini

# Prompts
from .prompts import format_prompt, get_template, TEMPLATES, SYSTEM_INSTRUCTION

# Parsing
from .parser import parse_json, validate_choice, validate_length, ParseResult

# Safety
from .safety import retry_on_failure, call_with_fallback, call_with_retry_and_fallback

# Logging
from .logger import get_logger, Logger

__all__ = [
    # Raw API
    "call_gemini",
    # Prompts
    "format_prompt",
    "get_template",
    "TEMPLATES",
    "SYSTEM_INSTRUCTION",
    # Parsing
    "parse_json",
    "validate_choice",
    "validate_length",
    "ParseResult",
    # Safety
    "retry_on_failure",
    "call_with_fallback",
    "call_with_retry_and_fallback",
    # Logging
    "get_logger",
    "Logger",
]
