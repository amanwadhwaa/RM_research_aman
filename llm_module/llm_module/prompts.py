"""Prompt templates with explicit output format requirements."""


# System instruction - what the AI should be like
SYSTEM_INSTRUCTION = """You are a helpful, clear, and concise assistant.
Answer questions directly without unnecessary explanation.
If unsure, say so.
ALWAYS follow the output format specified in the prompt."""


# Reusable prompt templates with EXPLICIT output format requirements
# Each template includes format instructions and examples
TEMPLATES = {
    "qa": """Question: {question}

Answer this clearly in 1-2 sentences. No explanations, no preamble.
Just answer the question directly.""",
    
    "json_extract": """Extract the key information from the text below and return ONLY a valid JSON object.
Do not include any text before or after the JSON.
The JSON must have exactly these keys: {required_keys}

Text: {text}

Return ONLY valid JSON (no markdown, no explanation):""",
    
    "classify": """Classify the text below as exactly one of: {categories}

Text: {text}

Return ONLY the classification word, nothing else. No explanation.""",
    
    "sentiment": """Analyze the sentiment of the text below.
Return ONLY one word: positive, neutral, or negative.
No explanation, no punctuation.

Text: {text}

Answer:""",
    
    "structured_info": """Extract information about a person from the text below.
Return ONLY a valid JSON object with exactly these fields: name, age, location
If any field is unknown, use "unknown" as the value.
Do not include any text before or after the JSON.

Text: {text}

Return ONLY valid JSON:""",
}


def get_template(name: str) -> str:
    """Get a prompt template by name."""
    if name not in TEMPLATES:
        raise ValueError(f"Unknown template: {name}. Available: {list(TEMPLATES.keys())}")
    return TEMPLATES[name]


def format_prompt(template_name: str, **kwargs) -> str:
    """
    Format a prompt template with variables.
    
    This is the KEY separation point:
    - Prompts are NOT hardcoded in application logic
    - Only template names and variables are passed around
    - Changing a prompt only requires changing TEMPLATES dict
    - Application logic doesn't care about prompt content
    
    Args:
        template_name: Name of the template to use
        **kwargs: Variables to fill in the template
        
    Returns:
        The formatted prompt string
        
    Example:
        # To change a prompt, modify TEMPLATES dict, not your code:
        prompt = format_prompt("qa", question="What is Python?")
        
        # Application doesn't need to change if we update TEMPLATES["qa"]
    """
    template = get_template(template_name)
    return template.format(**kwargs)
