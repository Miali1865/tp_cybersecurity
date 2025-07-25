from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Génération clé privée de l'attaquant
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Sauvegarde clé privée
with open("attacker_private.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Sauvegarde clé publique
public_key = private_key.public_key()
with open("attacker_public.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print("Clés de l'attaquant générées avec succès.")
