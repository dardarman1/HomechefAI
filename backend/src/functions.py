from google.cloud import secretmanager


def get_api_key() -> str:
    """
    Retrieves the Gemini API key from the database

    Returns:
        _NONE_: _returns None if fails_
        _str_: _returns _the api_key if success_
    """
    project_id = 'glassy-acolyte-451801-t4'
    secret_id = "GEMINI_API"
    version_id = "lateest"
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    
    try:
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(request={"name": secret_name})
        gemini_api_key = response.payload.data.decode('UTF-8')
        print("{gemini_api_key}")
        return gemini_api_key
    
    except Exception as e:
        return None
    print("debug")
    global db
    doc_ref = db.collection('api_keys').document('gemini')
    try:
        doc = doc_ref.get()
        
        if not getattr(doc, 'exists', False):
            return None
        return doc.to_dict()['api_key']
    except Exception as e:
        return None