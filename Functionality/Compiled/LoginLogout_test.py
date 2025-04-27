import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
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

def logout(driver):
    sidebar_button = driver.find_element(By.ID, "react-burger-menu-btn")
    sidebar_button.click()
    logout_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link")))
    logout_button.click()
    WebDriverWait(driver, 10).until(EC.url_to_be("https://www.saucedemo.com/"))

def write_result(test_name, result):
    filepath = os.path.expanduser("~/Official-SauceDemo/Functionality/Compiled/Results/LoginLogout.txt")
    os.makedirs(os.path.dirname(filepath), exist_ok=True) 
    with open(filepath, "a") as f:
        f.write(f"{test_name}: {result}\n")

def test_blank_login(driver):
    test_name = "FL_01"
    try:
        driver.get("https://www.saucedemo.com/")
        login(driver, "", "")
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h3[@data-test='error']"))
        )
        assert "Username is required" in error_message.text or "Password is required" in error_message.text, "Login did not produce the expected error message."
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_standard_user_login(driver):
    test_name = "FL_02"
    try:
        driver.get("https://www.saucedemo.com/")
        login(driver, "standard_user", "secret_sauce")
        assert "inventory.html" in driver.current_url, "Login was unsuccessful for standard_user."
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_locked_out_user_login(driver):
    test_name = "Fl_03"
    try:
        driver.get("https://www.saucedemo.com/")
        login(driver, "locked_out_user", "secret_sauce")
        assert "inventory.html" in driver.current_url, "Account Failed to Login"
        write_result(test_name, "Pass")
    except AssertionError as e:  
        write_result(test_name, "Fail: Account Failed to Login")
        raise
    except Exception as e: 
        write_result(test_name, f"Fail: {type(e).__name__}: {e}") 
        raise
    
def test_problem_user_login(driver):
    test_name = "FL_04"
    try:
        driver.get("https://www.saucedemo.com/")
        login(driver, "problem_user", "secret_sauce")
        assert "inventory.html" in driver.current_url, "Login was unsuccessful for problem_user."
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_performance_glitch_user_login(driver):
    test_name = "FL_05"
    try:
        driver.get("https://www.saucedemo.com/")
        login(driver, "performance_glitch_user", "secret_sauce")
        time.sleep(5)
        assert "inventory.html" in driver.current_url, "Login was unsuccessful for performance_glitch_user."
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_error_user_login(driver):
    test_name = "Fl_06"
    try:
        driver.get("https://www.saucedemo.com/")
        login(driver, "error_user", "secret_sauce")
        assert "inventory.html" in driver.current_url, "Login was unsuccessful for error_user."
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_visual_user_login(driver):
    test_name = "FL_07"
    try:
        driver.get("https://www.saucedemo.com/")
        login(driver, "visual_user", "secret_sauce")
        assert "inventory.html" in driver.current_url, "Login was unsuccessful for visual_user."
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_invalid_login(driver):
    test_name = "FL_08"
    try:
        driver.get("https://www.saucedemo.com/")
        login(driver, "invalid_user", "invalid_password")
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h3[@data-test='error']"))
        )
        assert "Username and password do not match any user in this service" in error_message.text, "Login did not produce the expected error message for invalid credentials."
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_standard_user_logout(driver):
    test_name = "FLO_01"
    try:
        login(driver, "standard_user", "secret_sauce")
        WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
        logout(driver)
        assert "saucedemo.com" in driver.current_url, "Logout failed for standard_user."
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_problem_user_logout(driver):
    test_name = "FLO_02"
    try:
        login(driver, "problem_user", "secret_sauce")
        WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
        logout(driver)
        assert "saucedemo.com" in driver.current_url, "Logout failed for problem_user."
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_performance_glitch_user_logout(driver):
    test_name = "FLO_03"
    try:
        login(driver, "performance_glitch_user", "secret_sauce")
        WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
        logout(driver)
        assert "saucedemo.com" in driver.current_url, "Logout failed for performance_glitch_user."
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_error_user_logout(driver):
    test_name = "FLO_04"
    try:
        login(driver, "error_user", "secret_sauce")
        WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
        logout(driver)
        assert "saucedemo.com" in driver.current_url, "Logout failed for error_user."
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_visual_user_logout(driver):
    test_name = "FLO_05"
    try:
        login(driver, "visual_user", "secret_sauce")
        WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
        logout(driver)
        assert "saucedemo.com" in driver.current_url, "Logout failed for visual_user."
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise