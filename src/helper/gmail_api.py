# gmail_api.py
import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Portée d'autorisation nécessaire pour envoyer des e-mails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    """Authentifie l'utilisateur et renvoie le service Gmail."""
    creds = None
    # Chemin vers le fichier credentials.json
    credentials_path = r"C:\Users\ilyas\PycharmProjects\facecounter\src\helper\credentials.json"
    token_path = r"C:\Users\ilyas\PycharmProjects\facecounter\src\helper\token.json"

    # Vérifie si un token d'authentification existe déjà
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # Si aucune authentification valide n'est trouvée, demande à l'utilisateur de se connecter
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # URI de redirection autorisé
            redirect_uri = "http://localhost:8080/"
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path,
                scopes=SCOPES,
                redirect_uri=redirect_uri
            )
            creds = flow.run_local_server(port=8080)  # Utilisez le même port que dans l'URI de redirection
        # Sauvegarde le token pour les utilisations futures
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, body, image_path=None):
    """Crée un message MIME pour l'e-mail."""
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    # Ajoute le corps du message
    message.attach(MIMEText(body, 'plain'))

    # Ajoute l'image en pièce jointe si elle est fournie
    if image_path:
        with open(image_path, 'rb') as f:
            img_data = f.read()
        image = MIMEImage(img_data, name=os.path.basename(image_path))
        message.attach(image)

    # Encode le message en base64
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def send_email(service, sender, to, subject, body, image_path=None):
    """Envoie un e-mail via l'API Gmail."""
    message = create_message(sender, to, subject, body, image_path)
    try:
        message = service.users().messages().send(userId='me', body=message).execute()
        print(f"E-mail envoyé avec succès ! Message ID: {message['id']}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")