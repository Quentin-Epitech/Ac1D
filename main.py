import json
from selenium import webdriver
from auth import authenticate
from content_handler import handle_content
from utils import extract_id_from_url
import time
# Configuration du navigateur
driver = webdriver.Chrome()

try:
    # Étape 1 : Authentification
    authenticate(driver)

    # Étape 2 : Surveiller l'URL
    print("Veuillez naviguer vers une formation.")
    while True:
        current_url = driver.current_url
        if "/Training/view/" in current_url:
            training_id, step_id = extract_id_from_url(current_url)
            print(f"Formation ID: {training_id}, Step ID: {step_id}")

            # Appeler handle_content et continuer la boucle
            success = handle_content(driver, training_id, step_id)
            if success:
                print("Étape traitée avec succès. Passage à l'étape suivante...")
                time.sleep(2)  # Attendre avant de surveiller la prochaine URL
            else:
                print("Erreur lors du traitement de l'étape. Tentative de récupération...")
                time.sleep(5)

except Exception as e:
    print(f"Une erreur s'est produite : {e}")
finally:
    print("Appuyez sur Entrée pour fermer le navigateur.")
    input()
    driver.quit()