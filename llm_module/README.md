# RoboLLM

Minimal repository. See the `llm_module` folder for implementation. Set the `GEMINI_API_KEY` environment variable and run the scripts in `llm_module` as needed.

Examples:

```
cd llm_module
python main.py
```

## Quick Start

### 1. Set API Key
```bash
export GEMINI_API_KEY="your-api-key"
```

### 2. Verify Setup
```bash
cd llm_module
python verify.py
```

### 3. Run Experiments
```bash
cd llm_module
python experiments.py
```

### 4. Try Interactive Demo
```bash
cd llm_module
python main.py
```

---

## What This Module Does

✅ **Separation of Concerns** - Each module has one job  
✅ **Output Contracts** - Strict format requirements & validation  
✅ **Failure Handling** - Retry + fallback (never silent failures)  
✅ **Logging & Traceability** - Inspect prompt, response, and errors  
✅ **Non-Determinism Aware** - Acknowledged and handled  

---

## Core Concepts

### 1. Prompts Are Separated (prompts.py)
```python
# Prompts stored in one place, not hardcoded
TEMPLATES = {
    "structured_info": """Extract JSON with: name, age, location
Do not include any text before or after JSON."""
}

# Application uses template names only
prompt = format_prompt("structured_info", text="Alice is 28 in NYC")
```

**Benefit**: Change a prompt → edit `TEMPLATES` only. Code doesn't change.

### 2. Output Contracts Are Enforced (parser.py)
```python
# Model instructed to return specific format
response = call_gemini(api_key, prompt)

# Schema validation (strict)
result = parse_json(
    response,
    required_keys=["name", "age", "location"],
    allow_extra_keys=False
)

# Invalid outputs are caught (not silent)
if not result.success:
    print(result.validation_steps)  # See exactly why it failed
```

**Benefit**: Catch invalid outputs early. Debug with full trace.

### 3. Failures Are Handled Gracefully (safety.py)
```python
# Retry with backoff + fallback
response = call_with_retry_and_fallback(
    call_gemini,
    args=(api_key, prompt),
    fallback_value='{"name": "unknown"}',
    max_attempts=3
)

# Never breaks silently - logged at each step
```

**Benefit**: Resilient to API failures. Graceful degradation.

### 4. Everything Is Logged (logger.py)
```python
# Prompt sent: ✓
# Response received: ✓ (with latency)
# Validation steps: ✓ (detailed trace)
# Failures/retries: ✓ (logged)
# Final result: ✓
```

**Benefit**: Debug after execution. Inspect what actually happened.

---

## Module Files

```
llm_module/
├── llm_client.py       # Raw API calls (returns text + metadata)
├── prompts.py          # Prompt templates (format instructions included)
├── parser.py           # Validation (schema checking, error traces)
├── safety.py           # Retry + fallback (failure handling)
├── logger.py           # Structured logging
├── __init__.py         # Module exports
├── experiments.py      # Demonstrations of all features
├── main.py             # Interactive chatbot
├── verify.py           # Verification script
├── DESIGN.md           # Detailed design explanation
└── SIMPLIFIED_README.md # Beginner-friendly overview
```

---

## How It Fits Together

```
Application asks for: format_prompt("template_name", variables)
         ↓
  Prompt injected with format instructions
         ↓
  API call: call_gemini(api_key, prompt)
         ↓
  Response + metadata returned
         ↓
  Validation: parse_json(response, schema)
         ↓
  ParseResult: success=True/False, data, validation_steps
         ↓
  Application uses result.data or handles result.error
```

---

## Mandatory Requirements Met

See [REQUIREMENTS.md](REQUIREMENTS.md) for detailed validation.

✅ **Prompt Management** - Not hardcoded, separated in prompts.py  
✅ **Output Contracts** - Strict format + schema validation  
✅ **Failure Handling** - Retry/fallback/validation  
✅ **Logging** - Prompt, response, errors all traced  
✅ **Non-Determinism** - Acknowledged in code & docs  

✅ **4 Experiments** - Demonstrating all requirements  
✅ **Code Quality** - Modular, readable, reusable  

---

## Usage Examples

### Basic Call
```python
from llm_module import format_prompt, call_gemini, parse_json
import os

api_key = os.getenv("GEMINI_API_KEY")
prompt = format_prompt("qa", question="What is Python?")
response, metadata = call_gemini(api_key, prompt)
result = parse_json(response)

if result.success:
    print(result.data)
else:
    print(f"Failed: {result.error}")
    for step in result.validation_steps:
        print(f"  {step}")
```

### With Retry + Fallback
```python
from llm_module import call_with_retry_and_fallback

response = call_with_retry_and_fallback(
    call_gemini,
    args=(api_key, prompt),
    fallback_value='{"error": "Unable to process"}',
    max_attempts=3
)
```

### Structured Extraction
```python
response, _ = call_gemini(api_key, prompt)
result = parse_json(
    response,
    required_keys=["name", "age", "email"],
    allow_extra_keys=False
)

if result.success:
    print(result.data)  # {"name": "...", "age": "...", "email": "..."}
else:
    print(f"Schema error: {result.error}")
```

---

## One Limitation: Model Compliance

We rely on the model following format instructions. Not all models always comply.

**How we handle it**:
1. Explicit format instructions in every prompt (reduce variation)
2. Strict validation (catch non-compliance)
3. Retry + fallback (handle gracefully)

**Trade-off**: Makes problems **obvious** rather than silent failures downstream.

---

## Design Philosophy

**No frameworks. No magic. Just clear, composable functions.**

- Each module does one thing
- Every operation is loggable
- Failures are explicit, not silent
- Input/output contracts are clear

This serves as foundation for:
- Semantic search (validated extraction)
- RAG (trusted retrieval + generation)
- Multi-step workflows (explicit error handling)
- Agentic systems (structured tool calling)

---

**Status**: ✅ All mandatory requirements met and demonstrated.  
**Ready for**: Production use as LLM foundation layer.
