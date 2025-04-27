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

def expand_sidebar(driver):
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "bm-menu")))

def get_sidebar_links(driver):
    sidebar = driver.find_element(By.CLASS_NAME, "bm-menu")
    links = sidebar.find_elements(By.TAG_NAME, "a")
    return [link.text.strip() for link in links]

def write_result(test_name, message, new_block=False):
    """
    Writes test result to file.

    Args:
        test_name (str): The name of the test case (e.g., "UN_01").
        message (str): The result message (e.g., "All Items: ✅ Present").
        new_block (bool, optional): If True, adds a newline *before* writing.
    """
    filepath = os.path.expanduser("~/Official-SauceDemo/Usability/Compiled/Results/NavigationSidebar.txt")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "a") as f:
        if new_block:
            f.write("\n")
        f.write(f"{test_name}: {message}\n")

@pytest.mark.parametrize(
    "username, test_id",
    [
        ("standard_user", "UN_01"),
        ("problem_user", "UN_02"),
        ("performance_glitch_user", "UN_03"),
        ("error_user", "UN_04"),
        ("visual_user", "UN_05"),
    ],
)
def test_sidebar_navigation_links_present(driver, username, test_id):
    expected_links = ["All Items", "About", "Logout", "Reset App State"]
    try:
        login(driver, username, "secret_sauce")
        expand_sidebar(driver)
        actual_links = get_sidebar_links(driver)

        # Write the results for the current test case
        for i, link in enumerate(expected_links):
            write_result(test_id, f"{link}: ✅ Present") if link in actual_links else write_result(test_id, f"{link}: ❌ Missing")
        if test_id != "UN_05":
            write_result("", "", new_block=True)

    except Exception as e:
        write_result(test_id, f"❌ Error: {e}")
        raise
