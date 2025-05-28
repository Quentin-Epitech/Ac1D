def extract_id_from_url(url):
    parts = url.split("/")
    try:
        training_id = parts[parts.index("view") + 1]  # ID de la formation
        step_id = parts[parts.index("step") + 1].split("?")[0] if "step" in parts else None  # ID du step ou None
        print(f"Formation ID: {training_id}, Step ID: {step_id}")
        return training_id, step_id
    except ValueError as e:
        print(f"Erreur lors de l'extraction des IDs : {e}")
        return None, None