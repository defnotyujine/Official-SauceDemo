import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import random

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()

def get_random_user():
    users = {
        "standard_user": "secret_sauce",
        "problem_user": "secret_sauce",
        "performance_glitch_user": "secret_sauce"
    }
    user, password = random.choice(list(users.items()))
    return user, password

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

def write_result(test_name, result):
    filepath = os.path.expanduser("~/Official-SauceDemo/Functionality/Compiled/Results/SidebarButtons.txt")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "a") as f:
        f.write(f"{test_name}: {result}\n")

def test_FSB_01_all_items_redirect(driver):
    test_name = "FSB_01"
    try:
        user, password = get_random_user()
        login(driver, user, password)
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "inventory_sidebar_link"))).click()
        WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FSB_02_about_redirect(driver):
    test_name = "FSB_02"
    try:
        user, password = get_random_user()
        login(driver, user, password)
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "about_sidebar_link"))).click()
        WebDriverWait(driver, 10).until(EC.url_contains("saucelabs.com"))
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FSB_03_logout_redirect(driver):
    test_name = "FSB_03"
    try:
        user, password = get_random_user()
        login(driver, user, password)
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))).click()
        WebDriverWait(driver, 10).until(EC.url_contains("saucedemo.com"))
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FSB_04_reset_app_state(driver):
    test_name = "FSB_04"
    try:
        user, password = get_random_user()
        login(driver, user, password)
        driver.find_element(By.CLASS_NAME, "product_sort_container").click()
        driver.find_element(By.XPATH, "//option[@value='za']").click()
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "reset_sidebar_link"))).click()
        driver.find_element(By.ID, "react-burger-cross-btn").click()
        driver.refresh()

        sort_value = driver.find_element(By.CLASS_NAME, "active_option").text
        cart_count = len(driver.find_elements(By.CLASS_NAME, "shopping_cart_badge"))

        assert sort_value == "Name (A to Z)", "Filter not reset"
        assert cart_count == 0, "Cart not reset"
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise