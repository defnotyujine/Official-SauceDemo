import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()

def login(driver, username, password):
    driver.get("https://www.saucedemo.com/")
    username_field = driver.find_element(By.ID, "user-name")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))

def reset_app_state(driver):
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "reset_sidebar_link"))).click()
    driver.find_element(By.ID, "react-burger-cross-btn").click()

def add_items_to_cart(driver):
    driver.refresh()
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
    WebDriverWait(driver, 10).until(lambda d: d.find_element(By.CLASS_NAME, "shopping_cart_badge").text == "2")

def checkout(driver, firstname, lastname, postalcode):
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()

    first_name_field = driver.find_element(By.ID, "first-name")
    last_name_field = driver.find_element(By.ID, "last-name")
    postal_code_field = driver.find_element(By.ID, "postal-code")

    first_name_field.send_keys(firstname)
    last_name_field.send_keys(lastname)
    postal_code_field.send_keys(postalcode)

    if first_name_field.get_attribute("value") == "" or last_name_field.get_attribute("value") == "" or postal_code_field.get_attribute("value") == "":
        raise AssertionError("One or more text fields are empty before clicking continue.")

    driver.find_element(By.ID, "continue").click()
    driver.find_element(By.ID, "finish").click()

def get_item_prices(driver):
    prices = []
    price_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    for price_element in price_elements:
        prices.append(float(price_element.text.replace("$", "")))
    return prices

def checkout_and_verify_total(driver):
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()
    driver.find_element(By.ID, "first-name").send_keys("Eugene")
    driver.find_element(By.ID, "last-name").send_keys("Torre")
    driver.find_element(By.ID, "postal-code").send_keys("5009")
    driver.find_element(By.ID, "continue").click()

    prices = get_item_prices(driver)
    item1_price = prices[0]
    item2_price = prices[1]

    summary_subtotal_element = driver.find_element(By.CLASS_NAME, "summary_subtotal_label")
    summary_subtotal_text = summary_subtotal_element.text
    subtotal = float(summary_subtotal_text.split("$")[1])

    summary_tax_element = driver.find_element(By.CLASS_NAME, "summary_tax_label")
    summary_tax_text = summary_tax_element.text
    tax = float(summary_tax_text.split("$")[1])

    summary_total_element = driver.find_element(By.CLASS_NAME, "summary_total_label")
    summary_total_text = summary_total_element.text
    actual_total = float(summary_total_text.split("$")[1])

    expected_total = subtotal + tax

    assert actual_total == expected_total, f"Total price mismatch: Expected ${expected_total}, but got ${actual_total}"

def write_result(test_name, result):
    filepath = os.path.expanduser("~/Official-SauceDemo/Functionality/Compiled/Results/CheckoutProcess.txt")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "a") as f:
        f.write(f"{test_name}: {result}\n")

def test_FCP_01_standard_user_checkout(driver):
    test_name = "FCP_01"
    try:
        login(driver, "standard_user", "secret_sauce")
        reset_app_state(driver)
        driver.refresh()
        add_items_to_cart(driver)
        checkout(driver, "Eugene", "Torre", "5000")
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FCP_02_problem_user_checkout(driver):
    test_name = "FCP_02"
    try:
        login(driver, "problem_user", "secret_sauce")
        reset_app_state(driver)
        driver.refresh()
        add_items_to_cart(driver)
        checkout(driver, "Eugene", "Torre", "5000")
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FCP_03_performance_glitch_user_checkout(driver):
    test_name = "FCP_03"
    try:
        login(driver, "performance_glitch_user", "secret_sauce")
        reset_app_state(driver)
        driver.refresh()
        add_items_to_cart(driver)
        checkout(driver, "Eugene", "Torre", "5000")
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FCP_04_error_user_checkout(driver):
    test_name = "FCP_04"
    try:
        login(driver, "error_user", "secret_sauce")
        reset_app_state(driver)
        driver.refresh()
        add_items_to_cart(driver)
        checkout(driver, "Eugene", "Torre", "5000")
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FCP_05_visual_user_checkout(driver):
    test_name = "FCP_05"
    try:
        login(driver, "visual_user", "secret_sauce")
        reset_app_state(driver)
        driver.refresh()
        add_items_to_cart(driver)
        checkout(driver, "Eugene", "Torre", "5000")
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FCP_06_standard_user_checkout_total(driver):
    test_name = "FCP_06"
    try:
        login(driver, "standard_user", "secret_sauce")
        reset_app_state(driver)
        driver.refresh()
        add_items_to_cart(driver)
        checkout_and_verify_total(driver)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FCP_07_problem_user_checkout_total(driver):
    test_name = "FCP_07"
    try:
        login(driver, "problem_user", "secret_sauce")
        reset_app_state(driver)
        driver.refresh()
        add_items_to_cart(driver)
        checkout_and_verify_total(driver)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FCP_08_performance_glitch_user_checkout_total(driver):
    test_name = "FCP_08"
    try:
        login(driver, "performance_glitch_user", "secret_sauce")
        reset_app_state(driver)
        driver.refresh()
        add_items_to_cart(driver)
        checkout_and_verify_total(driver)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FCP_09_error_user_checkout_total(driver):
    test_name = "FCP_09"
    try:
        login(driver, "error_user", "secret_sauce")
        reset_app_state(driver)
        driver.refresh()
        add_items_to_cart(driver)
        checkout_and_verify_total(driver)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FCP_10_visual_user_checkout_total(driver):
    test_name = "FCP_10"
    try:
        login(driver, "visual_user", "secret_sauce")
        reset_app_state(driver)
        driver.refresh()
        add_items_to_cart(driver)
        checkout_and_verify_total(driver)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise