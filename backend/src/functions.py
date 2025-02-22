from firebase_config import get_db

db = get_db

# api_key refers to the Gemini API key
def store_api_key(api_key):
    """
    _safely stores the api_key_

    Args:
        api_key (_str_): _the gemini api_key being used_

    Returns:
        _int_: _returns the int 0 if success, -1 if it fails_
    """
    doc_ref = db.collection('api_keys').document('gemini')
    data = {
        'api_key': api_key
    }
    try:
        doc_ref.set(data)
    except Exception as e:
        return -1
    return 0

def get_api_key():
    """
    Retrieves the Gemini API key from the database

    Returns:
        _int_: _returns the int -1 if error_
        _dict_: _returns the dictionary containing the API key_
    """
    doc_ref = db.collection('api_keys').document('gemini')
    try:
        doc = doc_ref.get()
        
        if not getattr(doc, 'exists', False):
            return -1
        return doc.to_dict()
    except Exception as e:
        return -1