from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Génération de la clé privée CA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Sauvegarde clé privée
with open("ca_private.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Sauvegarde clé publique
public_key = private_key.public_key()
with open("ca_public.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print("Clés CA générées avec succès !")
