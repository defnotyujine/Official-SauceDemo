import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

@pytest.fixture(scope="session")
def driver():
    options = webdriver.FirefoxOptions()
    options.headless = True  # Run in headless mode for speed
    driver = webdriver.Firefox(options=options)
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
    try:
        WebDriverWait(driver, 2).until(EC.url_contains("inventory.html"))  # Reduced wait time
    except:
        pass

def get_error_message(driver):
    error_element = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    return error_element.text

def reset_app_state(driver):
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "reset_sidebar_link"))).click() # reduced wait time
    driver.find_element(By.ID, "react-burger-cross-btn").click()

def write_result(test_name, result):
    filepath = os.path.expanduser("~/Official-SauceDemo/Functionality/Compiled/Results/ErrorHandling.txt")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "a") as f:
        f.write(f"{test_name}: {result}\n")

def test_FEH_01_blank_username_password(driver):
    test_name = "FEH_01"
    try:
        login(driver, "", "")
        error_message = get_error_message(driver)
        assert "Username is required" in error_message, f"Unexpected error message: {error_message}"
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FEH_02_blank_password(driver):
    test_name = "FEH_02"
    try:
        login(driver, "standard_user", "")
        error_message = get_error_message(driver)
        assert "Password is required" in error_message, f"Unexpected error message: {error_message}"
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FEH_03_invalid_username_password(driver):
    test_name = "FEH_03"
    try:
        login(driver, "invalid_user", "invalid_password")
        error_message = get_error_message(driver)
        assert "Username and password do not match any user in this service" in error_message, f"Unexpected error message: {error_message}"
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FEH_04_locked_out_user(driver):
    test_name = "FEH_04"
    try:
        login(driver, "locked_out_user", "secret_sauce")
        error_message = get_error_message(driver)
        assert "Sorry, this user has been locked out" in error_message, f"Unexpected error message: {error_message}"
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FEH_05_empty_cart_checkout_standard(driver):
    test_name = "FEH_05"
    try:
        login(driver, "standard_user", "secret_sauce")
        reset_app_state(driver)
        driver.refresh()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        current_url_before = driver.current_url
        driver.find_element(By.ID, "checkout").click()
        WebDriverWait(driver, 2).until(lambda d: d.current_url != "")
        current_url_after = driver.current_url

        if current_url_after != current_url_before:
            raise Exception(f"URL changed to {current_url_after} after checkout click with empty cart")
        
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FEH_06_empty_cart_checkout_problem(driver):
    test_name = "FEH_06"
    try:
        login(driver, "problem_user", "secret_sauce")
        reset_app_state(driver)
        driver.refresh()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        current_url_before = driver.current_url
        driver.find_element(By.ID, "checkout").click()
        WebDriverWait(driver, 2).until(lambda d: d.current_url != "")
        current_url_after = driver.current_url

        if current_url_after != current_url_before:
            raise Exception(f"URL changed to {current_url_after} after checkout click with empty cart")

        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FEH_07_empty_cart_checkout_performance(driver):
    test_name = "FEH_07"
    try:
        login(driver, "performance_glitch_user", "secret_sauce")
        reset_app_state(driver)
        driver.refresh()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        current_url_before = driver.current_url
        driver.find_element(By.ID, "checkout").click()
        WebDriverWait(driver, 2).until(lambda d: d.current_url != "")
        current_url_after = driver.current_url

        if current_url_after != current_url_before:
            raise Exception(f"URL changed to {current_url_after} after checkout click with empty cart")

        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FEH_08_empty_cart_checkout_error(driver):
    test_name = "FEH_08"
    try:
        login(driver, "error_user", "secret_sauce")
        reset_app_state(driver)
        driver.refresh()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        current_url_before = driver.current_url
        driver.find_element(By.ID, "checkout").click()
        WebDriverWait(driver, 2).until(lambda d: d.current_url != "")
        current_url_after = driver.current_url

        if current_url_after != current_url_before:
            raise Exception(f"URL changed to {current_url_after} after checkout click with empty cart")

        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_FEH_09_empty_cart_checkout_visual(driver):
    test_name = "FEH_09"
    try:
        login(driver, "visual_user", "secret_sauce")
        reset_app_state(driver)
        driver.refresh()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        current_url_before = driver.current_url
        driver.find_element(By.ID, "checkout").click()
        WebDriverWait(driver, 2).until(lambda d: d.current_url != "")
        current_url_after = driver.current_url

        if current_url_after != current_url_before:
            raise Exception(f"URL changed to {current_url_after} after checkout click with empty cart")

        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise
