import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from json_handler import save_step

def register_and_handle(driver, training_id, step_id):
    """
    Détecte dynamiquement le type de contenu et met à jour le JSON.
    """
    try:
        # Vérifier la présence du bouton "Faire un autre essai"
        retry_quiz_buttons = driver.find_elements(By.CSS_SELECTOR, 
            "a.btn.btn-rup-outline-primary.with-border.nav-bottom-previous.nav-change-step.mr-3.js-confirm-start-quiz-splash-screen")
        if retry_quiz_buttons:
            print("Bouton 'Faire un autre essai' détecté.")
            retry_quiz_buttons[0].click()
            time.sleep(2)  # Attendre après le clic
            return True  # Étape traitée

        # Vérifier la présence du bouton "Démarrer le quiz"
        if driver.find_elements(By.CLASS_NAME, "js-confirm-start-quiz-splash-screen"):
            print("Contenu détecté : Bouton 'Démarrer le quiz'.")
            save_step(training_id, step_id, "quiz")
            return True

        # Vérifier la présence d'une vidéo YouTube
        youtube_video = driver.find_elements(By.CSS_SELECTOR, "iframe[src*='youtube.com']")
        if youtube_video:
            print("Contenu détecté : Vidéo YouTube.")
            save_step(training_id, step_id, "video")
            return True

        # Vérifier la présence d'un contenu texte
        print("Contenu détecté : Texte.")
        save_step(training_id, step_id, "text")
        return True

    except Exception as e:
        print(f"Erreur lors de la tentative de détection : {e}")
        return False