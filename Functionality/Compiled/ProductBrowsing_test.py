import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import os

expected_product_details = {
    "Sauce Labs Backpack": {
        "description": "Carry all the things with the sleek, streamlined sly pack that melds uncompromising style with unequaled laptop and tablet protection.",
        "price": "$29.99"
    },
    "Sauce Labs Bike Light": {
        "description": "A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes, 1 AAA battery included.",
        "price": "$9.99"
    },
    "Sauce Labs Bolt T-Shirt": {
        "description": "Get your testing superhero on with the Sauce Labs bolt T-shirt. From American Apparel, 100% ringspun combed cotton, heather gray with red bolt.",
        "price": "$15.99"
    },
    "Sauce Labs Fleece Jacket": {
        "description": "It's not every day that you come across a midweight quarter-zip fleece jacket capable of handling everything from a relaxing day outdoors to a busy day at the office.",
        "price": "$49.99"
    },
    "Sauce Labs Onesie": {
        "description": "Rib snap infant onesie for the junior automation engineer in development. Reinforced 3-snap bottom closure, two-needle hemmed sleeved and bottom won't unravel.",
        "price": "$7.99"
    },
    "T-Shirt (Red)": {
        "description": "This classic Sauce Labs t-shirt is perfect to wear when cozying up to your keyboard to automate a few tests. Super-soft and comfy ringspun combed cotton.",
        "price": "$15.99"
    },
}

results_file_path = os.path.expanduser("~/Official-SauceDemo/Functionality/Compiled/Results/ProductBrowsing.txt")
os.makedirs(os.path.dirname(results_file_path), exist_ok=True)

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

def verify_product_details(driver):
    errors = {}
    product_items = driver.find_elements(By.CLASS_NAME, "inventory_item")

    if len(product_items) != len(expected_product_details):
        errors["product_count"] = f"Number of products does not match expected. Expected: {len(expected_product_details)}, Actual: {len(product_items)}"

    for item in product_items:
        name_element = item.find_element(By.CLASS_NAME, "inventory_item_name")
        desc_element = item.find_element(By.CLASS_NAME, "inventory_item_desc")
        price_element = item.find_element(By.CLASS_NAME, "inventory_item_price")

        actual_name = name_element.text
        actual_description = desc_element.text.strip()
        actual_price = price_element.text

        if actual_name in expected_product_details:
            expected = expected_product_details[actual_name]
            if actual_description != expected["description"].strip():
                if "description_mismatch" not in errors:
                    errors["description_mismatch"] = []
                errors["description_mismatch"].append(f"Description mismatch for '{actual_name}'. Expected: '{expected['description'].strip()}', Actual: '{actual_description}'")
            if actual_price != expected["price"]:
                if "price_mismatch" not in errors:
                    errors["price_mismatch"] = []
                errors["price_mismatch"].append(f"Price mismatch for '{actual_name}'. Expected: '{expected['price']}', Actual: '{actual_price}'")
        else:
            if "name_mismatch" not in errors:
                errors["name_mismatch"] = []
            errors["name_mismatch"].append(f"Product name '{actual_name}' not found in expected details.")

    return errors

@pytest.mark.parametrize(
    "test_id, username",
    [
        ("FP_01", "standard_user"),
        ("FP_02", "problem_user"),
        ("FP_03", "performance_glitch_user"),
        ("FP_04", "error_user"),
        ("FP_05", "visual_user"),
    ],
)
def test_verify_product_details_for_user(driver, test_id, username):
    login(driver, username, "secret_sauce")
    print(f"\nExecuting Test Case ID: {test_id} for user: {username}")
    errors = verify_product_details(driver)

    result_string = ""
    if errors:
        result_string = "[FAIL]\n"
        for error_type, messages in errors.items():
            if isinstance(messages, list):
                for msg in messages:
                    result_string += f"  - {msg}\n"
            else:
                result_string += f"  - {messages}\n"
    else:
        result_string = "[PASS] - Product details are displayed correctly."

    print(f"{test_id} ({username}): {result_string}\n")

    with open(results_file_path, "a") as f:
        f.write(f"{test_id} ({username}): {result_string}\n\n")

    if errors:
        pytest.fail(result_string)

def reset_app_state(driver):
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "reset_sidebar_link"))).click()
    driver.find_element(By.ID, "react-burger-cross-btn").click()

def get_product_names(driver):
    product_name_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    return [element.text for element in product_name_elements]

