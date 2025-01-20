from src.face_detection_DNN import start_flask_app



def main():
# Démarrer le serveur Flask
    start_flask_app()


if __name__ == "__main__":
    main()

#ngrok http --url=cod-patient-currently.ngrok-free.app http://127.168.1.5:5000/ --basic-auth ""