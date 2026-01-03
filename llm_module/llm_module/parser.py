"""Parse and validate LLM output against expected schemas."""

import json
import re
from typing import Any, Dict, List, Optional


class ParseResult:
    """Result of parsing output with full traceability."""
    
    def __init__(
        self,
        success: bool,
        data: Any = None,
        error: str = None,
        raw_text: str = "",
        validation_steps: List[str] = None,
    ):
        self.success = success
        self.data = data
        self.error = error
        self.raw_text = raw_text
        self.validation_steps = validation_steps or []
        
    def __repr__(self):
        if self.success:
            return f"ParseResult(success=True, data={self.data}, steps={len(self.validation_steps)})"
        else:
            return f"ParseResult(success=False, error={self.error}, steps={self.validation_steps})"


def parse_json(
    text: str,
    required_keys: Optional[List[str]] = None,
    allow_extra_keys: bool = False,
) -> ParseResult:
    """
    Try to extract and parse JSON from text with schema validation.
    
    Args:
        text: Text that should contain JSON
        required_keys: List of keys that MUST be in the JSON (e.g., ["name", "age"])
        allow_extra_keys: If False, fail if JSON has keys not in required_keys
        
    Returns:
        ParseResult with full validation trace
        
    Example:
        result = parse_json(
            response,
            required_keys=["name", "age", "email"],
            allow_extra_keys=False  # Strict schema
        )
        if not result.success:
            print(result.validation_steps)  # See exactly what failed
    """
    steps = []
    
    # Step 1: Check if input is empty
    if not text or not text.strip():
        steps.append("❌ Input is empty")
        return ParseResult(success=False, error="Empty response", validation_steps=steps)
    
    steps.append(f"✓ Input received ({len(text)} chars)")
    
    # Step 2: Try direct JSON parsing
    try:
        data = json.loads(text)
        steps.append("✓ Direct JSON parse succeeded")
    except json.JSONDecodeError as e:
        steps.append(f"✗ Direct JSON parse failed: {str(e)[:60]}")
        
        # Step 3: Try to extract JSON from surrounding text
        json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
                steps.append(f"✓ Extracted JSON from text (found at char {json_match.start()})")
            except json.JSONDecodeError as e2:
                steps.append(f"✗ Extracted JSON also invalid: {str(e2)[:60]}")
                return ParseResult(
                    success=False,
                    error=f"No valid JSON found: {str(e)}",
                    raw_text=text,
                    validation_steps=steps,
                )
        else:
            steps.append("✗ No JSON structure found in text")
            return ParseResult(
                success=False,
                error="No JSON structure found",
                raw_text=text,
                validation_steps=steps,
            )
    
    # Step 4: Validate schema (required keys)
    if required_keys:
        missing_keys = [k for k in required_keys if k not in data]
        if missing_keys:
            steps.append(f"❌ Missing required keys: {missing_keys}")
            return ParseResult(
                success=False,
                error=f"Schema violation: missing keys {missing_keys}",
                data=data,
                raw_text=text,
                validation_steps=steps,
            )
        steps.append(f"✓ All required keys present: {required_keys}")
        
        # Step 5: Check for extra keys (if strict)
        if not allow_extra_keys:
            extra_keys = [k for k in data.keys() if k not in required_keys]
            if extra_keys:
                steps.append(f"❌ Extra keys not allowed: {extra_keys}")
                return ParseResult(
                    success=False,
                    error=f"Schema violation: unexpected keys {extra_keys}",
                    data=data,
                    raw_text=text,
                    validation_steps=steps,
                )
            steps.append(f"✓ No extra keys (strict schema enforced)")
    
    steps.append("✅ JSON validation complete")
    return ParseResult(success=True, data=data, raw_text=text, validation_steps=steps)


def validate_choice(text: str, valid_choices: List[str]) -> ParseResult:
    """
    Check if text matches one of the valid choices (case-insensitive).
    
    Args:
        text: The text to validate
        valid_choices: List of acceptable answers
        
    Returns:
        ParseResult with validation trace
    """
    steps = []
    
    if not text or not text.strip():
        steps.append("❌ Input is empty")
        return ParseResult(
            success=False,
            error="Empty response",
            validation_steps=steps,
        )
    
    steps.append(f"✓ Input received: '{text}'")
    
    # Normalize: lowercase and strip whitespace
    normalized = text.strip().lower()
    valid_normalized = [c.lower() for c in valid_choices]
    
    if normalized in valid_normalized:
        # Return the original choice (not lowercased)
        idx = valid_normalized.index(normalized)
        original_choice = valid_choices[idx]
        steps.append(f"✓ Matched choice: '{original_choice}'")
        return ParseResult(
            success=True,
            data=original_choice,
            raw_text=text,
            validation_steps=steps,
        )
    
    steps.append(f"❌ Not in allowed choices: {valid_choices}")
    return ParseResult(
        success=False,
        error=f"'{text}' is not one of: {valid_choices}",
        raw_text=text,
        validation_steps=steps,
    )


def validate_length(
    text: str,
    min_length: int = 0,
    max_length: Optional[int] = None,
) -> ParseResult:
    """
    Check if text length is within bounds.
    
    Args:
        text: The text to validate
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        
    Returns:
        ParseResult with validation trace
    """
    steps = []
    length = len(text)
    steps.append(f"✓ Text length: {length} chars")
    
    if min_length > 0 and length < min_length:
        steps.append(f"❌ Too short: {length} < {min_length}")
        return ParseResult(
            success=False,
            error=f"Text too short: {length} < {min_length}",
            raw_text=text,
            validation_steps=steps,
        )
    
    if max_length and length > max_length:
        steps.append(f"❌ Too long: {length} > {max_length}")
        return ParseResult(
            success=False,
            error=f"Text too long: {length} > {max_length}",
            raw_text=text,
            validation_steps=steps,
        )
    
    steps.append(f"✓ Length within bounds")
    return ParseResult(success=True, data=text, raw_text=text, validation_steps=steps)
