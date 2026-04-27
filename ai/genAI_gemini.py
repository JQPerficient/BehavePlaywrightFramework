import os
from google import genai


def generate_scenarios_asserts(test_description: str):
    """
    :param test_description:
    :return:
    """
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = f"""
    Based on this test scenario:
    {test_description}

    Generate appropriate tests outcomes
    Return ONLY scenarios and assertions in plain English, no code.
    """

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text


def validate_text_with_llm(captured_text: str, expected_intent: str) -> dict:
    """
    Uses LLM to semantically validate UI text intent.
    :param captured_text: Text extracted from the UI
    :param expected_intent: Human intent (e.g. 'Homepage welcome message')
    :return: dict with pass/fail and reason
    """
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = f"""
    You are a senior QA Automation engineer.

    You are validating UI text using semantic understanding.

    UI TEXT:
    \"\"\"
    {captured_text}
    \"\"\"

    EXPECTED MEANING:
    \"\"\"
    {expected_intent}
    \"\"\"

    Task:
    Determine whether the UI text fulfills the expected meaning.

    Rules:
    - Focus on intent, not exact wording
    - Allow different phrasing, synonyms, or tone
    - Ignore branding or decorative text

    Return the result STRICTLY in this format:

    RESULT: PASS or FAIL
    REASON: one short sentence
    """

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    raw_text = response.text.strip()

    # Simple parsing (robusto para CI)
    result = {
        "status": "FAIL",
        "reason": raw_text
    }

    if "RESULT: PASS" in raw_text:
        result["status"] = "PASS"

    if "REASON:" in raw_text:
        result["reason"] = raw_text.split("REASON:")[-1].strip()

    return result


def suggest_alternative_locators(
    failed_locator: str,
    action: str,
    error_message: str,
    element_intent: str
) -> str:
    """
    :param failed_locator:
    :param action:
    :param error_message:
    :param element_intent:
    :return:
    """
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = f"""
    You are a Senior QA Automation engineer specialized in self-healing test automation.

    A test step failed due to a selector issue.

    FAILED LOCATOR:
    {failed_locator}

    INTENDED ACTION:
    {action}

    ELEMENT INTENT:
    {element_intent}

    ERROR MESSAGE:
    {error_message}

    Task:
    Suggest 2 to 3 alternative robust selectors for the same element.

    Additionally:
    - Assign a confidence score between 0 and 100 to each selector
    - Higher score means more stable and reliable in test automation

    Scoring guidelines:
    - Prefer semantic selectors (role, aria): +20
    - Prefer relative selectors over absolute XPaths
    - Prefer selectors resilient to layout changes
    - Avoid brittle text-only selectors

    Return STRICTLY in this format:

    *** SUGGESTED_ALTERNATIVE_SELECTORS | SELECTOR_SCORES ***
    1. <selector> | score: <number>
    2. <selector> | score: <number>
    3. <selector> | score: <number>
    """

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text.strip()



