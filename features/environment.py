from playwright.sync_api import sync_playwright
import allure
from allure_commons.types import AttachmentType
from Utilities import configReader
from Utilities.logUtil import Logger
import time
import os


def before_all(context):
    """
    :param context:
    """
    context.playwright = sync_playwright().start()

    run_id = time.strftime("%Y%m%d_%H%M%S")
    context.run_id = run_id
    context.log_file_path = f"Logs/run_{run_id}.log"

    Logger(log_file_path=context.log_file_path)

    # 🔥 ESCRIBIR current_log_path.txt EN EL ROOT DEL PROYECTO
    project_root = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(project_root, ".."))

    current_log_pointer = os.path.join(project_root, "current_log_path.txt")

    with open(current_log_pointer, "w", encoding="utf-8") as f:
        f.write(context.log_file_path)


def before_scenario(context, scenario):
    """
    Se ejecuta antes de cada Scenario
    - Inicializa UI SIEMPRE (como ya funcionaba)
    - Inicializa API SOLO si el scenario/feature tiene tag @API
    """

    # Crear API request context por escenario
    context.api_request = context.playwright.request.new_context()

    # ============================================================
    # 🔥 1. CREAR LOGGER POR SCENARIO (lo nuevo que necesitabas)
    # ============================================================
    import logging

    base_logger = logging.getLogger()   # logger raíz
    context.scenario_logger = logging.LoggerAdapter(
        base_logger,
        {
            "scenario": scenario.name,
            "feature": scenario.feature.name
        }
    )

    # ============================================================
    # 🔥 2. IMPRIMIR MARCADORES DE INICIO DE SCENARIO (opcional pero útil)
    # ============================================================
    context.scenario_logger.info("=" * 70)
    context.scenario_logger.info(f"FEATURE       : {scenario.feature.name}")
    context.scenario_logger.info(f"START SCENARIO: {scenario.name}")
    context.scenario_logger.info("=" * 70)

    # ============================================================
    # 🔥 3. TU UI SETUP (no se tocó nada aquí)
    # ============================================================
    browser_type = configReader.readConfig(
        "browser", "browser"
    ).lower()

    if browser_type == "chrome":
        context.browser = context.playwright.chromium.launch(
            headless=False,
            channel="chrome"
            #slow_mo=500
        )
    elif browser_type == "edge":
        context.browser = context.playwright.chromium.launch(
            headless=False,
            channel="msedge"
        )
    elif browser_type == "firefox":
        context.browser = context.playwright.firefox.launch(
            headless=False
        )
    elif browser_type == "safari":
        context.browser = context.playwright.webkit.launch(
            headless=False
        )
    else:
        raise Exception(f"Unsupported browser: {browser_type}")

    context.page = context.browser.new_page()


def after_step(context, step):
    """
    Screenshot solo si es UI y el step falla
    """
    if step.status == "failed" and hasattr(context, "page"):
        screenshot = context.page.screenshot()
        allure.attach(
            screenshot,
            name="UI Screenshot",
            attachment_type=AttachmentType.PNG
        )


def after_scenario(context, scenario):
    """
    Cleanup por escenario + logging de cierre del Scenario
    """

    status = scenario.status.name.upper()
    duration = f"{scenario.duration:.2f}s"

    context.scenario_logger.info("=" * 70)
    context.scenario_logger.info(
        f"END SCENARIO  : {scenario.name}"
    )

    # 🔥 Nivel de log correcto según el resultado
    if scenario.status.name == "passed":
        context.scenario_logger.info(
            f"STATUS        : {status}"
        )
    elif scenario.status.name in ("failed", "error"):
        context.scenario_logger.error(
            f"STATUS        : {status}"
        )
    else:
        context.scenario_logger.warning(
            f"STATUS        : {status}"
        )

    context.scenario_logger.info(
        f"DURATION      : {duration}"
    )
    context.scenario_logger.info("=" * 70)

    # =========================
    # ✅ CLEANUP (NO SE TOCA)
    # =========================
    if hasattr(context, "page"):
        context.page.close()

    if hasattr(context, "context"):
        context.context.close()

    if hasattr(context, "browser"):
        context.browser.close()

    # Liberar API request context
    if hasattr(context, "api_request"):
        context.api_request.dispose()


def after_all(context):
    """
    Cleanup global
    """
    if hasattr(context, "playwright"):
        context.playwright.stop()