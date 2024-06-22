import logging
from functools import wraps
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FireFoxOptions

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def allure_attach_screenshot_on_failed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            allure.attach(self.browser.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
            raise e
    return wrapper


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--executor", action="store", default="172.17.0.2")
    parser.addoption("--vnc", action="store_true")
    parser.addoption("--logs", action="store_true")
    parser.addoption("--video", action="store_true")
    parser.addoption("--bv", action="store", default="latest")


@pytest.fixture()
def browser(request):
    browser = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    vnc = request.config.getoption("--vnc")
    version = request.config.getoption("--bv")
    logs = request.config.getoption("--logs")
    video = request.config.getoption("--video")

    options = None
    driver = None

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        chromedriver_path = "/usr/bin/chromedriver"
        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
    elif browser == "firefox":
        options = FireFoxOptions()
        options.binary_location = "/usr/bin/firefox"
        geckodriver_path = "/usr/bin/geckodriver"
        service = FirefoxService(executable_path=geckodriver_path)
        driver = webdriver.Firefox(service=service, options=options)

    capabilities = {
        'browserName': browser,
        'browserVersion': version,
        "selenoid:options": {
            "enableVNC": vnc,
            "name": request.node.name,
            "screenResolution": "1920x1080x24",
            "enableVideo": video,
            "enableLog": logs
        }
    }

    if options:
        for k, v in capabilities.items():
            options.set_capability(k, v)

    try:
        driver.maximize_window()
        yield driver
    finally:
        if driver is not None:
            driver.quit()
