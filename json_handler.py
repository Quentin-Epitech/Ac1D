import json
import os

# Charger les données JSON existantes ou initialiser une structure vide
def load_json():
    if os.path.exists("content.json"):
        with open("content.json", "r") as json_file:
            return {item["formation"]: item for item in json.load(json_file)}
    return {}

training_data = load_json()

def save_step(training_id, step_id, content_type, duration=None):
    step_data = {
        "step_id": step_id,
        "type": content_type,
        "duration": duration if duration else None,
    }

    if training_id not in training_data:
        training_data[training_id] = {"formation": training_id, "steps": []}

    # Ajouter l'étape uniquement si elle n'existe pas déjà
    existing_steps = {step["step_id"]: step for step in training_data[training_id]["steps"]}
    if step_id not in existing_steps:
        training_data[training_id]["steps"].append(step_data)
        print(f"Nouvelle étape ajoutée : {step_data}")

    # Sauvegarder dans le fichier JSON
    with open("content.json", "w") as json_file:
        json.dump(list(training_data.values()), json_file, indent=4)

def is_step_processed(training_id, step_id):
    return training_id in training_data and any(step["step_id"] == step_id for step in training_data[training_id]["steps"])

def check_step_exists(training_id, step_id):

    formation_exists = training_id in training_data
    step_exists = False
    
    if formation_exists:
        step_exists = any(
            step["step_id"] == step_id 
            for step in training_data[training_id]["steps"]
        )
        
    return formation_exists, step_exists
