import os
import firebase_admin
from firebase_admin import credentials, auth

if not firebase_admin._apps:
    path = os.getenv("FIREBASE_KEY_PATH", "firebase_key.json")
    cred = credentials.Certificate(path)
    firebase_admin.initialize_app(cred)
