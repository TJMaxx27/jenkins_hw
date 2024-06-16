import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from header_section import HeaderSection
from conftest import allure_attach_screenshot_on_failed
import random
import logging


class HomePage:
    def __init__(self, browser):
        self.browser = browser
        self.header = HeaderSection(browser)
        self.logger = logging.getLogger(__name__)

    @allure_attach_screenshot_on_failed
    @allure.step("Загрузка главной страницы")
    def load(self):
        self.logger.info("Загрузка главной страницы")
        self.browser.get("http://192.168.1.6:8081/")

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения логотипа")
    def is_logo_displayed(self):
        self.logger.info("Проверка отображения логотипа")
        return self._is_element_displayed(
            By.CSS_SELECTOR,
            'img[src="http://192.168.1.6:8081/image/catalog/opencart-logo.png"]',
        )

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения поля поиска")
    def is_search_field_displayed(self):
        self.logger.info("Проверка отображения поля поиска")
        return self._is_element_displayed(By.ID, "search")

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения корзины")
    def is_cart_displayed(self):
        self.logger.info("Проверка отображения корзины")
        return self._is_element_displayed(By.ID, "header-cart")

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения карусели")
    def is_carousel_displayed(self):
        self.logger.info("Проверка отображения карусели")
        return self._is_element_displayed(By.ID, "carousel-banner-0")

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения изображения MacBook")
    def is_macbook_image_displayed(self):
        self.logger.info("Проверка отображения изображения MacBook")
        return self._is_element_displayed(
            By.CSS_SELECTOR,
            'img[src="http://192.168.1.6:8081/image/cache/catalog/demo/banners/MacBookAir-1140x380.jpg"]',
        )

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения изображения iPhone")
    def is_iphone_image_displayed(self):
        self.logger.info("Проверка отображения изображения iPhone")
        return self._is_element_displayed(
            By.CSS_SELECTOR,
            'img[src="http://192.168.1.6:8081/image/cache/catalog/demo/banners/iPhone6-1140x380.jpg"]',
        )

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения ссылки выхода из аккаунта")
    def is_logout_displayed(self):
        self.logger.info("Проверка отображения ссылки выхода из аккаунта")
        return self._is_element_displayed(
            By.XPATH,
            'a.list-group-item[href^="http://192.168.1.6:8081/en-gb?route=account/logout"]',
        )

    @allure_attach_screenshot_on_failed
    @allure.step("Добавление случайного товара в корзину")
    def add_random_product_to_cart(self):
        self.logger.info("Добавление случайного товара в корзину")
        xpath_list = [
            '//*[@id="content"]/div[2]/div[2]/div/div[2]/form/div/button[1]',
            '//*[@id="content"]/div[2]/div[1]/div/div[2]/form/div/button[1]',
        ]

        random_xpath = random.choice(xpath_list)

        add_to_cart_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, random_xpath))
        )

        self.browser.execute_script(
            "arguments[0].scrollIntoView(true);", add_to_cart_button
        )

        while True:
            try:
                add_to_cart_button.click()
                break
            except ElementClickInterceptedException:
                add_to_cart_button = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, random_xpath))
                )

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка, что товар добавлен в корзину")
    def is_product_added_to_cart(self):
        self.logger.info("Проверка, что товар добавлен в корзину")
        return WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "#header-cart .dropdown-toggle"), "1 item(s)"
            )
        )

    @allure_attach_screenshot_on_failed
    @allure.step("Получение цен товаров")
    def get_product_prices(self):
        self.logger.info("Получение цен товаров")
        return [
            price.text
            for price in self.browser.find_elements(By.CSS_SELECTOR, ".price-new")
        ]

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
