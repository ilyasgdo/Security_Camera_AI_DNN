# Face Detection Surveillance System

Ce projet est un système de surveillance en temps réel qui utilise la détection de visages avec OpenCV et l'envoi
d'alertes par e-mail via l'API Gmail. Il inclut également une interface web pour visualiser le flux vidéo et
contrôler la détection.

## Fonctionnalités

- **Détection de visages en temps réel** : Utilisation d'un modèle MobileNet-SSD pour détecter les visages.
- **Envoi d'alertes par e-mail** : Envoi d'un e-mail avec une capture d'écran lorsqu'un visage est détecté.
- **Interface web** : Visualisation du flux vidéo en direct via une page web protégée par mot de passe.
- **Contrôle de la détection** : Possibilité de démarrer et d'arrêter la détection via des boutons sur l'interface
web.

## Prérequis

- Python 3.7 ou supérieur
- Compte Google pour l'API Gmail
- Compte ngrok pour exposer l'application en ligne

## Installation

1. Clonez le dépôt :
   ```bash
git clone https://github.com/votre-utilisateur/votre-depot.git
```
2. Installez les dépendances :
   ```bash
pip install -r requirements.txt
```
3. Configurez l'API Gmail :
   * Allez sur Google Cloud Console.
   * Créez un projet et activez l'API Gmail.
   * Téléchargez le fichier credentials.json et placez-le dans le dossier src/helper.
4. Configurez ngrok :
   * Téléchargez et installez ngrok depuis ngrok.com.
   * Authentifiez ngrok avec votre compte :
     ```bash
ngrok authtoken votre_token_ngrok
```

## Utilisation

1. Démarrez l'application :
   ```bash
python main.py
```
2. Exposez l'application avec ngrok :
   ```bash
ngrok http 5000
```
3. Accédez à l'URL fournie par ngrok (par exemple, https://cod-patient-currently.ngrok-free.app).
4. Connectez-vous avec le nom d'utilisateur admin et le mot de passe motdepasse.
5. Utilisez les boutons "Démarrer la détection" et "Arrêter la détection" pour contrôler la détection.

## Structure du projet

- `src/` :
  - `helper/` : Contient les fichiers d'aide tels que l'API Gmail.
  - `face_detection_web.py` : Contient la logique de détection de visages et l'interface web.
  - `face_detection_DNN.py` : Contient le modèle MobileNet-SSD pour détecter les visages.
- `templates/` :
  - `index.html` : Page web pour visualiser le flux vidéo et contrôler la détection.
- `main.py` : Point d'entrée de l'application.
- `requirements.txt` : Fichier de requêtes pour instaler les dépendances du projet.

## Objectif

Le but de ce projet est de créer un système de surveillance intelligent capable de détecter les visages en temps
réel et d'envoyer des alertes par e-mail.