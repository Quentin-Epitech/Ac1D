import time
import random
from selenium.webdriver.common.by import By

def handle_star_ratings(driver):
    try:
        print("Détection des questions évaluatives (étoiles)...")
        # Récupérer les questions évaluatives sur la page
        questions = driver.find_elements(By.CLASS_NAME, "js-survey")
        if not questions:
            print("Aucune question évaluative trouvée.")
            return False

        for index, question in enumerate(questions, start=1):
            try:
                # Extraire le titre de la question
                question_title = question.find_element(By.CLASS_NAME, "question-title").text.strip()
                print(f"Traitement de la question {index}: {question_title}")

                # Sélectionner une note aléatoire entre 1 et 10
                random_score = random.randint(1, 10)
                print(f"Note sélectionnée pour la question '{question_title}': {random_score}")

                # Trouver l'étoile correspondant à la note et cliquer dessus
                star_element = question.find_element(By.CSS_SELECTOR, f".js-star-score[data-score='{random_score}']")
                driver.execute_script("arguments[0].click();", star_element)
                time.sleep(1)  # Pause pour simuler un comportement humain

            except Exception as e:
                print(f"Erreur lors du traitement de la question {index}: {e}")

        # Cliquer sur le bouton "Valider" après avoir répondu à toutes les questions
        print("Validation des réponses...")
        validate_button = driver.find_element(By.ID, "validateSurvey")
        if validate_button:
            driver.execute_script("arguments[0].click();", validate_button)
            print("Réponses validées avec succès.")
        else:
            print("Bouton 'Valider' introuvable.")

    except Exception as e:
        print(f"Erreur lors du traitement des évaluations : {e}")
        return False

    return True