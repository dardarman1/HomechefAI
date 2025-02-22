import os
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not service_account_path:
        raise ValueError('GOOGLE_APPLICATION_CREDENTIALS environment variable is not set')
    
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)
    
    db = firestore.client()