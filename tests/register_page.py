import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from conftest import allure_attach_screenshot_on_failed

class RegisterPage:
    def __init__(self, browser):
        self.browser = browser
        self.logger = logging.getLogger(__name__)

    @allure_attach_screenshot_on_failed
    @allure.step("Загрузка страницы регистрации")
    def load(self):
        self.logger.info("Загрузка страницы регистрации")
        self.browser.get("http://192.168.1.6:8081/index.php?route=account/register")

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения поля имени")
    def is_name_field_displayed(self):
        self.logger.info("Проверка отображения поля имени")
        return self._is_element_displayed(By.ID, "input-firstname")

    @allure_attach_screenshot_on_failed
    @allure.step("Ввод имени")
    def enter_name(self, name):
        self.logger.info("Ввод имени")
        name_field = self.browser.find_element(By.ID, "input-firstname")
        name_field.clear()
        name_field.send_keys(name)

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения поля фамилии")
    def is_last_name_field_displayed(self):
        self.logger.info("Проверка отображения поля фамилии")
        return self._is_element_displayed(By.ID, "input-lastname")

    @allure_attach_screenshot_on_failed
    @allure.step("Ввод фамилии")
    def enter_last_name(self, last_name):
        self.logger.info("Ввод фамилии")
        last_name_field = self.browser.find_element(By.ID, "input-lastname")
        last_name_field.clear()
        last_name_field.send_keys(last_name)

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения поля электронной почты")
    def is_email_field_displayed(self):
        self.logger.info("Проверка отображения поля электронной почты")
        return self._is_element_displayed(By.ID, "input-email")

    @allure_attach_screenshot_on_failed
    @allure.step("Ввод адреса электронной почты")
    def enter_email(self, email):
        self.logger.info("Ввод адреса электронной почты")
        email_field = self.browser.find_element(By.ID, "input-email")
        email_field.clear()
        email_field.send_keys(email)

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения поля пароля")
    def is_password_field_displayed(self):
        self.logger.info("Проверка отображения поля пароля")
        return self._is_element_displayed(By.ID, "input-password")

    @allure_attach_screenshot_on_failed
    @allure.step("Ввод пароля")
    def enter_password(self, password):
        self.logger.info("Ввод пароля")
        password_field = self.browser.find_element(By.ID, "input-password")
        password_field.clear()
        password_field.send_keys(password)

    @allure_attach_screenshot_on_failed
    @allure.step("Подтверждение согласия с политикой конфиденциальности")
    def privacy_policy_checkbox_agree(self):
        self.logger.info("Подтверждение согласия с политикой конфиденциальности")
        return self.browser.find_element(
            By.CSS_SELECTOR, 'input[name="agree"][value="1"]'
        )

    @allure_attach_screenshot_on_failed
    @allure.step('Проверка отображения кнопки "Продолжить"')
    def is_continue_button_displayed(self):
        self.logger.info("Проверка отображения кнопки 'Продолжить'")
        return self._is_element_displayed(By.CLASS_NAME, "btn-primary")

    @allure_attach_screenshot_on_failed
    @allure.step('Клик по кнопке "Продолжить"')
    def continue_button(self):
        self.logger.info("Клик по кнопке 'Продолжить'")
        return self.browser.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")

    def _is_element_displayed(self, by, value):
        try:
            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except:
            allure.attach(self.browser.get_screenshot_as_png(), name="element_not_displayed",
                          attachment_type=allure.attachment_type.PNG)
            return False
