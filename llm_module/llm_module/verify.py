"""Quick validation that the module structure is correct and everything imports properly."""

import sys
import os

# Verify all required files exist
required_files = [
    "llm_client.py",
    "prompts.py",
    "parser.py",
    "safety.py",
    "logger.py",
    "__init__.py",
    "experiments.py",
]

print("Checking module structure...")
print("=" * 70)

all_good = True
for filename in required_files:
    path = os.path.join(os.path.dirname(__file__), filename)
    exists = os.path.exists(path)
    status = "✓" if exists else "✗"
    print(f"  {status} {filename}")
    if not exists:
        all_good = False

if not all_good:
    print("\n❌ Some files missing!")
    sys.exit(1)

print("\n" + "=" * 70)
print("Checking imports...")
print("=" * 70)

try:
    from llm_client import call_gemini
    print("✓ llm_client.call_gemini")
except ImportError as e:
    print(f"✗ llm_client: {e}")
    all_good = False

try:
    from prompts import format_prompt, get_template, TEMPLATES
    print("✓ prompts.format_prompt, get_template, TEMPLATES")
except ImportError as e:
    print(f"✗ prompts: {e}")
    all_good = False

try:
    from parser import parse_json, validate_choice, validate_length, ParseResult
    print("✓ parser.parse_json, validate_choice, validate_length, ParseResult")
except ImportError as e:
    print(f"✗ parser: {e}")
    all_good = False

try:
    from safety import retry_on_failure, call_with_fallback, call_with_retry_and_fallback
    print("✓ safety.retry_on_failure, call_with_fallback, call_with_retry_and_fallback")
except ImportError as e:
    print(f"✗ safety: {e}")
    all_good = False

try:
    from logger import get_logger, Logger
    print("✓ logger.get_logger, Logger")
except ImportError as e:
    print(f"✗ logger: {e}")
    all_good = False

print("\n" + "=" * 70)
print("Checking core features...")
print("=" * 70)

# Test prompt formatting
print("\n→ Prompt formatting:")
try:
    prompt = format_prompt("qa", question="Test question?")
    print(f"  ✓ format_prompt works: {len(prompt)} chars generated")
except Exception as e:
    print(f"  ✗ format_prompt failed: {e}")
    all_good = False

# Test parser
print("\n→ Output parsing:")
try:
    result = parse_json('{"name": "Alice"}', required_keys=["name"])
    if result.success:
        print(f"  ✓ JSON parsing works: {result.data}")
    else:
        print(f"  ✗ JSON parsing failed: {result.error}")
        all_good = False
except Exception as e:
    print(f"  ✗ parse_json failed: {e}")
    all_good = False

# Test validation with failed case
print("\n→ Validation (failure detection):")
try:
    result = parse_json('{"name": "Alice"}', required_keys=["name", "age"])
    if not result.success:
        print(f"  ✓ Detects invalid schema: {result.error}")
        print(f"    Validation trace: {len(result.validation_steps)} steps")
    else:
        print(f"  ✗ Should have failed but succeeded")
        all_good = False
except Exception as e:
    print(f"  ✗ Validation failed: {e}")
    all_good = False

# Test logger
print("\n→ Logging:")
try:
    logger = get_logger(enabled=False)  # Disable output for testing
    logger.info("test")
    print(f"  ✓ Logger instantiation works")
except Exception as e:
    print(f"  ✗ Logger failed: {e}")
    all_good = False

print("\n" + "=" * 70)

if all_good:
    print("✅ All checks passed!\n")
    print("Next step: Run experiments")
    print("  cd llm_module")
    print("  export GEMINI_API_KEY='your-key-here'")
    print("  python experiments.py")
    sys.exit(0)
else:
    print("❌ Some checks failed!")
    sys.exit(1)
