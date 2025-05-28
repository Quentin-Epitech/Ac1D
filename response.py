import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from star_rating_handler import handle_star_ratings


def answer_quiz(driver, training_id, step_id, json_file="content.json"):
    try:
        # Charger les données JSON
        print("Chargement des données JSON...")
        with open(json_file, "r") as f:
            content = json.load(f)

        # Trouver la formation et l'étape correspondantes
        quiz_data = None
        for formation in content:
            if formation["formation"] == training_id:
                for step in formation["steps"]:
                    if step["step_id"] == step_id:
                        quiz_data = step["quiz_data"]
                        break

        if not quiz_data:
            print("Aucune donnée trouvée pour cette formation et étape.")
            return False

        print("Données JSON chargées avec succès. Début du traitement des questions...")

        # Récupérer les questions sur la page
        questions = driver.find_elements(By.CLASS_NAME, "js-quiz")
        for question in questions:
            # Extraire le titre de la question
            question_title = question.find_element(By.CLASS_NAME, "question-title").text.strip()
            print(f"Question détectée : {question_title}")

            # Trouver les réponses correspondantes dans le JSON
            matching_question = next((q for q in quiz_data if q["question"] == question_title), None)
            if not matching_question:
                print(f"Aucune correspondance trouvée pour la question : {question_title}")
                continue

            print(f"Réponses trouvées dans le JSON : {matching_question['answers']}")

            # Identifier le type de question (multiple choice ou vrai/faux)
            question_type = question.find_element(By.CLASS_NAME, "js-questionType").get_attribute("value")
            if question_type == "multiplechoice":
                print("Type de question : Choix multiples.")
                options = question.find_elements(By.CLASS_NAME, "js-multiple-choice-option")
                for option in options:
                    option_text = option.text.strip()
                    if option_text in matching_question["answers"]:
                        option.click()
                        print(f"Réponse sélectionnée : {option_text}")

            elif question_type == "yesno":
                print("Type de question : Vrai/Faux.")
                options = question.find_elements(By.CLASS_NAME, "btn-rup-outline-dark")
                for option in options:
                    if option.text.strip() in matching_question["answers"]:
                        option.click()
                        print(f"Réponse sélectionnée : {option.text.strip()}")

            else:
                print(f"Type de question non pris en charge : {question_type}")

            # Pause aléatoire pour simuler un comportement humain
            time.sleep(1)

        # Cliquer sur le bouton "Valider"
        print("Validation des réponses...")
        validate_button = driver.find_element(By.CSS_SELECTOR, "button#validateQuiz.js-btn-validate-questions")
        if validate_button:
            validate_button.click()
            time.sleep(2)
            handle_star_ratings(driver)
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary.next.nav-bottom-next.nav-change-step.mr-0"))
            )
            time.sleep(120)
            if "disabled" not in next_button.get_attribute("class"):
                driver.execute_script("arguments[0].click();", next_button)
                print("Bouton 'Suivant' cliqué avec succès.")
                
            else:
                print("Le bouton 'Suivant' est désactivé ou non interactif.")
            print("Réponses validées avec succès.")
        else:
            print("Bouton 'Valider' introuvable.")

    except Exception as e:
        print(f"Erreur lors du traitement du quiz : {e}")
        return False

    return True