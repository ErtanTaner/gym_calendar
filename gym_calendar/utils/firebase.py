import os
from firebase_admin import firestore, auth, initialize_app 

f_client = None

def init_firebase():
    if os.environ["LOCAL"] == "true":
        os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
        os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "localhost:9099"
    initialize_app()

def get_db():
    return firestore.client()

def get_auth():
    return auth
