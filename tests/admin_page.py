import allure
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import allure_attach_screenshot_on_failed


class AdminPage:
    def __init__(self, browser):
        self.browser = browser
        self.logger = logging.getLogger(__name__)

    @allure_attach_screenshot_on_failed
    @allure.step("Загрузка страницы администрирования")
    def load(self):
        self.logger.info("Загрузка страницы администрирования")
        self.browser.get("http://192.168.1.6:8081/administration/")

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения логотипа")
    def is_logo_displayed(self):
        return self._is_element_displayed(
            By.CSS_SELECTOR, 'img[src="view/image/logo.png"]'
        )

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения заголовка")
    def is_header_displayed(self):
        return self._is_element_displayed(By.CSS_SELECTOR, ".card-header")

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения поля 'Имя пользователя'")
    def is_username_field_displayed(self):
        return self._is_element_displayed(By.ID, "input-username")

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения поля 'Пароль'")
    def is_password_field_displayed(self):
        return self._is_element_displayed(By.ID, "input-password")

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения кнопки 'Войти'")
    def is_login_button_displayed(self):
        return self._is_element_displayed(By.CLASS_NAME, "btn-primary")

    @allure_attach_screenshot_on_failed
    @allure.step("Авторизация пользователя")
    def login(self, username, password):
        self.logger.info(f"Авторизация пользователя {username}")
        self.browser.find_element(By.ID, "input-username").send_keys(username)
        self.browser.find_element(By.ID, "input-password").send_keys(password)
        self.browser.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Logout"))
        )

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения страницы 'Dashboard'")
    def is_dashboard_displayed(self):
        return self._is_element_displayed(By.XPATH, "//h1[text()='Dashboard']")

    @allure_attach_screenshot_on_failed
    @allure.step("Переход на вкладку 'Продукты'")
    def go_to_catalog_and_products(self):
        self.logger.info("Переход на вкладку Продукты")
        catalog_menu = self.browser.find_element(
            By.CSS_SELECTOR, 'a.parent[href="#collapse-1"][data-bs-toggle="collapse"]'
        )
        catalog_menu.click()

        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//a[contains(@href, "catalog/product")]')
            )
        )

        products_menu = self.browser.find_element(
            By.XPATH, '//a[contains(@href, "catalog/product")]'
        )
        return products_menu

    @allure_attach_screenshot_on_failed
    @allure.step("Кнопка 'New Product'")
    def add_new_product_button(self):
        self.logger.info("Кнопка new_product")
        add_new_product_button = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "i.fa-solid.fa-plus"))
        )
        return add_new_product_button

    @allure_attach_screenshot_on_failed
    @allure.step("Добавление нового продукта")
    def add_product(self):
        self.logger.info("Добавление нового продукта")
        self.browser.find_element(By.ID, "input-name-1").send_keys("iPhoneXs_test")
        self.browser.find_element(By.ID, "input-meta-title-1").send_keys(
            "iPhoneXs_test"
        )
        self.browser.find_element(
            By.CSS_SELECTOR, 'a.nav-link[href="#tab-data"]'
        ).click()
        self.browser.find_element(By.ID, "input-model").send_keys("iPhoneXs_test")
        self.browser.find_element(
            By.CSS_SELECTOR, 'a.nav-link[aria-selected="false"][href="#tab-seo"]'
        ).click()
        self.browser.find_element(By.ID, "input-keyword-0-1").send_keys("iPhoneXS")

    @allure_attach_screenshot_on_failed
    @allure.step("Кнопка 'Save'")
    def save_button(self):
        self.logger.info("Кнопка Save")
        return self.browser.find_element(
            By.XPATH,
            "//button[@type='submit' and @form='form-product' and contains(@title, 'Save')]",
        )

    @allure_attach_screenshot_on_failed
    @allure.step("Поиск тестового продукта в списке продуктов")
    def find_test_product_in_products(self):
        return self.browser.find_element(
            By.XPATH, f"//td[contains(text(), 'iPhoneXs_test')]/.."
        )

    @allure_attach_screenshot_on_failed
    @allure.step("Выбор чекбокса тестового продукта")
    def find_checkbox_test_product(self):
        test_product_row = self.find_test_product_in_products()
        return test_product_row.find_element(
            By.CSS_SELECTOR, 'input[type="checkbox"][name="selected[]"]'
        )

    @allure_attach_screenshot_on_failed
    @allure.step("Кнопка 'Delete'")
    def delete_button(self):
        self.logger.info("Кнопка удалить")
        return self.browser.find_element(By.XPATH, "//button[@title='Delete']")

    @allure_attach_screenshot_on_failed
    @allure.step("Обработка всплывающего окна 'Успешно изменено'")
    def alert_window_success(self):
        alert = WebDriverWait(self.browser, 10).until(EC.alert_is_present())
        alert.accept()
        return alert

    @allure_attach_screenshot_on_failed
    @allure.step("Ожидание всплывающего окна 'Успешно изменено'")
    def modified_popup(self):
        modified_popup = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.alert.alert-success.alert-dismissible")
            )
        )
        return modified_popup

    @allure_attach_screenshot_on_failed
    @allure.step("Выход из аккаунта")
    def logout(self):
        self.logger.info("Логаут")
        self.browser.find_element(By.LINK_TEXT, "Logout").click()
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".card-header"))
        )

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
