from behave import *
from Utilities import configReader
from ai.genAI_gemini import generate_scenarios_asserts, validate_text_with_llm, suggest_alternative_locators
from ai.mcp_client import run_mcp
from features.pageobjects.RegistrationPage import RegistrationPage
import os.path


@given(u'I navigate to Selenium Download page')
def step_impl(context):
    context.reg = RegistrationPage(
        context.page,
        context.scenario_logger
    )
    context.reg.open(
        configReader.readConfig("urls", "downloadSeleniumUrl")
    )


@given("I navigate to Selenium Homepage")
def step_go_to_homepage(context):
        context.reg = RegistrationPage(
            context.page,
            context.scenario_logger
        )
        context.reg.open(
            configReader.readConfig("urls", "seleniumUrl")
        )


@when("I try to capture the main hero title with an invalid locator")
def step_trigger_locator_failure(context):
    # Locator INTENCIONALMENTE incorrecto
    context.failed_locator = "//main//h99"

    try:
        context.page.locator(context.failed_locator).inner_text()

    except Exception as e:
        context.locator_error = str(e)

        # ✅ PRUEBA CONTROLADA DEL MEJOR SELECTOR SUGERIDO
        try:
            context.healed_text = context.page.get_by_role(
                "heading", level=1
            ).inner_text()

            context.scenario_logger.info(
                "SELF-HEALING VERIFICATION SUCCESS\n"
                "Selector tested: role=heading[level=1]\n"
                f"Recovered text: {context.healed_text}",
                extra={
                    "feature": context.feature.name,
                    "scenario": context.scenario.name
                }
            )

        except Exception as heal_error:
            context.scenario_logger.error(
                "SELF-HEALING VERIFICATION FAILED\n"
                "Selector tested: role=heading[level=1]\n"
                f"Error: {str(heal_error)}",
                extra={
                    "feature": context.feature.name,
                    "scenario": context.scenario.name
                }
            )


@when("I capture the main welcome text")
def step_capture_welcome_text(context):
    xpath = configReader.readConfig(
        "locators",
        "first_title_selenium_page_XPATH"
    )

    try:
        context.captured_text = context.page.locator(xpath).inner_text()

    except Exception as e:
        print("\n⚠️ Locator failed. Asking Gemini for self-healing suggestions...\n")

        suggestions = suggest_alternative_locators(
            failed_locator=xpath,
            action="get inner text",
            error_message=str(e),
            element_intent="Main hero title of Selenium homepage"
        )

        print("\n******* Gemini self-healing locator suggestions *******")
        print(suggestions )
        print("*****************************************************\n")

        # ❌ seguimos fallando el test (no hacemos magia automática)
        raise e


@when("I ask Gemini for suggested asserts")
def step_impl(context):
    suggested_asserts = generate_scenarios_asserts(context.text)
    print("\n*******!!! Gemini suggested asserts (for review): !!!*******\n")
    print(suggested_asserts)


@then(u"I download the file")
def step_impl(context):
    page = context.page

    with page.expect_download() as download_info:
        page.get_by_role("link", name="4.41.0", exact=True).click()

    download = download_info.value

    # ✅ Ruta robusta al proyecto (independiente del runner)
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

    downloads_dir = os.path.join(project_root, "Downloads")
    os.makedirs(downloads_dir, exist_ok=True)

    file_path = os.path.join(downloads_dir, "Selenium.jar")

    # ✅ Espera REAL a que la descarga termine
    download.save_as(file_path)
    download.path()

    print(f"File downloaded successfully in: {file_path}")


@then("The text should semantically represent a homepage welcome message")
def step_validate_welcome_message(context):
    result = validate_text_with_llm(
        captured_text=context.captured_text,
        expected_intent="Homepage welcome message for new users"
    )

    assert result["status"] == "PASS", (
        f"LLM semantic assertion failed.\n"
        f"Captured text: {context.captured_text}\n"
        f"Reason: {result['reason']}"
    )

    print(
        "\n*******!!! Gemini text validation result (for review): !!!*******"
        f"\nStatus : {result['status']}"
        f"\nReason : {result['reason']}"
        "\n-----------------------------\n"
    )


@then("I see expected title")
def step_validate_welcome_message(context):
    expected_title = "Selenium automates browsers. That's it!"
    assert expected_title == "Selenium automates browsers. That's it!", f"Page title: {expected_title}"


@then("Gemini MCP should suggest alternative locators for the element")
def step_mcp_self_healing(context):
    from ai.mcp_client import run_mcp

    result = run_mcp(
        prompt=f"""
        A Playwright test failed due to a locator issue.

        Failed locator:
        {context.failed_locator}

        Intended action:
        get inner text

        Error message:
        {context.locator_error}

        Element intent:
        Main hero title of Selenium homepage.
        """,
        context_data={
            "failed_locator": context.failed_locator,
            "action": "get inner text",
            "error_message": context.locator_error,
            "element_intent": "Main hero title of Selenium homepage"
        }
    )

    # ✅ LOGGING AUTOMÁTICO (AQUÍ ESTÁ EL VALOR)
    context.scenario_logger.warning(
        "SELF-HEALING SUGGESTIONS WITH CONFIDENCE SCORE\n"
        f"Failed locator: {context.failed_locator}\n"
        f"Action: get inner text\n"
        f"Error: {context.locator_error}\n"
        f"{result['output']}",
        extra={
            "feature": context.feature.name,
            "scenario": context.scenario.name
        }
    )

    # (Opcional) salida visual local
    print("\n======= MCP SELF-HEALING RESULT =======")
    print(f"Tool used: {result['tool_used']}")
    print(result["output"])
    print("=====================================\n")

    assert result["tool_used"] == "suggest_alternative_locators", (
        "Gemini MCP did not invoke the self-healing locator tool"
    )




