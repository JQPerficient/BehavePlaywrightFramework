from ai.genAI_gemini import (
    generate_scenarios_asserts,
    validate_text_with_llm,
    suggest_alternative_locators
)

TOOLS = [
    {
        "name": "suggest_alternative_locators",
        "description": "Suggest alternative selectors when a locator fails",
        "parameters": {
            "type": "object",
            "properties": {
                "failed_locator": {"type": "string"},
                "action": {"type": "string"},
                "error_message": {"type": "string"},
                "element_intent": {"type": "string"}
            },
            "required": [
                "failed_locator",
                "action",
                "error_message",
                "element_intent"
            ]
        },
        "function": suggest_alternative_locators
    }
]
