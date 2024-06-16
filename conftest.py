import logging
from functools import wraps
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
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
    parser.addoption("--executor", action="store", default="127.0.0.1")
    parser.addoption("--vnc", action="store_true")
    parser.addoption("--logs", action="store_true")
    parser.addoption("--video", action="store_true")
    parser.addoption("--bv")


@pytest.fixture()
def browser(request):
    browser = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    vnc = request.config.getoption("--vnc")
    version = request.config.getoption("--bv")
    logs = request.config.getoption("--logs")
    video = request.config.getoption("--video")

    executor_url = f'http://{executor}:4444/wd/hub'
    options = None

    if browser == "chrome":
        options = ChromeOptions()
    elif browser == "firefox":
        options = FireFoxOptions()

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

    for k, v in capabilities.items():
        options.set_capability(k, v)

    driver = None
    try:
        driver = webdriver.Remote(
            command_executor=executor_url,
            options=options
        )
        driver.maximize_window()
        yield driver
    finally:
        if driver is not None:
            driver.quit()

