from django.shortcuts import render
from django.http import HttpResponse
from registry_utils import register_user_in_registry
import os
import base64
import json
from datetime import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

def home(request):
    return HttpResponse("Bienvenue sur le TP des signatures électroniques.")

def register_user(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        public_key_file = request.FILES.get("public_key_file")
        if username and public_key_file:
            try:
                # Lire le contenu de la clé publique uploadée
                public_key_pem = public_key_file.read().decode('utf-8')
                # Enregistrer dans le registre
                register_user_in_registry(username, public_key_pem)
                message = f"Clé publique de {username} enregistrée avec succès."
            except Exception as e:
                message = f"Erreur lors de l'enregistrement : {str(e)}"
        else:
            message = "Veuillez fournir un nom d'utilisateur et un fichier .pem."

    return render(request, "signaturesapp/register.html", {"message": message})

def sign_file(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        txt_file = request.FILES.get("txt_file")
        if username and txt_file:
            try:
                # Lire le contenu du fichier texte
                txt_content = txt_file.read()

                # Calculer le hash SHA-256
                digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
                digest.update(txt_content)
                hash_value = digest.finalize()

                # Charger la clé privée de l'utilisateur
                private_key_path = f"{username}_private.pem"
                if not os.path.exists(private_key_path):
                    message = f"Clé privée {private_key_path} non trouvée."
                    return render(request, "signaturesapp/sign.html", {"message": message})

                with open(private_key_path, "rb") as key_file:
                    private_key = serialization.load_pem_private_key(
                        key_file.read(),
                        password=None,
                        backend=default_backend()
                    )

                # Signer le hash
                signature = private_key.sign(
                    hash_value,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )

                # Sauvegarder la signature dans un fichier .sig
                with open("document.sig", "wb") as sig_file:
                    sig_file.write(signature)

                # Sauvegarder signature + metadata dans un fichier JSON
                signature_json = {
                    "user": username,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "signature": base64.b64encode(signature).decode('utf-8')
                }

                with open("document_signature.json", "w") as json_file:
                    json.dump(signature_json, json_file, indent=4)

                message = "Fichier signé avec succès. Fichiers 'document.sig' et 'document_signature.json' générés."
            except Exception as e:
                message = f"Erreur lors de la signature : {str(e)}"
        else:
            message = "Veuillez fournir le nom d'utilisateur et un fichier .txt."
    return render(request, "signaturesapp/sign.html", {"message": message})

def verify_signature(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        txt_file = request.FILES.get("txt_file")
        sig_file = request.FILES.get("sig_file")
        if username and txt_file and sig_file:
            try:
                # Charger le registre et récupérer la clé publique
                if not os.path.exists("registry.json"):
                    message = "registry.json introuvable."
                    return render(request, "signaturesapp/verify.html", {"message": message})

                with open("registry.json", "r") as reg_file:
                    registry = json.load(reg_file)

                if username not in registry:
                    message = f"L'utilisateur {username} n'existe pas dans le registre."
                    return render(request, "signaturesapp/verify.html", {"message": message})

                public_key_pem = registry[username].encode()
                public_key = serialization.load_pem_public_key(
                    public_key_pem,
                    backend=default_backend()
                )

                # Lire le contenu du fichier texte
                txt_content = txt_file.read()

                # Calculer le hash SHA-256
                digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
                digest.update(txt_content)
                hash_value = digest.finalize()

                # Lire la signature
                signature = sig_file.read()

                # Vérifier la signature
                public_key.verify(
                    signature,
                    hash_value,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )

                message = "✅ Signature VALIDE."
            except Exception as e:
                message = f"❌ Signature INVALIDE ou erreur : {str(e)}"
        else:
            message = "Veuillez fournir le nom d'utilisateur, le fichier texte et le fichier signature."
    return render(request, "signaturesapp/verify.html", {"message": message})
