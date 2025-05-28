from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import EMAIL, PASSWORD, BASE_URL

def setup_driver():
    return webdriver.Chrome()

def authenticate(driver):
    driver.get(BASE_URL)
    print("Connexion en cours...")

    # Cliquer sur "Se connecter avec Microsoft"
    sso_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "have-sso-account"))
    )
    sso_button.click()

    # Remplir les champs de connexion
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "loginfmt"))
    )
    email_field.send_keys(EMAIL)
    email_field.send_keys(Keys.RETURN)

    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "passwd"))
    )
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)

    print("Veuillez terminer la vérification manuelle et appuyez sur Entrée.")
    input()
    print("Connexion réussie.")