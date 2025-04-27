import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import logging

log_file_path = os.path.expanduser("~/Official-SauceDemo/Usability/Compiled/log.txt")
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
logging.basicConfig(filename=log_file_path, level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

baseline_colors = {}
standard_fonts = []

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Firefox()
    logging.info("Initialized Firefox WebDriver")
    yield driver
    driver.quit()
    logging.info("Closed WebDriver session")

def login(driver, username, password):
    logging.info(f"Logging in as: {username}")
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").clear()
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
    logging.info(f"{username} successfully logged in")

def write_result(test_id, result, message=""):
    filepath = os.path.expanduser("~/Official-SauceDemo/Usability/Compiled/Results/UIColorFont.txt")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "a") as f:
        if message:
            f.write(f"{test_id}: {result} - {message}\n")
        else:
            f.write(f"{test_id}: {result}\n")
    logging.info(f"Result for {test_id}: {result} {message}")

def get_ui_colors(driver):
    try:
        header = driver.find_element(By.CLASS_NAME, "header_secondary_container")
        footer = driver.find_element(By.TAG_NAME, "footer")
        buttons = driver.find_elements(By.CLASS_NAME, "btn")
        product_titles = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        product_descriptions = driver.find_elements(By.CLASS_NAME, "inventory_item_desc")

        button_color = buttons[0].value_of_css_property("background-color") if buttons else None
        button_text_color = buttons[0].value_of_css_property("color") if buttons else None
        title_color = product_titles[0].value_of_css_property("color") if product_titles else None
        desc_color = product_descriptions[0].value_of_css_property("color") if product_descriptions else None

        return {
            "header_bg": header.value_of_css_property("background-color"),
            "footer_bg": footer.value_of_css_property("background-color"),
            "button_bg": button_color,
            "button_text": button_text_color,
            "product_title": title_color,
            "product_description": desc_color
        }

    except Exception as e:
        logging.warning(f"Failed to get extended UI colors: {e}")
        return {
            "header_bg": None,
            "footer_bg": None,
            "button_bg": None,
            "button_text": None,
            "product_title": None,
            "product_description": None
        }


@pytest.mark.parametrize("username,test_id", [
    ("standard_user", "UUI_01"),
    ("problem_user", "UUI_02"),
    ("performance_glitch_user", "UUI_03"),
    ("error_user", "UUI_04"),
    ("visual_user", "UUI_05")
])
def test_ui_color_comparison(driver, username, test_id):
    global baseline_colors
    try:
        login(driver, username, "secret_sauce")

        try:
            navigate_to_pages(driver)
        except Exception as nav_error:
            message = f"Error: Other parts of the website are not accessible!"
            write_result(test_id, "Fail", message)
            pytest.fail(message)

        current_colors = get_ui_colors(driver)

        if username == "standard_user":
            baseline_colors = current_colors
            write_result(test_id, "Pass")
        else:
            result = "Pass"
            for key in baseline_colors:
                if current_colors.get(key) != baseline_colors.get(key):
                    result = "Fail"
                    break
            write_result(test_id, result)

    except Exception as e:
        logging.error(f"Exception in UI color test for {username}: {e}")
        write_result(test_id, "Fail", "Unexpected error during test")

@pytest.mark.parametrize("username,test_id", [
    ("standard_user", "UUI_06"),
    ("problem_user", "UUI_07"),
    ("performance_glitch_user", "UUI_08"),
    ("error_user", "UUI_09"),
    ("visual_user", "UUI_10")
])
def test_font_consistency(driver, username, test_id):
    global standard_fonts

    try:
        login(driver, username, "secret_sauce")

        try:
            navigate_to_pages(driver)
        except Exception as nav_error:
            message = f"Error: Other parts of the website are not accessible!"
            write_result(test_id, "Fail", message)
            pytest.fail(message)


        if username == "standard_user":
            standard_fonts = extract_fonts_from_all_pages(driver)
            write_result(test_id, "Pass")
            return

        test_fonts = extract_fonts_from_all_pages(driver)

        mismatches = 0
        for i, font in enumerate(test_fonts):
            if i < len(standard_fonts) and font != standard_fonts[i]:
                mismatches += 1

        result = "Fail" if mismatches > 0 else "Pass"
        write_result(test_id, result)

    except Exception as e:
        logging.error(f"Exception in font consistency test for {username}: {e}")
        write_result(test_id, "Fail", "Unexpected error during test")


def navigate_to_pages(driver):
    pages = []
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver, 10).until(EC.url_contains("cart.html"))

    driver.find_element(By.ID, "checkout").click()
    WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-one.html"))

    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()

    WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-two.html"))
    driver.find_element(By.ID, "finish").click()

    WebDriverWait(driver, 10).until(EC.url_contains("checkout-complete.html"))
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "bm-menu")))

def extract_fonts_from_all_pages(driver):
    fonts = []

    fonts.extend(get_fonts_from_current_page(driver))  # Products
    navigate_to_cart(driver)
    fonts.extend(get_fonts_from_current_page(driver))

    navigate_to_checkout_info(driver)
    fonts.extend(get_fonts_from_current_page(driver))

    navigate_to_checkout_overview(driver)
    fonts.extend(get_fonts_from_current_page(driver))

    navigate_to_checkout_complete(driver)
    fonts.extend(get_fonts_from_current_page(driver))

    expand_sidebar(driver)
    fonts.extend(get_fonts_from_current_page(driver))

    return fonts

def get_fonts_from_current_page(driver):
    elements = driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //p | //span | //button | //label | //a")
    return [get_font_properties(e) for e in elements if e.text.strip()]

def get_font_properties(element):
    return {
        "font-family": element.value_of_css_property("font-family"),
        "font-size": element.value_of_css_property("font-size")
    }

def navigate_to_cart(driver):
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver, 10).until(EC.url_contains("cart.html"))

def navigate_to_checkout_info(driver):
    navigate_to_cart(driver)
    driver.find_element(By.ID, "checkout").click()
    WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-one.html"))

def navigate_to_checkout_overview(driver):
    navigate_to_checkout_info(driver)
    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()
    WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-two.html"))

def navigate_to_checkout_complete(driver):
    navigate_to_checkout_overview(driver)
    driver.find_element(By.ID, "finish").click()
    WebDriverWait(driver, 10).until(EC.url_contains("checkout-complete.html"))

def expand_sidebar(driver):
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "bm-menu")))
