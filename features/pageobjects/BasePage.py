from Utilities import configReader
import allure


class BasePage:

    def __init__(self, page, logger):
        """
        page   : playwright page
        logger : LoggerAdapter inyectado por scenario
        """
        self.page = page
        self.logger = logger

    # ----------- BASIC ACTIONS -----------

    def click(self, locator):
        with allure.step(f"Clicking on an Element {locator}"):
            self.page.locator(
                configReader.readConfig("locators", locator)
            ).click()
            self.logger.info(f"Clicked on Element {locator}")

    def click_when_ready(self, locator, timeout=5000):
        with allure.step(f"Clicking when Element {locator} is ready"):
            element = self.page.locator(
                configReader.readConfig("locators", locator)
            )
            element.wait_for(state="visible", timeout=timeout)
            element.click()
            self.logger.info(f"Clicked on Element {locator} when ready")

    def double_click(self, locator):
        with allure.step(f"Double clicking on Element {locator}"):
            self.page.locator(
                configReader.readConfig("locators", locator)
            ).dblclick()
            self.logger.info(f"Double clicked on Element {locator}")

    def type(self, locator, value):
        with allure.step(f"Typing '{value}' in Element {locator}"):
            self.page.locator(
                configReader.readConfig("locators", locator)
            ).fill(value)
            self.logger.info(
                f"Typed '{value}' in Element {locator}"
            )

    def press_key(self, locator, key):
        with allure.step(f"Pressing key '{key}' on Element {locator}"):
            self.page.locator(
                configReader.readConfig("locators", locator)
            ).press(key)
            self.logger.info(
                f"Pressed key '{key}' on Element {locator}"
            )

    def move_to(self, locator):
        with allure.step(f"Moving to Element {locator}"):
            self.page.locator(
                configReader.readConfig("locators", locator)
            ).hover()
            self.logger.info(f"Moved to Element {locator}")

    def select(self, locator, value):
        with allure.step(
            f"Selecting value '{value}' from Element {locator}"
        ):
            self.page.select_option(
                configReader.readConfig("locators", locator),
                value
            )
            self.logger.info(
                f"Selected value '{value}' from Element {locator}"
            )

    def scroll_into_view(self, locator):
        with allure.step(f"Scrolling to Element {locator}"):
            self.page.locator(
                configReader.readConfig("locators", locator)
            ).scroll_into_view_if_needed()
            self.logger.info(f"Scrolled to Element {locator}")

    # ----------- NAVIGATION -----------

    def navigate_to(self, url):
        with allure.step(f"Navigating to {url}"):
            self.page.goto(url, timeout=60000)
            self.logger.info(f"Navigated to {url}")

    def wait_for_url(self, url_pattern, timeout=5000):
        with allure.step(f"Waiting for URL to match '{url_pattern}'"):
            self.page.wait_for_url(url_pattern, timeout=timeout)
            self.logger.info(f"URL matched '{url_pattern}'")

    # ----------- GETTERS -----------

    def get_value(self, locator):
        with allure.step(f"Getting value from input {locator}"):
            real_locator = configReader.readConfig("locators", locator)
            self.logger.info(
                f"Resolved locator [{locator}] -> [{real_locator}]"
            )

            element = self.page.locator(real_locator)
            element.wait_for(state="visible", timeout=5000)

            value = element.input_value()
            self.logger.info(
                f"Captured value from input [{locator}] -> [{value}]"
            )

            return value

    def get_text(self, locator):
        with allure.step(f"Getting text from Element {locator}"):
            real_locator = configReader.readConfig("locators", locator)
            self.logger.info(
                f"Resolved locator [{locator}] -> [{real_locator}]"
            )

            element = self.page.locator(real_locator)
            element.wait_for(state="visible", timeout=5000)

            text = element.inner_text()
            self.logger.info(
                f"Captured text from Element [{locator}] -> [{text}]"
            )

            return text

    def get_attribute(self, locator, attribute):
        with allure.step(
            f"Getting attribute '{attribute}' from Element {locator}"
        ):
            value = self.page.locator(
                configReader.readConfig("locators", locator)
            ).get_attribute(attribute)
            self.logger.info(
                f"Captured attribute '{attribute}' from Element {locator} -> {value}"
            )
            return value

    def get_elements_count(self, locator):
        with allure.step(f"Counting Elements {locator}"):
            count = self.page.locator(
                configReader.readConfig("locators", locator)
            ).count()
            self.logger.info(
                f"Element count for {locator} -> {count}"
            )
            return count

    def get_title(self):
        with allure.step("Getting page title"):
            title = self.page.title()
            self.logger.info(f"Page title -> {title}")
            return title

    def get_current_url(self):
        with allure.step("Getting current URL"):
            url = self.page.url
            self.logger.info(f"Current URL -> {url}")
            return url

    # ----------- WAITS & STATES -----------

    def is_visible(self, locator, timeout=5000):
        with allure.step(f"Checking if Element {locator} is visible"):
            element = self.page.locator(
                configReader.readConfig("locators", locator)
            )
            element.wait_for(state="visible", timeout=timeout)
            visible = element.is_visible()
            self.logger.info(
                f"Element {locator} visibility -> {visible}"
            )
            return visible

    def is_enabled(self, locator):
        enabled = self.page.locator(
            configReader.readConfig("locators", locator)
        ).is_enabled()
        self.logger.info(f"Element {locator} enabled -> {enabled}")
        return enabled

    def is_disabled(self, locator):
        disabled = not self.is_enabled(locator)
        self.logger.info(f"Element {locator} disabled -> {disabled}")
        return disabled

    def is_checked(self, locator):
        checked = self.page.locator(
            configReader.readConfig("locators", locator)
        ).is_checked()
        self.logger.info(f"Element {locator} checked -> {checked}")
        return checked

    def wait_until_hidden(self, locator, timeout=5000):
        with allure.step(f"Waiting for Element {locator} to disappear"):
            self.page.locator(
                configReader.readConfig("locators", locator)
            ).wait_for(state="hidden", timeout=timeout)
            self.logger.info(
                f"Element {locator} is now hidden"
            )