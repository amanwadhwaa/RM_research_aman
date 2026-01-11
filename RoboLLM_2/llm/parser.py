import json

class OutputValidationError(Exception):
    pass

def parse_and_validate(raw_output: str) -> dict:
    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError:
        raise OutputValidationError("Output is not valid JSON")

    if not isinstance(data, dict):
        raise OutputValidationError("Output is not a JSON object")

    if "answer" not in data or "confidence" not in data:
        raise OutputValidationError("Missing required keys")

    if not isinstance(data["confidence"], (int, float)):
        raise OutputValidationError("Confidence must be a number")

    return data
