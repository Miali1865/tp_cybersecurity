import json
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

username = "user1"

# Charger clé publique utilisateur
with open(f"{username}_public.pem", "rb") as f:
    public_key_pem = f.read()

# Charger clé privée CA
with open("ca_private.pem", "rb") as f:
    ca_private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
        backend=default_backend()
    )

# Calculer le hash de (username + clé_publique)
data_to_hash = username.encode() + public_key_pem
digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
digest.update(data_to_hash)
hash_value = digest.finalize()

# Signer le hash avec la clé privée CA
signature = ca_private_key.sign(
    hash_value,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Créer le certificat
certificate = {
    "username": username,
    "public_key": public_key_pem.decode(),
    "CA_signature": base64.b64encode(signature).decode()
}

# Sauvegarder le certificat
with open(f"{username}_certificate.json", "w") as f:
    json.dump(certificate, f, indent=4)

print(f"Certificat pour {username} généré avec succès !")
