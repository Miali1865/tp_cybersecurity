from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Génération de la clé privée
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Sauvegarde de la clé privée
with open("user1_private.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Extraire et sauvegarder la clé publique
public_key = private_key.public_key()
with open("user1_public.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print("Clés générées avec succès !")
