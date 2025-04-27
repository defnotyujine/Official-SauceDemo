from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

test_cases = {
    "SSM_01": "standard_user",
     "SSM_02": "problem_user",
     "SSM_03": "performance_glitch_user",
     "SSM_04": "error_user",
     "SSM_05": "visual_user",
}
password = "secret_sauce"
timeout_duration = 900 
results_file = os.path.expanduser("~/Official-SauceDemo/Security/Compiled/Results/SessionTimeout.txt")
os.makedirs(os.path.dirname(results_file), exist_ok=True)

with open(results_file, "w") as f:
    f.write("Session Timeout Test Results:\n\n")

    for test_id, user in test_cases.items():
        print(f"\nTesting session timeout for Test Case ID: {test_id} ({user})")
        f.write(f"Test Case ID: {test_id} ({user})\n")

        try:
            driver = webdriver.Firefox()
        except Exception as e:
            print(f"Error setting up Firefox driver: {e}")
            print("Make sure geckodriver is installed and in your system's PATH.")
            f.write(f"Error setting up Firefox driver: {e}\n")
            f.write("Make sure geckodriver is installed and in your system's PATH.\n")
            continue

        driver.get("https://www.saucedemo.com")

        # Login
        driver.find_element(By.ID, "user-name").send_keys(user)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()

        print(f"Logged in as {user}. Waiting {timeout_duration} seconds to simulate inactivity...")
        f.write(f"Logged in as {user}. Waiting {timeout_duration} seconds to simulate inactivity...\n")
        time.sleep(timeout_duration)

        driver.get("https://www.saucedemo.com/cart.html")
        time.sleep(2)

        current_url = driver.current_url
        if "saucedemo.com" in current_url and "/cart.html" not in current_url:
            result = "[PASS] Session expired. Redirected to: " + current_url
            print(result)
            f.write(f"{test_id}: {result}\n")
        else:
            result = "[FAIL] Session still active. Current URL: " + current_url
            print(result)
            f.write(f"{test_id}: {result}\n")

        driver.quit()

print(f"\nSession timeout testing complete. Results saved to: {results_file}")