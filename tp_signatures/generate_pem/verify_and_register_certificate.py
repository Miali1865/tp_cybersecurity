import json
import base64
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

REGISTRY_FILE = "registry.json"
certificate_file = "user1_certificate.json"

# Charger certificat
with open(certificate_file, "r") as f:
    cert = json.load(f)

username = cert["username"]
public_key_pem = cert["public_key"].encode()
signature = base64.b64decode(cert["CA_signature"])

# Charger clé publique CA
with open("ca_public.pem", "rb") as f:
    ca_public_key = serialization.load_pem_public_key(
        f.read(),
        backend=default_backend()
    )

# Recalculer le hash
data_to_hash = username.encode() + public_key_pem
digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
digest.update(data_to_hash)
hash_value = digest.finalize()

try:
    # Vérifier la signature
    ca_public_key.verify(
        signature,
        hash_value,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Certificat VALIDE ✅. Ajout au registre...")

    # Charger registre
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, "r") as f:
            registry = json.load(f)
    else:
        registry = {}

    registry[username] = cert["public_key"]

    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=4)

    print("Clé publique ajoutée au registre avec succès.")
except Exception as e:
    print(f"Certificat INVALIDE ❌ : {str(e)}")
