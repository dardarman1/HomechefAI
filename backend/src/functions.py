from firebase_config import get_db

db = get_db

# chatgpt_key refers to the ChatGPT API key
def store_user_data(user_id, name, chatgpt_key):
    doc_ref = db.collection('users').document(user_id)
    user_data = {
        'name': name,
        'chatgpt_key': chatgpt_key
    }
    try:
        doc_ref.set(user_data)
    except Exception as e:
        return -1
    return 0

def get_user_data(user_id):
    doc_ref = db.collection('users').document(user_id)
    try:
        doc = doc_ref.get()
        return doc.to_dict()
    except Exception as e:
        return -1