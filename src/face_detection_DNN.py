# face_detection_web.py
import cv2
import time
from flask import Flask, Response, render_template, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from src.helper.gmail_api import authenticate_gmail, send_email

# Initialiser Flask
app = Flask(__name__)
auth = HTTPBasicAuth()

# Mot de passe pour protéger la page web
users = {
    "admin": generate_password_hash("ilyasgdo")  # Remplacez "motdepasse" par votre mot de passe
}

# Variable globale pour gérer l'état de la détection
detection_active = True

# Vérifier le mot de passe
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

# Route pour la page d'accueil protégée
@app.route('/')
@auth.login_required
def index():
    return render_template('index.html')

# Route pour démarrer la détection
@app.route('/start_detection')
@auth.login_required
def start_detection():
    global detection_active
    detection_active = True
    return jsonify({"status": "Détection démarrée"})

# Route pour arrêter la détection
@app.route('/stop_detection')
@auth.login_required
def stop_detection():
    global detection_active
    detection_active = False
    return jsonify({"status": "Détection arrêtée"})

# Générer les frames vidéo en temps réel
def generate_frames():
    # Charger le modèle MobileNet-SSD
    model_file = r"C:\Users\ilyas\PycharmProjects\facecounter\src\deploy.prototxt"
    weights_file = r"C:\Users\ilyas\PycharmProjects\facecounter\src\res10_300x300_ssd_iter_140000.caffemodel"
    net = cv2.dnn.readNetFromCaffe(model_file, weights_file)

    # Initialiser la capture vidéo
    cap = cv2.VideoCapture(0)

    # Variables pour mesurer le temps de visibilité
    start_time = None
    total_time = 0

    # Variable pour éviter les envois multiples d'e-mails
    last_email_time = 0
    email_cooldown = 60  # Délai de 60 secondes entre deux e-mails

    # Authentifier Gmail
    service = authenticate_gmail()
    sender_email = "youreemail@gmail.com"  # Remplacez par votre adresse Gmail
    recipient_email = "youreemail@gmail.com"  # Remplacez par l'adresse du destinataire

    while True:
        # Lire une frame de la vidéo
        ret, frame = cap.read()
        if not ret:
            break

        # Obtenir les dimensions de la frame
        (h, w) = frame.shape[:2]

        # Préparer l'image pour le modèle DNN
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], swapRB=False, crop=False)
        net.setInput(blob)
        detections = net.forward()

        # Vérifier si un visage est détecté
        face_detected = False

        # Parcourir les détections
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]  # Score de confiance

            # Filtrer les détections faibles (seuil de confiance > 0.5)
            if confidence > 0.5:
                face_detected = True

                # Calculer les coordonnées de la boîte englobante
                box = detections[0, 0, i, 3:7] * [w, h, w, h]
                (startX, startY, endX, endY) = box.astype("int")

                # Dessiner la boîte englobante et afficher le score de confiance
                cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 2)
                text = f"Visage: {confidence * 100:.2f}%"
                cv2.putText(frame, text, (startX, startY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Gestion du temps de visibilité
        if face_detected and detection_active:
            if start_time is None:
                start_time = time.time()
        else:
            if start_time is not None:
                end_time = time.time()
                total_time += end_time - start_time
                start_time = None

        # Afficher le temps total de visibilité
        cv2.putText(frame, f"Temps visible: {total_time:.2f} secondes", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Envoyer un e-mail si un visage est détecté et que le délai est respecté
        if face_detected and detection_active and (time.time() - last_email_time > email_cooldown):
            # Sauvegarder l'image capturée
            image_path = "detected_face.jpg"
            cv2.imwrite(image_path, frame)

            # Envoyer l'e-mail via l'API Gmail
            send_email(service, sender_email, recipient_email, "Alerte : Visage détecté !", "Un visage a été détecté. Voici l'image capturée.", image_path)
            last_email_time = time.time()

        # Convertir la frame en format JPEG pour la diffusion
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Renvoyer la frame au client
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # Libérer la capture vidéo
    cap.release()

# Route pour la diffusion vidéo
@app.route('/video_feed')
@auth.login_required
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Fonction pour démarrer le serveur Flask
def start_flask_app():
    app.run(host='127.168.1.5', port=5000, debug=True)
