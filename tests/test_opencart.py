from home_page import HomePage
from catalog_laptops_page import CatalogLaptopsPage
from product_info_page import ProductInfoPage
from admin_page import AdminPage
from register_page import RegisterPage
from desktop_page import DesktopsPage
from config import ADMIN_USERNAME, ADMIN_PASSWORD
from generate_random_user import generate_random_user
import allure


@allure.feature("Главная страница")
def test_home_page(browser):
    home_page = HomePage(browser)
    home_page.load()
    assert home_page.is_logo_displayed()
    assert home_page.is_search_field_displayed()
    assert home_page.is_cart_displayed()
    assert home_page.is_carousel_displayed()
    assert home_page.is_macbook_image_displayed()
    assert home_page.is_iphone_image_displayed()
    home_page.header.click_my_account()
    assert home_page.header.is_register_displayed()
    assert home_page.header.is_login_displayed()


@allure.feature("Страница каталога ноутбуков")
def test_catalog_laptop_notebooks(browser):
    catalog_page = CatalogLaptopsPage(browser)
    catalog_page.load()
    assert catalog_page.is_laptops_notebooks_displayed()
    assert catalog_page.is_product_list_displayed()
    assert catalog_page.is_product_image_displayed()
    catalog_page.click_list_view()
    assert catalog_page.is_product_list_view()


@allure.feature("Страница информации о продукте HP LP3065")
def test_product_info_hp_lp3065(browser):
    product_info_page = ProductInfoPage(browser)
    product_info_page.load()
    product_info_page.click_hp_lp3065()
    assert product_info_page.is_hp_lp3065_url
    assert product_info_page.is_product_image_displayed()
    assert product_info_page.is_price_displayed()
    assert product_info_page.is_calendar_displayed
    assert product_info_page.is_add_to_cart_displayed()


@allure.feature("Страница администрирования")
def test_administration_login(browser):
    admin_page = AdminPage(browser)
    admin_page.load()
    assert admin_page.is_logo_displayed()
    assert admin_page.is_header_displayed()
    assert admin_page.is_username_field_displayed()
    assert admin_page.is_password_field_displayed()
    assert admin_page.is_login_button_displayed()
    admin_page.login(ADMIN_USERNAME, ADMIN_PASSWORD)
    assert admin_page.is_dashboard_displayed()
    admin_page.logout()
    assert admin_page.is_header_displayed()


@allure.feature("Страница регистрации")
def test_register_account(browser):
    register_page = RegisterPage(browser)
    register_page.load()
    assert register_page.is_name_field_displayed()
    assert register_page.is_last_name_field_displayed()
    assert register_page.is_email_field_displayed()
    assert register_page.is_password_field_displayed()
    assert register_page.is_continue_button_displayed()


@allure.feature("Добавление случайного продукта в корзину")
def test_add_random_product_to_cart(browser):
    home_page = HomePage(browser)
    home_page.load()
    home_page.add_random_product_to_cart()
    assert home_page.is_product_added_to_cart()


@allure.feature("Смена валюты на главной странице")
def test_currency_change_main_page(browser):
    home_page = HomePage(browser)
    home_page.load()
    price_before_change = home_page.get_product_prices()
    home_page.header.change_currency("EUR")
    price_after_change = home_page.get_product_prices()
    assert price_after_change != price_before_change, "Цена не изменилась"
    price_before_change = home_page.get_product_prices()
    home_page.header.change_currency("GBP")
    price_after_change = home_page.get_product_prices()
    assert price_after_change != price_before_change, "Цена не изменилась"
    price_before_change = home_page.get_product_prices()
    home_page.header.change_currency("USD")
    price_after_change = home_page.get_product_prices()
    assert price_after_change != price_before_change, "Цена не изменилась"


@allure.feature("Смена валюты на странице каталога компьютеров")
def test_currency_change_catalog_desktops_page(browser):
    desktops_page = DesktopsPage(browser)
    desktops_page.load()
    price_before_change = desktops_page.get_product_prices()
    desktops_page.header.change_currency("GBP")
    price_after_change = desktops_page.get_product_prices()
    assert price_after_change != price_before_change, "Цена не изменилась"


@allure.feature("Добавление продукта в административной секции")
def test_add_product_in_admin_section(browser):
    admin_page = AdminPage(browser)
    admin_page.load()
    admin_page.login(ADMIN_USERNAME, ADMIN_PASSWORD)
    admin_page.go_to_catalog_and_products().click()
    admin_page.add_new_product_button().click()
    admin_page.add_product()
    admin_page.save_button().click()
    admin_page.modified_popup()


@allure.feature("Удаление продукта в административной секции")
def test_delete_product_in_admin_section(browser):
    admin_page = AdminPage(browser)
    admin_page.load()
    admin_page.login(ADMIN_USERNAME, ADMIN_PASSWORD)
    admin_page.go_to_catalog_and_products().click()
    admin_page.find_test_product_in_products()
    admin_page.find_checkbox_test_product().click()
    admin_page.delete_button().click()
    admin_page.alert_window_success()
    admin_page.modified_popup()


@allure.feature("Регистрация нового пользователя")
def test_register_new_user(browser):
    home_page = HomePage(browser)
    home_page.load()
    home_page.header.click_my_account()
    home_page.header.is_register_displayed().click()
    register_page = RegisterPage(browser)
    register_page.load()
    name, last_name, email, password = generate_random_user()
    register_page.enter_name(name)
    register_page.enter_last_name(last_name)
    register_page.enter_email(email)
    register_page.enter_password(password)
    register_page.privacy_policy_checkbox_agree().click()
    home_page.is_logout_displayed()
