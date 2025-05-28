import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from save_formation import save_quiz_answers
from handlers.quiz_handler import handle_quiz
from response import answer_quiz
from star_rating_handler import handle_star_ratings

def load_json(json_file="content.json"):
    """
    Charge dynamiquement le fichier JSON pour s'assurer d'avoir les dernières modifications.
    """
    try:
        with open(json_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Fichier {json_file} introuvable. Création d'un nouveau.")
        return []

def check_step_exists_dynamic(training_id, step_id, json_file="content.json"):
    """
    Vérifie dynamiquement si une formation et un step existent dans le JSON.
    """
    content = load_json(json_file)
    for formation in content:
        if formation["formation"] == training_id:
            for step in formation["steps"]:
                if step["step_id"] == step_id:
                    return True, True
            return True, False
    return False, False

def handle_content(driver, training_id, step_id):
    try:
        # Priorité 1 : Bouton "Réessayer"
        retry_button = driver.find_elements(
            By.CSS_SELECTOR, ".btn.btn-rup-outline-primary.with-border.nav-bottom-previous.nav-change-step.mr-3.js-confirm-start-quiz-splash-screen"
        )
        if retry_button:
            print("Bouton 'Réessayer' détecté.")
            retry_button[0].click()
            time.sleep(2)
            return True

        # Priorité 2 : Bouton "Démarrer le quiz"
        start_quiz_button = driver.find_elements(
            By.CSS_SELECTOR, ".btn.btn-primary.pull-right.js-confirm-start-quiz-splash-screen"
        )
        if start_quiz_button:
            print("Bouton 'Démarrer le quiz' détecté.")

            # Vérifier dynamiquement si la formation et l'étape existent dans content.json
            formation_exists, step_exists = check_step_exists_dynamic(training_id, step_id)

            if formation_exists and step_exists:
                print(f"Les réponses pour la formation {training_id}, étape {step_id} existent déjà. Validation des réponses.")
                start_quiz_button[0].click()
                time.sleep(5)  # Attendre le chargement du quiz
                answer_quiz(driver, training_id, step_id)
                time.sleep(5)  # Valider directement les réponses sauvegardées
                handle_star_ratings(driver)
                return True
            else:
                print(f"Les réponses pour la formation {training_id}, étape {step_id} n'existent pas. Gestion aléatoire des questions.")
                start_quiz_button[0].click()
                time.sleep(5)  # Attendre le chargement du quiz
                handle_quiz(driver, training_id, step_id)
                time.sleep(5)
                save_quiz_answers(driver, training_id, step_id)  # Gérer le quiz avec réponses aléatoires
                return True

        # Priorité 3 : Bouton "Commencer"
        start_button = driver.find_elements(
            By.CSS_SELECTOR, "a.btn.btn-primary.nav-button-start"
        )
        if start_button:
            print("Bouton 'Commencer' détecté.")
            start_button[0].click()
            time.sleep(2)
            return True

        # Priorité 4 : Bouton "Suivant"
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary.next.nav-bottom-next.nav-change-step.mr-0"))
            )
            # Vérifier si le bouton est activable
            if "disabled" not in next_button.get_attribute("class"):
                driver.execute_script("arguments[0].click();", next_button)
                print("Bouton 'Suivant' cliqué avec succès.")
                time.sleep(2)
                return True
            else:
                print("Le bouton 'Suivant' est désactivé ou non interactif.")
        except Exception as e:
            print(f"Erreur lors du clic sur le bouton 'Suivant' : {e}")

    except Exception as e:
        print(f"Erreur lors du traitement du contenu : {e}")

    # Retourner True pour indiquer que le contenu a été traité ou qu'il n'y avait rien à traiter
    return True