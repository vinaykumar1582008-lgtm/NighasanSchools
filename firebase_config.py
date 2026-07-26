import os
import json
import firebase_admin
from firebase_admin import credentials, auth

if not firebase_admin._apps:
    if "FIREBASE_KEY" in os.environ:
        cred_dict = json.loads(os.environ["FIREBASE_KEY"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)

    elif os.path.exists("firebase_key.json"):
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)

    else:
        print("Firebase key not found. Firebase OTP disabled.")
