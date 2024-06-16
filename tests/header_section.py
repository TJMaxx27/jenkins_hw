from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import allure
from conftest import allure_attach_screenshot_on_failed

class HeaderSection:
    def __init__(self, browser):
        self.browser = browser
        self.logger = logging.getLogger(__name__)

    @allure_attach_screenshot_on_failed
    @allure.step("Клик по кнопке My Account")
    def click_my_account(self):
        self.logger.info("Клик по кнопке My Account")
        my_account = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//span[text()="My Account"]'))
        )
        my_account.click()

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения ссылки на регистрацию")
    def is_register_displayed(self):
        self.logger.info("Проверка отображения ссылки на регистрацию")
        register = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[text()="Register"]'))
        )
        return register

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения ссылки на вход")
    def is_login_displayed(self):
        self.logger.info("Проверка отображения ссылки на вход")
        login = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[text()="Login"]'))
        )
        return login

    @allure_attach_screenshot_on_failed
    @allure.step("Смена валюты")
    def change_currency(self, currency_name):
        self.logger.info(f"Смена валюты на {currency_name}")
        currency_dropdown = self.browser.find_element(
            By.XPATH, "//nav/div/div[1]/ul/li[1]/form/div/a/span"
        )
        currency_dropdown.click()

        currency_option = self.browser.find_element(
            By.XPATH, f'//a[@href="{currency_name}"]'
        )
        currency_option.click()

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка смены валюты")
    def is_currency_changed(self, expected_currency):
        self.logger.info(f"Проверка смены валюты на {expected_currency}")
        actual_currency = self.browser.find_element(
            By.XPATH, "//nav/div/div[1]/ul/li[1]/form/div/a/span"
        ).text
        return actual_currency == expected_currency
