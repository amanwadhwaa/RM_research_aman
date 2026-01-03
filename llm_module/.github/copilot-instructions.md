DEPRECATED

This file was removed. See the repository README.md for contributor instructions.

## Architecture & Key Components

### Main Pattern
- **File**: `roboLLM.py`
- **Core Design**: Interactive REPL (Read-Eval-Print Loop) that processes user input and generates responses using the Gemini 2.5 Flash model
- **Data Flow**: User input → Gemini API call → Response display → Loop

### Key Dependencies
- **google.generativeai**: Google's official SDK for Gemini models
- **Environment Configuration**: Requires `GEMINI_API_KEY` environment variable

## Critical Configuration

### API Setup
The project uses environment-based configuration:
```python
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
```

**Important**: The API key is sourced from `GEMINI_API_KEY` environment variable. When extending this project, maintain this pattern for API credentials.

## Development Workflows

### Running the Application
```bash
python roboLLM.py
```

### Exit Behavior
- Type `exit` to gracefully terminate the chat session
- Application prints goodbye message before exit

## Project Patterns & Conventions

### Input/Output Format
- Prompts are prefixed with `"You: "` and `"LLM: "`
- All responses from Gemini are accessed via `.text` attribute
- User input is case-insensitive for exit command (`.lower()` check)

### Error Handling
- Currently minimal error handling; API errors will surface as exceptions
- When enhancing, consider wrapping `generate_content()` calls in try-except blocks

## Common Extensions & Next Steps

When expanding this codebase:
1. **Multi-turn Conversation**: Maintain conversation history as list of dicts with "role" and "content" keys
2. **Model Configuration**: Parameters like `temperature`, `top_p`, `max_tokens` should be externalized to environment variables or config file
3. **Input Validation**: Add checks for empty input before API calls
4. **Logging**: Use Python's `logging` module rather than print statements for production readiness

## Integration Points

- **Gemini API**: Endpoint is implicit in the `genai.GenerativeModel()` call
- **Standard Input/Output**: Uses `input()` for user prompts and `print()` for output
- **Environment**: Depends on shell environment variable `GEMINI_API_KEY`

---
*Last updated: January 2026*
