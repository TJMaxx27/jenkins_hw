import allure
import logging
from selenium.webdriver.common.by import By
from header_section import HeaderSection
from conftest import allure_attach_screenshot_on_failed

class DesktopsPage:
    def __init__(self, browser):
        self.browser = browser
        self.header = HeaderSection(browser)
        self.logger = logging.getLogger(__name__)

    @allure_attach_screenshot_on_failed
    @allure.step("Загрузка страницы с компьютерами")
    def load(self):
        self.logger.info("Загрузка страницы с компьютерами")
        self.browser.get("http://192.168.1.6:8081/en-gb/catalog/desktops")

    @allure_attach_screenshot_on_failed
    @allure.step("Смена валюты на Польскую Крону")
    def change_currency_to_poland_sterling(self):
        self.logger.info("Смена валюты на Польскую Крону")
        currency_dropdown = self.browser.find_element(
            By.XPATH, "//nav/div/div[1]/ul/li[1]/form/div/a/span"
        )
        currency_dropdown.click()
        eur_option = self.browser.find_element(
            By.CSS_SELECTOR, ".dropdown-menu.show li:nth-child(2) a.dropdown-item"
        )
        eur_option.click()

    @allure_attach_screenshot_on_failed
    @allure.step("Получение цен продуктов")
    def get_product_prices(self):
        self.logger.info("Получение цен продуктов")
        return [
            price.text for price in self.browser.find_elements(By.ID, "product-list")
        ]
