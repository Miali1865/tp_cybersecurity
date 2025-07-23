import base64
import json
from datetime import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

username = "user1"

# Charger clé privée de l'attaquant
with open("attacker_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
        backend=default_backend()
    )

# Lire le fichier à signer
with open("tp_signature.txt", "rb") as f:
    data = f.read()

# Calculer hash
digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
digest.update(data)
hash_value = digest.finalize()

# Signer le hash
signature = private_key.sign(
    hash_value,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Sauvegarder signature binaire
with open("document.sig", "wb") as f:
    f.write(signature)

# Sauvegarder signature + metadata JSON
metadata = {
    "user": username,
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "signature": base64.b64encode(signature).decode()
}
with open("document_signature.json", "w") as f:
    json.dump(metadata, f, indent=4)

print("Fichier signé avec succès par l'attaquant.")
