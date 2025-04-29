# **Deployment Instructions for SauceDemo Automated Testing Project**

This document provides the necessary steps to deploy and replicate the **SauceDemo Automated Testing Project** on your local machine.

---

## **Prerequisites**

Before deploying the project locally, ensure that the following software is installed on your system:

1. **Python (3.x or higher)**
   - Python is required to run the test scripts.
   - To verify if Python is installed, run the following command in your terminal:
     ```bash
     python --version
     ```
   - If not installed, download Python from [https://www.python.org/downloads/](https://www.python.org/downloads/).

2. **Mozilla Firefox (Browser)**
   - The tests have been designed to run with **Mozilla Firefox**.
   - Download and install Firefox from [https://www.mozilla.org/firefox/](https://www.mozilla.org/firefox/).

3. **Geckodriver (for Firefox)**
   - Geckodriver is necessary for Selenium to interact with Firefox.
   - You can download it from [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases).
   - Make sure to add Geckodriver to your system’s PATH environment variable for ease of access.

4. **Git (Optional, for cloning the repository)**
   - Git allows you to clone the project repository if you haven’t downloaded it manually.
   - Install Git from [https://git-scm.com/downloads](https://git-scm.com/downloads).

---

## **Steps to Deploy the Project Locally**

Follow these steps to deploy the **SauceDemo Automated Testing Project** on your local machine:

### **1. Clone the Repository**
   - If you are using Git, clone the project repository to your local system's home directory:
     ```bash
     git clone https://github.com/defnotyujine/Official-SauceDemo.git
     ```

   - Alternatively, download the project as a ZIP file from the repository and extract it to your `home` folder.

### **2. Install Python Dependencies**
   - Navigate to the project directory:
     ```bash
     cd ~/Official-SauceDemo
     ```

   - Install the necessary Python libraries by running:
     ```bash
     pip install -r requirements.txt
     ```

     The `requirements.txt` file contains the necessary libraries, including Selenium, to execute the automated tests.

### **3. Configure Geckodriver**
   - Ensure that **Geckodriver** is installed and added to your system’s **PATH**.
     - On Linux, you can move the Geckodriver to `/usr/local/bin/`:
       ```bash
       sudo mv geckodriver /usr/local/bin/
       ```

### **4. Configure Your Browser (Optional)**
   - Ensure that **Mozilla Firefox** is installed on your machine.
   - Make sure that Firefox is up to date to avoid compatibility issues with Selenium WebDriver.

### **5. Run the Test Scripts**
   - Once the dependencies and configurations are in place, you can start running the test cases.
   - Navigate to the directory containing the test scripts and run the main test files:
     ```bash
    
     # For running all the test cases
     ./master.sh

---

## **Additional Notes**

- **Browser Compatibility**: The tests are currently optimized for **Mozilla Firefox**. Ensure that the correct browser is being used for test execution.


## **Optional Deployment Instructions for Windows**

If you are using a **Windows** operating system, follow these additional steps for deployment:

### **1. Install Python and Dependencies**
   - **Python Installation**: Install Python 3.x or higher from [Python’s official website](https://www.python.org/downloads/).
     - During installation, make sure to select the checkbox **"Add Python to PATH"**.
   - **Install Dependencies**: Open **Command Prompt** and navigate to the project directory:
     ```bash
     cd path\to\Official-SauceDemo
     ```
     Then, install the dependencies:
     ```bash
     pip install -r requirements.txt
     ```

### **2. Install Geckodriver**
   - **Download Geckodriver** from [Geckodriver Releases](https://github.com/mozilla/geckodriver/releases).
   - **Extract** the downloaded file and **move `geckodriver.exe`** to a folder on your system (e.g., `C:\geckodriver\`).
   - Add this folder to your **system's PATH**:
     - Right-click **This PC** > **Properties** > **Advanced system settings** > **Environment Variables**.
     - Under **System variables**, find **Path**, click **Edit**, and **add** the path where `geckodriver.exe` is located (e.g., `C:\geckodriver\`).

### **3. Run the Test Scripts**
   - Once all dependencies are installed, run the test scripts from **Command Prompt**:
     ```bash
     # For running all the test cases
     master.bat

     Note that `.bat` files can be used to automate the process on Windows for running tests.

---
