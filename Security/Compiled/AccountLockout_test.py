import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Firefox()  
    yield driver
    driver.quit()

def login(driver, username, password):
    driver.get("https://www.saucedemo.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name")))
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

def check_login_error(driver):
    try:
        error_element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Username and password do not match')]")))
        return error_element.is_displayed()
    except:
        return False

def check_account_locked(driver, lockout_message_part):
    try:
        locked_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{lockout_message_part}')]")))
        return locked_element.is_displayed()
    except:
        return False

def write_result(test_id, result, details=""):
    filepath = os.path.expanduser("~/Official-SauceDemo/Security/Compiled/Results/AccountLockout.txt")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "a") as f:
        f.write(f"{test_id}: {result}\n")
        if result == "Fail" and details:
            f.write(f"Details:\n{details}\n\n")

def test_login_lockout_standard_user(driver):
    test_id = "SLS_01_standard_user_30_attempts"
    result = "Pass"
    details = ""
    username = "standard_user"
    incorrect_password_base = "wrong_password_"
    lockout_threshold = 30

    driver.get("https://www.saucedemo.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name")))
    username_field = driver.find_element(By.ID, "user-name")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username_field.send_keys(username)

    for attempt in range(1, lockout_threshold + 1):
        password_field.clear()
        password_field.send_keys(f"{incorrect_password_base}{attempt}")
        login_button.click()
        if not check_login_error(driver):
            result = "Fail"
            details += f"Attempt {attempt}: Login did not fail with incorrect credentials.\n"
            break

    password_field.clear()
    password_field.send_keys("secret_sauce")
    login_button.click()

    if driver.current_url == "https://www.saucedemo.com/inventory.html":
        result = "Fail"
        details += "Account lockout did not occur after 30 failed attempts.\n"
    else:
        details += "Account lockout was triggered after 30 failed attempts.\n"

    write_result(test_id, result, details)
    assert result == "Pass", f"{test_id} failed: {details}"