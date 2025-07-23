# tp_cybersecurity

# 📜 TP – Signatures électroniques et Autorité de Certification simulée

## 🎯 Objectif général

Mettre en œuvre une **application Django** simple de **signatures électroniques** permettant de :

✅ Générer des paires de clés RSA  
✅ Simuler une autorité (CA) qui enregistre les clés publiques  
✅ Signer des fichiers `.txt`  
✅ Vérifier les signatures  
✅ Comprendre l’intérêt d’une infrastructure de confiance (PKI)  
✅ Simuler une attaque MITM  
✅ Simuler l'utilisation de certificats signés par la CA

---

## 🛠️ Technologies utilisées

- **Python 3**
- **Django**
- **Cryptography** (bibliothèque pour RSA, SHA-256)

---

## 📌 Plan complet étape par étape

### ✅ **1. Préparation de l'environnement**

- Installer Python 3 et pip :
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip python3-venv
    ```
- Créer un dossier `tp_signatures` :
    ```bash
    mkdir tp_signatures
    cd tp_signatures
    ```
- Créer et activer un environnement virtuel :
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
- Installer Django et Cryptography :
    ```bash
    pip install django cryptography
    ```

---

### ✅ **2. Création du projet Django**

- Créer le projet :
    ```bash
    django-admin startproject signaturesproject .
    ```
- Créer l'application :
    ```bash
    python manage.py startapp signaturesapp
    ```
- Ajouter `'signaturesapp'` dans `INSTALLED_APPS` de `settings.py`.
- Configurer `urls.py` :
    ```python
    from django.contrib import admin
    from django.urls import path
    from signaturesapp import views

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.home, name='home'),
        path('register/', views.register_user, name='register_user'),
        path('sign/', views.sign_file, name='sign_file'),
        path('verify/', views.verify_signature, name='verify_signature'),
    ]
    ```

---

### ✅ **3. Création des clés RSA utilisateur**

- Créer `generate_keys.py` :
    - Génère `user1_private.pem` et `user1_public.pem` (clé privée et publique utilisateur).
    - Utilise `cryptography` pour `RSA 2048 bits`.
    - Exécution :
        ```bash
        python generate_keys.py
        ```

---

### ✅ **4. Création de l'autorité de certification simulée (CA)**

- Créer `generate_ca_keys.py` :
    - Génère `ca_private.pem` et `ca_public.pem` (clé privée et publique CA).
    - Exécution :
        ```bash
        python generate_ca_keys.py
        ```

---

### ✅ **5. Page `/register/`**

- Permet à l’utilisateur d’uploader sa clé publique (`user1_public.pem`).
- La clé est ajoutée dans `registry.json` de forme :
    ```json
    {
        "user1": "-----BEGIN PUBLIC KEY----- ... -----END PUBLIC KEY-----"
    }
    ```
- Vue Django prête permettant l'upload et l'enregistrement sécurisé de la clé publique.

---

### ✅ **6. Page `/sign/`**

- L'utilisateur choisit :
    - Son `username`.
    - Le fichier `.txt` à signer.
- Le système :
    - Calcule le hash SHA-256.
    - Signe avec `user1_private.pem`.
    - Renvoie :
        - `document.sig` (signature binaire).
        - `document_signature.json` (signature en base64 + metadata : user, timestamp, signature).

---

### ✅ **7. Page `/verify/`**

- L'utilisateur fournit :
    - `username`.
    - Fichier `.txt`.
    - Fichier `document.sig`.
- Le système :
    - Charge la clé publique dans `registry.json`.
    - Calcule le hash du fichier.
    - Vérifie la signature.
    - Affiche :
        - ✅ Signature VALIDE.
        - ❌ Signature INVALIDE.

---

### ✅ **8. Simulation MITM**

- Génération de clés de l'attaquant via `generate_attacker_keys.py`.
- Remplacement de la clé publique de `user1` par celle de l’attaquant dans `registry.json`.
- L'attaquant signe un fichier avec `attacker_private.pem`.
- Le système `/verify/` valide **faussement** la signature car il utilise le registre naïf.
- **Permet de démontrer la vulnérabilité sans certificat.**

---

### ✅ **9. BONUS - Utilisation d'un certificat signé par la CA**

- Génération d'un certificat :
    ```json
    {
        "username": "user1",
        "public_key": "-----BEGIN PUBLIC KEY----- ...",
        "CA_signature": "base64..."
    }
    ```
- La CA signe le hash de `(username + public_key)` avec sa clé privée.
- Avant ajout dans `registry.json`, le système vérifie :
    - La signature CA est valide avec `ca_public.pem`.
- Si la signature est valide, la clé publique est ajoutée au registre.
- **Empêche l’attaque MITM** car l’attaquant ne peut pas générer un certificat valide.

---

## ❓ Questions théoriques résolues

✅ **Pourquoi la clé privée doit-elle rester secrète ?**  
Elle est utilisée pour signer ; si elle est volée, quelqu’un peut se faire passer pour toi.

✅ **Pourquoi signe-t-on le hash et pas tout le fichier directement ?**  
Signer le hash est plus rapide, léger et sécurisé, le hash représentant de manière unique le contenu du fichier.

✅ **Quelles informations doit-on vérifier en plus du hash ?**  
- Timestamp
- Identité de l’utilisateur
- Intégrité de la clé publique

✅ **Différence entre registre naïf et certificat CA :**  
- **Registre naïf :** vulnérable aux remplacements de clés.  
- **Certificat CA :** le certificat signé prouve l’authenticité de la clé publique, empêchant les attaques MITM.

---

## 📦 Fichiers fournis / attendus pour remise

✅ `user1_private.pem`  
✅ `user1_public.pem`  
✅ `ca_private.pem`, `ca_public.pem`  
✅ `attacker_private.pem`, `attacker_public.pem`  
✅ `registry.json`  
✅ `document.txt`, `document.sig`, `document_signature.json`  
✅ `signaturesproject/` Django complet  
✅ Scripts de génération de clés et certificats  
✅ README.md (ce fichier)

---

## 🏁 Résultat final

✅ Compréhension **théorique et pratique** des signatures électroniques.  
✅ Capacité à signer, vérifier, gérer des clés, simuler MITM et comprendre les PKI.  
✅ **Projet Django fonctionnel pour démonstration.**

---

## 🚀 Exécution

1️⃣ Activer l'environnement :
```bash
source venv/bin/activate
