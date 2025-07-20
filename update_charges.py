
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Load Excel data
df = pd.read_excel("to_increase_price.xlsx")
df.fillna(0, inplace=True)

# Setup Chrome driver
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Login manually for CAPTCHA
driver.get("https://vashishtkunj.ayodhyada.in/admin/login")
input("🔐 After logging in manually and solving CAPTCHA, press ENTER to continue...")

# Map labels to form field IDs
label_to_id = {
    "Corner Plot (10%)": "extra_charge_for_corner",
    "Park Facing (5%)": "extra_charge_for_park_facing",
    "18 Meter or Wide (10%)": "extra_charge_for_wide_road"
}

# Process each registration number
for _, row in df.iterrows():
    reg_no = str(int(row["Registration Number"]))
    print(f"🔄 Processing: {reg_no}")
    
    driver.get("https://vashishtkunj.ayodhyada.in/admin/applicant-list-to-set-extra-charges")
    time.sleep(2)
    
    try:
        # Search visually (Ctrl+F replacement)
        page_source = driver.page_source
        if reg_no not in page_source:
            print(f"❌ Registration number {reg_no} not found on page.")
            continue
        
        # Locate button by XPath using reg_no context
        button_xpath = f"//td[contains(text(), '{reg_no}')]/following-sibling::td//a[contains(text(), 'Set Extra Charges')]"
        set_button = driver.find_element(By.XPATH, button_xpath)
        set_button.click()
        time.sleep(2)

        # Fill the form based on Excel columns
        for label, field_id in label_to_id.items():
            value = row.get(label, 0)
            try:
                input_field = driver.find_element(By.ID, field_id)
                input_field.clear()
                input_field.send_keys(str(int(value)))
            except Exception as e:
                print(f"⚠️ Could not fill '{label}' for {reg_no}: {e}")

        # Submit the form
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print(f"✅ Submitted for {reg_no}")
        time.sleep(2)

    except Exception as e:
        print(f"❌ Error with {reg_no}: {e}")

driver.quit()
