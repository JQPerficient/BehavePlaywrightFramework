from google import genai
from ai.genAI_gemini import suggest_alternative_locators
import os


def mcp_decide_tool(prompt: str) -> str:
    """
    :param prompt:
    :return:
    """
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    decision_prompt = f"""
    You are an automation AI router.

    Based on the following situation, decide which action is needed.

    Available tools:
    - suggest_alternative_locators
    - none

    Situation:
    {prompt}

    Return ONLY the tool name.
    """

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=decision_prompt
    )

    return response.text.strip()


def run_mcp(prompt: str, context_data: dict) -> dict:
    """
    MCP emulado para Gemini Python:
    1. LLM decide la tool
    2. Python ejecuta la función
    """

    decision = mcp_decide_tool(prompt)

    if decision == "suggest_alternative_locators":
        output = suggest_alternative_locators(
            failed_locator=context_data["failed_locator"],
            action=context_data["action"],
            error_message=context_data["error_message"],
            element_intent=context_data["element_intent"]
        )

        return {
            "tool_used": "suggest_alternative_locators",
            "output": output
        }

    return {
        "tool_used": "none",
        "output": "No MCP action required"
    }