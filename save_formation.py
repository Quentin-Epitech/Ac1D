from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

def save_quiz_answers(driver, training_id, step_id):
    print(f"Début de la sauvegarde des réponses pour Training ID: {training_id}, Step ID: {step_id}")
    
    try:
        # Cliquer sur le bouton "Voir la correction"
        print("Recherche du bouton 'Voir la correction'...")
        try:
            correction_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-primary.mr-3.js-see-selected-score"))
            )
            driver.execute_script("arguments[0].click();", correction_button)
            print("Bouton 'Voir la correction' cliqué avec succès.")
            time.sleep(2)  # Attendre que la correction s'affiche
        except Exception as e:
            print(f"Erreur lors du clic sur le bouton 'Voir la correction': {e}")
            return False
        # Attendre que les questions soient visibles
        print("Attente du chargement des questions...")
        questions_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "questions"))
        )
        print("Questions trouvées.")
        
        # Récupérer toutes les questions
        questions = questions_container.find_elements(By.CLASS_NAME, "quiz-item")
        print(f"Nombre de questions trouvées : {len(questions)}")
        
        quiz_data = []
        
        for idx, question in enumerate(questions, start=1):
            print(f"Traitement de la question {idx}...")
            
            # Récupérer le titre de la question
            question_title = question.find_element(By.CLASS_NAME, "question-title").text
            print(f"Titre de la question : {question_title}")
            
            # Vérifier si c'est une question vrai/faux
            true_false_buttons = question.find_elements(By.CLASS_NAME, "btn-group")
            
            answers = []
            if true_false_buttons:
                print("Question détectée comme étant de type Vrai/Faux.")
                
                # Boutons Vrai et Faux
                true_button = question.find_element(By.CSS_SELECTOR, "button:first-child")
                false_button = question.find_element(By.CSS_SELECTOR, "button:last-child")
                
                if "active" in true_button.get_attribute("class"):
                    answers = ["Vrai"]
                    print("Réponse : Vrai")
                else:
                    answers = ["Faux"]
                    print("Réponse : Faux")
            else:
                print("Question détectée comme étant de type Choix multiples.")
                
                # Question à choix multiples
                correct_answers = question.find_elements(By.CLASS_NAME, "list-group-item-success")
                answers = [answer.text for answer in correct_answers]
                print(f"Réponses correctes trouvées : {answers}")
            
            quiz_data.append({
                "question": question_title,
                "answers": answers
            })
        
        # Charger le fichier JSON existant
        print("Chargement du fichier content.json...")
        with open("content.json", "r") as f:
            content = json.load(f)
        
        # Recherche ou ajout de la formation et de l'étape
        print("Recherche de la formation et de l'étape correspondantes...")
        formation_found = False
        for formation in content:
            if formation["formation"] == training_id:
                formation_found = True
                step_found = False
                for step in formation["steps"]:
                    if step["step_id"] == step_id:
                        print(f"Étape trouvée : {step_id}. Mise à jour des données.")
                        step["quiz_data"] = quiz_data
                        step_found = True
                        break
                if not step_found:
                    print(f"Étape non trouvée. Ajout de l'étape {step_id}.")
                    formation["steps"].append({
                        "step_id": step_id,
                        "quiz_data": quiz_data
                    })
                break
        
        if not formation_found:
            print(f"Formation non trouvée. Ajout de la formation {training_id} avec l'étape {step_id}.")
            content.append({
                "formation": training_id,
                "steps": [{
                    "step_id": step_id,
                    "quiz_data": quiz_data
                }]
            })
        
        # Sauvegarder les modifications
        print("Sauvegarde des réponses dans content.json...")
        with open("content.json", "w") as f:
            json.dump(content, f, indent=4)
        print("Sauvegarde terminée avec succès.")
        # Cliquer sur le bouton "Fermer"
        close_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary[onclick='window.location.reload()']")
        close_button.click()
        time.sleep(2)  # Attendre que la fenêtre se ferme
        return True
        
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des réponses du quiz : {e}")
        return False