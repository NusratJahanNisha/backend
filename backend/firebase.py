import firebase_admin
from firebase_admin import firestore, credentials

if not firebase_admin._apps:
    cred = credentials.Certificate("./serviceAccountKey.json")
    firebase_admin.initialize_app(cred) #this initializes a firebase app so that we can use firebase and its packages 

db = firestore.client() 