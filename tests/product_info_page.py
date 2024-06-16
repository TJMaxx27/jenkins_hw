import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from conftest import allure_attach_screenshot_on_failed


class ProductInfoPage:
    def __init__(self, browser):
        self.browser = browser
        self.logger = logging.getLogger(__name__)

    @allure_attach_screenshot_on_failed
    @allure.step("Загрузка страницы информации о продукте")
    def load(self):
        self.logger.info("Загрузка страницы информации о продукте")
        self.browser.get("http://192.168.1.6:8081/en-gb/catalog/laptop-notebook")

    @allure_attach_screenshot_on_failed
    @allure.step("Клик по продукту HP LP3065")
    def click_hp_lp3065(self):
        self.logger.info("Клик по продукту HP LP3065")
        card_hp_lp3065 = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//a[contains(text(), 'HP LP3065')]")
            )
        )
        card_hp_lp3065.click()

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка URL для продукта HP LP3065")
    def is_hp_lp3065_url(self):
        self.logger.info("Проверка URL для продукта HP LP3065")
        return (
            self.browser.current_url
            == "http://192.168.1.6:8081/en-gb/product/laptop-notebook/hp-lp3065"
        )

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения изображения продукта")
    def is_product_image_displayed(self):
        self.logger.info("Проверка отображения изображения продукта")
        return self._is_element_displayed(
            By.CSS_SELECTOR,
            'img[src="http://192.168.1.6:8081/image/cache/catalog/demo/hp_1-500x500.jpg"]',
        )

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения цены продукта")
    def is_price_displayed(self):
        self.logger.info("Проверка отображения цены продукта")
        return self._is_element_displayed(By.CSS_SELECTOR, "span.price-new")

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения календаря")
    def is_calendar_displayed(self):
        self.logger.info("Проверка отображения календаря")
        return self._is_element_displayed(
            By.CSS_SELECTOR,
            ".daterangepicker.ltr.auto-apply.single.opensright.show-calendar",
        )

    @allure_attach_screenshot_on_failed
    @allure.step('Проверка отображения кнопки "Добавить в корзину"')
    def is_add_to_cart_displayed(self):
        self.logger.info("Проверка отображения кнопки 'Добавить в корзину'")
        return self._is_element_displayed(By.XPATH, '//*[@id="button-cart"]')

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
