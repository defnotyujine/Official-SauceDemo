import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

SAUCE_USERS = [
    "standard_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user"
]

EXPECTED_PRODUCT_IMAGES = {
    "Sauce Labs Backpack": "https://www.saucedemo.com/static/media/sauce-backpack-1200x1500.0a0b85a3.jpg",
    "Sauce Labs Bike Light": "https://www.saucedemo.com/static/media/bike-light-1200x1500.37c843b0.jpg",
    "Sauce Labs Bolt T-Shirt": "https://www.saucedemo.com/static/media/bolt-shirt-1200x1500.c2599ac5.jpg",
    "Sauce Labs Fleece Jacket": "https://www.saucedemo.com/static/media/sauce-pullover-1200x1500.51d7ffaf.jpg",
    "Sauce Labs Onesie": "https://www.saucedemo.com/static/media/red-onesie-1200x1500.2ec615b2.jpg",
    "Test.allTheThings() T-Shirt (Red)": "https://www.saucedemo.com/static/media/red-tatt-1200x1500.30dadef4.jpg",
}

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()

def login(driver, username, password="secret_sauce"):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))

def write_result(test_name, result):
    filepath = os.path.expanduser("~/Official-SauceDemo/Usability/Compiled/Results/UIImages.txt")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "a") as f:
        f.write(f"{test_name}: {result}\n")

@pytest.mark.parametrize("user_type", SAUCE_USERS)
def test_user_product_images_match(driver, user_type):
    user_test_cases = {
        "standard_user": "UUI_16",
        "problem_user": "UUI_17",
        "performance_glitch_user": "UUI_18",
        "error_user": "UUI_19",
        "visual_user": "UUI_20",
    }

    test_name = user_test_cases[user_type]
    mismatched_images = {}

    try:
        login(driver, username=user_type)
        products = driver.find_elements(By.CLASS_NAME, "inventory_item")

        for product in products:
            try:
                title_element = product.find_element(By.CLASS_NAME, "inventory_item_name")
                product_name = title_element.text
                img_element = product.find_element(By.CLASS_NAME, "inventory_item_img").find_element(By.TAG_NAME, "img")
                img_src = img_element.get_attribute("src")

                expected_src = EXPECTED_PRODUCT_IMAGES.get(product_name)
                if expected_src and img_src != expected_src:
                    mismatched_images[product_name] = {"actual": img_src, "expected": expected_src}
                elif expected_src is None:
                    mismatched_images[product_name] = {"actual": img_src, "expected": "N/A (Product name not in expected list)"}

            except Exception:
                pass 

        if mismatched_images:
            error_message = "Mismatched product images found:\n"
            for name, details in mismatched_images.items():
                error_message += f"- {name}: Actual='{details['actual']}', Expected='{details['expected']}'\n"
            result = error_message
        else:
            result = "Pass"

    except Exception as e:
        result = f"🚨 Exception occurred: {e}"

    write_result(test_name, result)
    assert result == "Pass", f"{test_name} failed — {result}"