def verify_sorting(driver, sort_option):
    sort_dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    sort_dropdown.select_by_value(sort_option)
    WebDriverWait(driver, 5).until(lambda d: Select(d.find_element(By.CLASS_NAME, "product_sort_container")).first_selected_option.get_attribute("value") == sort_option)
    product_names = get_product_names(driver)

    if sort_option == "az":
        assert product_names == sorted(product_names), "Sorting A to Z failed."
    elif sort_option == "za":
        assert product_names == sorted(product_names, reverse=True), "Sorting Z to A failed."
    elif sort_option == "lohi":
        prices = [float(p.text.replace("$", "")) for p in driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
        assert prices == sorted(prices), "Sorting Low to High failed."
    elif sort_option == "hilo":
        prices = [float(p.text.replace("$", "")) for p in driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
        assert prices == sorted(prices, reverse=True), "Sorting High to Low failed."

def add_all_items_to_cart(driver):
    driver.refresh()
    add_to_cart_buttons = driver.find_elements(By.XPATH, "//button[text()='Add to cart']")
    for button in add_to_cart_buttons:
        button.click()
    WebDriverWait(driver, 10).until(lambda d: d.find_element(By.CLASS_NAME, "shopping_cart_badge").text == "6")
    assert driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text == "6", "shopping_cart_badge is not equal to 6"

def remove_items_from_products_page(driver):
    remove_buttons = driver.find_elements(By.XPATH, "//button[text()='Remove']")
    for button in remove_buttons:
        button.click()
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))

def write_result(test_name, result):
    filepath = os.path.expanduser("~/Official-SauceDemo/Functionality/Compiled/Results/ProductBrowsing.txt")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "a") as f:
        f.write(f"{test_name}: {result}\n")

def test_standard_user_product_filtering(driver):
    test_name = "FP_06"
    try:
        login(driver, "standard_user", "secret_sauce")
        for sort_option in ["az", "za", "lohi", "hilo"]:
            verify_sorting(driver, sort_option)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: Sorting is broken!")
        raise

def test_problem_user_product_filtering(driver):
    test_name = "FP_07"
    try:
        login(driver, "problem_user", "secret_sauce")
        for sort_option in ["az", "za", "lohi", "hilo"]:
            verify_sorting(driver, sort_option)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: Sorting is broken!")
        raise

def test_performance_glitch_user_product_filtering(driver):
    test_name = "FP_08"
    try:
        login(driver, "performance_glitch_user", "secret_sauce")
        for sort_option in ["az", "za", "lohi", "hilo"]:
            verify_sorting(driver, sort_option)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: Sorting is broken!")
        raise

def test_error_user_product_filtering(driver):
    test_name = "FP_09"
    try:
        login(driver, "error_user", "secret_sauce")
        for sort_option in ["az", "za", "lohi", "hilo"]:
            verify_sorting(driver, sort_option)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: Sorting is broken!")
        raise

def test_visual_user_product_filtering(driver):
    test_name = "FP_10"
    try:
        login(driver, "visual_user", "secret_sauce")
        for sort_option in ["az", "za", "lohi", "hilo"]:
            verify_sorting(driver, sort_option)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: Sorting is broken!")
        raise

def test_standard_user_add_to_cart(driver):
    test_name = "FP_11"
    try:
        login(driver, "standard_user", "secret_sauce")
        reset_app_state(driver)
        add_all_items_to_cart(driver)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_problem_user_add_to_cart(driver):
    test_name = "FP_12"
    try:
        login(driver, "problem_user", "secret_sauce")
        reset_app_state(driver)
        add_all_items_to_cart(driver)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: Unable to add other items.")
        raise

def test_performance_glitch_user_add_to_cart(driver):
    test_name = "FP_13"
    try:
        login(driver, "performance_glitch_user", "secret_sauce")
        reset_app_state(driver)
        add_all_items_to_cart(driver)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_error_user_add_to_cart(driver):
    test_name = "FP_14"
    try:
        login(driver, "error_user", "secret_sauce")
        reset_app_state(driver)
        add_all_items_to_cart(driver)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: Unable to add other items.")
        raise

def test_visual_user_add_to_cart(driver):
    test_name = "FP_15"
    try:
        login(driver, "visual_user", "secret_sauce")
        reset_app_state(driver)
        add_all_items_to_cart(driver)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_standard_user_remove_from_products_page(driver):
    test_name = "FP_16"
    try:
        login(driver, "standard_user", "secret_sauce")
        reset_app_state(driver)
        add_all_items_to_cart(driver)
        remove_items_from_products_page(driver)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_problem_user_remove_from_products_page(driver):
    test_name = "FP_17"
    try:
        login(driver, "problem_user", "secret_sauce")
        reset_app_state(driver)
        add_all_items_to_cart(driver)
        remove_items_from_products_page(driver)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: Remove button on added items doesn't work.")
        raise

def test_performance_glitch_user_remove_from_products_page(driver):
    test_name = "FP_18"
    try:
        login(driver, "performance_glitch_user", "secret_sauce")
        reset_app_state(driver)
        add_all_items_to_cart(driver)
        remove_items_from_products_page(driver)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise

def test_error_user_remove_from_products_page(driver):
    test_name = "FP_19"
    try:
        login(driver, "error_user", "secret_sauce")
        reset_app_state(driver)
        add_all_items_to_cart(driver)
        remove_items_from_products_page(driver)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: Remove button on added items doesn't work.")
        raise

def test_visual_user_remove_from_products_page(driver):
    test_name = "FP_20"
    try:
        login(driver, "visual_user", "secret_sauce")
        reset_app_state(driver)
        add_all_items_to_cart(driver)
        remove_items_from_products_page(driver)
        write_result(test_name, "Pass")
    except Exception as e:
        write_result(test_name, f"Fail: {e}")
        raise
