import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Firefox() 
    yield driver
    driver.quit()

def login(driver, username="standard_user", password="secret_sauce"):
    driver.get("https://www.saucedemo.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name")))
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 10).until(EC.url_contains("inventory"))

def navigate_to_cart(driver):
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver, 10).until(EC.url_contains("cart"))

def add_all_items_to_cart(driver):
    add_buttons = driver.find_elements(By.XPATH, "//button[starts-with(@id, 'add-to-cart')]")
    initial_item_count = len(driver.find_elements(By.CLASS_NAME, "inventory_item"))
    if len(add_buttons) != 6:
        pytest.fail(f"Expected 6 items on the inventory page, but found {initial_item_count}.")
    for button in add_buttons:
        button.click()

def get_cart_item_count(driver):
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    return len(cart_items)

def check_element_presence(driver, by_type, locator):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((by_type, locator)))
        return True, ""
    except:
        return False, f"Element with locator '{locator}' not found."

def write_result(test_id, result, details=""):
    filepath = os.path.expanduser("~/Official-SauceDemo/Usability/Compiled/Results/Responsiveness.txt")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "a") as f:
        f.write(f"{test_id}: {result}\n")
        if result == "Fail" and details:
            f.write(f"Details:\n{details}\n\n")

def check_cart_responsiveness(driver, width, height):
    driver.set_window_size(width, height)
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_list")))
        cart_list = driver.find_element(By.CLASS_NAME, "cart_list")
        return cart_list.is_displayed(), ""
    except:
        return False, f"Cart elements not visible at {width}x{height}."

@pytest.mark.parametrize("test_id,width,height", [
    ("UR_01", 375, 667),   
    ("UR_02", 768, 1024),  
])
def test_mobile_and_tablet_cart_functionality(driver, test_id, width, height):
    try:
        login(driver)
        add_all_items_to_cart(driver)
        navigate_to_cart(driver)

        cart_item_count = get_cart_item_count(driver)
        if cart_item_count != 6:
            pytest.fail(f"Expected 6 items in the cart, but found {cart_item_count}.")

        continue_shopping_present, continue_shopping_details = check_element_presence(driver, By.ID, "continue-shopping")
        checkout_present, checkout_details = check_element_presence(driver, By.ID, "checkout")
        cart_layout_ok, cart_details = check_cart_responsiveness(driver, width, height)

        overall_result = "Pass"
        details = ""

        if not continue_shopping_present:
            overall_result = "Fail"
            details += f"Continue Shopping button not present: {continue_shopping_details}\n"
        if not checkout_present:
            overall_result = "Fail"
            details += f"Checkout button not present: {checkout_details}\n"
        if not cart_layout_ok:
            overall_result = "Fail"
            details += f"Cart layout issue at {width}x{height}: {cart_details}\n"

        write_result(test_id, overall_result, details.strip())

    except pytest.fail.Exception:
        pass
    except Exception as e:
        write_result(test_id, "Error", str(e))
        raise

def test_desktop_resize_cart_functionality(driver):
    test_id = "UR_03"
    try:
        login(driver)
        add_all_items_to_cart(driver)
        navigate_to_cart(driver)

        cart_item_count = get_cart_item_count(driver)
        if cart_item_count != 6:
            pytest.fail(f"Expected 6 items in the cart, but found {cart_item_count}.")

        overall_result = "Pass"
        details = ""
        sizes = [
            (1024, 768),   
            (1280, 800),   
            (1440, 900),   
            (1920, 1080)   
        ]

        for w, h in sizes:
            continue_shopping_present, continue_shopping_details = check_element_presence(driver, By.ID, "continue-shopping")
            checkout_present, checkout_details = check_element_presence(driver, By.ID, "checkout")
            cart_layout_ok, cart_details = check_cart_responsiveness(driver, w, h)

            if not continue_shopping_present:
                overall_result = "Fail"
                details += f"Continue Shopping button not present at {w}x{h}: {continue_shopping_details}\n"
            if not checkout_present:
                overall_result = "Fail"
                details += f"Checkout button not present at {w}x{h}: {checkout_details}\n"
            if not cart_layout_ok:
                overall_result = "Fail"
                details += f"Cart layout issue at {w}x{h}: {cart_details}\n"

        write_result(test_id, overall_result, details.strip())

    except pytest.fail.Exception:
        pass
    except Exception as e:
        write_result(test_id, "Error", str(e))
        raise