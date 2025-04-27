import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

BASE_URL = "https://www.saucedemo.com/"
ACCEPTABLE_RESPONSE_TIME = 2  
OUTPUT_FILENAME = "UserPerformance.txt"

def write_grouped_results(test_case_id, results_dict):
    filepath = os.path.expanduser(f"~/Official-SauceDemo/Performance/Compiled/Results/{OUTPUT_FILENAME}")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "a") as f:
        f.write(f"\n=== {test_case_id} ===\n")
        for step, result in results_dict.items():
            f.write(f"{step}: {result}\n")
        f.write("\n")

def login(driver, username, password):
    driver.get(BASE_URL)
    username_field = driver.find_element(By.ID, "user-name")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))

def go_to_cart(driver):
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver, 10).until(EC.url_contains("cart.html"))

def go_back(driver):
    driver.back()

def go_to_all_items(driver):
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "bm-menu")))
    driver.find_element(By.ID, "inventory_sidebar_link").click()
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))

def measure_response_time(func, driver, *args):
    start_time = time.time()
    func(driver, *args)
    end_time = time.time()
    return end_time - start_time

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()

@pytest.mark.parametrize(
    "username, test_case_id",
    [
        ("standard_user", "PUP_01"),
        ("problem_user", "PUP_02"),
        ("performance_glitch_user", "PUP_03"),
        ("error_user", "PUP_04"),
        ("visual_user", "PUP_05"),
    ],
)
def test_page_load_times(driver, username, test_case_id):
    results = {}
    failures = []

    try:
        login_time = measure_response_time(login, driver, username, "secret_sauce")
        if login_time < ACCEPTABLE_RESPONSE_TIME:
            results["Login"] = f"Pass ({login_time:.2f}s)"
        else:
            results["Login"] = f"Fail ({login_time:.2f}s)"
            failures.append(f"Login took too long: {login_time:.2f}s")

        go_to_cart_time = measure_response_time(go_to_cart, driver)
        if go_to_cart_time < ACCEPTABLE_RESPONSE_TIME:
            results["GoToCart"] = f"Pass ({go_to_cart_time:.2f}s)"
        else:
            results["GoToCart"] = f"Fail ({go_to_cart_time:.2f}s)"
            failures.append(f"GoToCart took too long: {go_to_cart_time:.2f}s")

        back_to_inventory_time = measure_response_time(go_back, driver)
        if back_to_inventory_time < ACCEPTABLE_RESPONSE_TIME:
            results["BackToInventory"] = f"Pass ({back_to_inventory_time:.2f}s)"
        else:
            results["BackToInventory"] = f"Fail ({back_to_inventory_time:.2f}s)"
            failures.append(f"BackToInventory took too long: {back_to_inventory_time:.2f}s")

        all_items_time = measure_response_time(go_to_all_items, driver)
        if all_items_time < ACCEPTABLE_RESPONSE_TIME:
            results["AllItems"] = f"Pass ({all_items_time:.2f}s)"
        else:
            results["AllItems"] = f"Fail ({all_items_time:.2f}s)"
            failures.append(f"AllItems took too long: {all_items_time:.2f}s")

    finally:
        write_grouped_results(test_case_id, results)

    assert not failures, f"{test_case_id} failed steps:\n" + "\n".join(failures)


