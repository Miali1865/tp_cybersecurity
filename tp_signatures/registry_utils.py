import json
import os

REGISTRY_FILE = "registry.json"

def load_registry():
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_registry(registry):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=4)

def register_user_in_registry(username, public_key_pem):
    registry = load_registry()
    registry[username] = public_key_pem
    save_registry(registry)
    print(f"{username} enregistré avec succès.")

