from behave import *
from Utilities import configReader
from features.pageobjects.RegistrationPage import RegistrationPage

import os.path
import os
from Utilities.image_compare import compare_images


@given(u'I navigate to Selenium Website')
def step_impl(context):
    context.reg = RegistrationPage(
        context.page,
        context.scenario_logger
    )
    context.reg.open(
        configReader.readConfig("urls", "seleniumUrl")
    )


@when(u'I capture the actual image')
def step_impl(context):
    context.actual_image_path = "visual_actual/homepage.png"
    context.page.screenshot(path=context.actual_image_path)


@then(u'I verify the image should match with the baseline')
def step_impl(context):
    baseline = "visual_baseline/homepage.png"
    actual = context.actual_image_path
    diff = "visual_diff/homepage_diff.png"

    # 🔹 Asegurar folders
    os.makedirs("visual_baseline", exist_ok=True)
    os.makedirs("visual_diff", exist_ok=True)

    # ✅ 1️⃣ Primera ejecución → crear baseline
    if not os.path.exists(baseline):
        os.replace(actual, baseline )
        print("✅ Baseline creado automáticamente")
        return

    # ✅ 2️⃣ Comparación normal
    result, diff_path = compare_images(baseline, actual, diff)
    assert result, f"❌ Diferencias visuales encontradas. Revisa: {diff_path}"

