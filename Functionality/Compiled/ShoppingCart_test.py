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

def add_specific_items_to_cart(driver, username):
    driver.refresh()
    items_to_add = ["add-to-cart-sauce-labs-backpack", "add-to-cart-sauce-labs-bike-light", "add-to-cart-sauce-labs-onesie"]
    for item_id in items_to_add:
        driver.find_element(By.ID, item_id).click()
    WebDriverWait(driver, 10).until(lambda d: d.find_element(By.CLASS_NAME, "shopping_cart_badge").text == "3")

def add_all_items_to_cart(driver):
    driver.refresh()
    add_to_cart_buttons = driver.find_elements(By.XPATH, "//button[text()='Add to cart']")
    for button in add_to_cart_buttons:
        button.click()
    WebDriverWait(driver, 10).until(lambda d: d.find_element(By.CLASS_NAME, "shopping_cart_badge").text == "6")

def verify_cart_items(driver, username):
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    item_count = 3 if username in ["problem_user", "error_user"] else 6
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(cart_items) == item_count, f"Expected {item_count} items in cart, but found {len(cart_items)}."

    for item in cart_items:
        name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
        description = item.find_element(By.CLASS_NAME, "inventory_item_desc").text
        price = item.find_element(By.CLASS_NAME, "inventory_item_price").text

        assert name != "", "Item name is empty"
        assert description != "", "Item description is empty"
        assert price != "", "Item price is empty"
    driver.find_element(By.ID, "continue-shopping").click()

def remove_items_from_cart(driver, username):
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    remove_buttons = driver.find_elements(By.XPATH, "//button[text()='Remove']")
    for button in remove_buttons:
        button.click()
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    driver.find_element(By.ID, "continue-shopping").click()

def write_result(test_name, result):
    filepath = os.path.expanduser("~/Official-SauceDemo/Functionality/Compiled/Results/ShoppingCart.txt")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "a") as f:
        f.write(f"{test_name}: {result}\n")

def test_standard_user_cart(driver):
    test_name = "FSC_01"
    try:
        login(driver, "standard_user", "secret_sauce")
        reset_app_state(driver)
        add_all_items_to_cart(driver)
        verify_cart_items(driver, "standard_user")
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_problem_user_cart(driver):
    test_name = "FSC_02"
    try:
        login(driver, "problem_user", "secret_sauce")
        reset_app_state(driver)
        add_specific_items_to_cart(driver, "problem_user")
        verify_cart_items(driver, "problem_user")
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_performance_glitch_user_cart(driver):
    test_name = "FSC_03"
    try:
        login(driver, "performance_glitch_user", "secret_sauce")
        reset_app_state(driver)
        add_all_items_to_cart(driver)
        verify_cart_items(driver, "performance_glitch_user")
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_error_user_cart(driver):
    test_name = "FSC_04"
    try:
        login(driver, "error_user", "secret_sauce")
        reset_app_state(driver)
        add_specific_items_to_cart(driver, "error_user")
        verify_cart_items(driver, "error_user")
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_visual_user_cart(driver):
    test_name = "FSC_05"
    try:
        login(driver, "visual_user", "secret_sauce")
        reset_app_state(driver)
        add_all_items_to_cart(driver)
        verify_cart_items(driver, "visual_user")
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_standard_user_remove_cart_items(driver):
    test_name = "FSC_06"
    try:
        login(driver, "standard_user", "secret_sauce")
        reset_app_state(driver)
        add_all_items_to_cart(driver)
        remove_items_from_cart(driver, "standard_user")
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_problem_user_remove_cart_items(driver):
    test_name = "FSC_07"
    try:
        login(driver, "problem_user", "secret_sauce")
        reset_app_state(driver)
        add_specific_items_to_cart(driver, "problem_user")
        remove_items_from_cart(driver, "problem_user")
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_performance_glitch_user_remove_cart_items(driver):
    test_name = "FSC_08"
    try:
        login(driver, "performance_glitch_user", "secret_sauce")
        reset_app_state(driver)
        add_all_items_to_cart(driver)
        remove_items_from_cart(driver, "performance_glitch_user")
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_error_user_remove_cart_items(driver):
    test_name = "FSC_09"
    try:
        login(driver, "error_user", "secret_sauce")
        reset_app_state(driver)
        add_specific_items_to_cart(driver, "error_user")
        remove_items_from_cart(driver, "error_user")
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_visual_user_remove_cart_items(driver):
    test_name = "FSC_10"
    try:
        login(driver, "visual_user", "secret_sauce")
        reset_app_state(driver)
        add_all_items_to_cart(driver)
        remove_items_from_cart(driver, "visual_user")
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise