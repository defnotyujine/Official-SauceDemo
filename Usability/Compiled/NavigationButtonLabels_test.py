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
    login_label = login_button.get_attribute("value").strip()
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()
    WebDriverWait(driver, 30).until(EC.url_contains("inventory.html"))
    return login_label

def get_labels(driver):
    labels = {}

    add_button = driver.find_element(By.XPATH, "//button[starts-with(@id, 'add-to-cart')]")
    labels["Add to Cart"] = add_button.text.strip()
    add_button.click()

    remove_button = driver.find_element(By.XPATH, "//button[starts-with(@id, 'remove')]")
    labels["Remove"] = remove_button.text.strip()

    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver, 10).until(EC.url_contains("cart.html"))

    labels["Checkout"] = driver.find_element(By.ID, "checkout").text.strip()
    labels["Continue Shopping"] = driver.find_element(By.ID, "continue-shopping").text.strip()

    driver.find_element(By.ID, "checkout").click()
    WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-one.html"))

    wait = WebDriverWait(driver, 10)
    continue_btn = wait.until(EC.presence_of_element_located((By.ID, "continue")))
    cancel_btn = wait.until(EC.presence_of_element_located((By.ID, "cancel")))

    labels["Continue"] = continue_btn.get_attribute("value").strip()
    labels["Cancel"] = cancel_btn.get_attribute("data-test").capitalize().strip()

    return labels

def write_result(test_name, message, new_block=False):
    """
    Writes test result to file.

    Args:
        test_name (str): The name of the test case (e.g., "UN_06").
        message (str): The result message.
        new_block (bool, optional):  If True, adds a newline *before* writing.
    """
    filepath = os.path.expanduser("~/Official-SauceDemo/Usability/Compiled/Results/NavigationButtonLabels.txt")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "a") as f:
        if new_block:
            f.write("\n")
        f.write(f"{test_name}: {message}\n")

baseline_labels = {
    "Add to Cart": "Add to cart",
    "Remove": "Remove",
    "Checkout": "Checkout",
    "Continue Shopping": "Continue Shopping",
    "Continue": "Continue",
    "Cancel": "Cancel",
    "Login": "Login"
}

@pytest.mark.parametrize(
    "username, test_id",
    [
        ("standard_user", "UN_06"),
        ("problem_user", "UN_07"),
        ("performance_glitch_user", "UN_08"),
        ("error_user", "UN_09"),
        ("visual_user", "UN_10"),
    ],
)
def test_button_labels(driver, username, test_id):
    test_name = f"{test_id}_Button_Label_Comparison"
    try:
        login_label = login(driver, username, "secret_sauce")
        labels = get_labels(driver)
        labels["Login"] = login_label

        for key in baseline_labels:
            expected = baseline_labels[key]
            actual = labels.get(key, "Missing")
            if expected.lower() == actual.lower():
                write_result(test_name, f"{key}: ✅ Match - '{actual}'")
            else:
                write_result(test_name, f"{key}: ❌ Mismatch - Expected: '{expected}', Got: '{actual}'")
        if test_id != "UN_10":
            write_result("", "", new_block=True)

    except Exception as e:
        write_result(test_name, f"❌ Error: {e}")
        raise
