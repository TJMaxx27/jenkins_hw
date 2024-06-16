import allure
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import allure_attach_screenshot_on_failed

class CatalogLaptopsPage:
    def __init__(self, browser):
        self.browser = browser
        self.logger = logging.getLogger(__name__)

    @allure_attach_screenshot_on_failed
    @allure.step("Загрузка каталога")
    def load(self):
        self.logger.info("Загрузка каталога")
        self.browser.get("http://192.168.1.6:8081/")
        laptops_and_notebooks = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//a[contains(text(), 'Laptops & Notebooks')]")
            )
        )
        laptops_and_notebooks.click()
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//a[contains(text(), 'Show All Laptops & Notebooks')]")
            )
        ).click()

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения раздела 'Laptops & Notebooks'")
    def is_laptops_notebooks_displayed(self):
        return self._is_element_displayed(
            By.XPATH, '//h2[text()="Laptops & Notebooks"]'
        )

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения списка продуктов")
    def is_product_list_displayed(self):
        return self._is_element_displayed(By.ID, "product-list")

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения изображений продуктов")
    def is_product_image_displayed(self):
        products = self.browser.find_elements(
            By.CSS_SELECTOR, "#product-list .product-thumb"
        )
        for product in products:
            image = product.find_element(By.CSS_SELECTOR, 'img[src$=".jpg"]')
            if not image.is_displayed():
                return False
        return True

    @allure_attach_screenshot_on_failed
    @allure.step("Клик на кнопку 'List View'")
    def click_list_view(self):
        self.logger.info("Клик листа просмотра")
        wait = WebDriverWait(self.browser, 10)
        wait.until(EC.visibility_of_element_located((By.ID, "button-list"))).click()

    @allure_attach_screenshot_on_failed
    @allure.step("Проверка отображения списка продуктов в режиме 'List View'")
    def is_product_list_view(self):
        element = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.ID, "product-list"))
        )
        return element.get_attribute("class") == "row row-cols-1 product-list"

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
