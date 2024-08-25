import requests
import time
from cryptography.hazmat.primitives import  serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import  padding
import base64

auth_url = "http://127.0.0.1:8000/api/token/"
refresh_url = "http://127.0.0.1:8000/api/token/refresh/"
key="http://127.0.0.1:8000/key/"

public_key=None
access_token = None
refresh_token = None
access_token_expiration_time = None
refresh_token_expiration_time = None

######################     ###########################

def orderkey():
    global public_key
    response = requests.get(key)
    public_key = serialization.load_pem_public_key(
            response.content,
            backend=default_backend())
    return public_key

######################        ###########################

def get_access_token():
    global access_token, refresh_token, access_token_expiration_time,refresh_token_expiration_time,public_key
    public_key=orderkey()
    data = {
        
        "username":base64.b64encode(public_key.encrypt('admin'.encode(),padding.PKCS1v15())).decode('utf-8') ,
        "password":base64.b64encode( public_key.encrypt('1234'.encode(),padding.PKCS1v15())).decode('utf-8')
    }
    response = requests.post(auth_url, data=data)
    if response.status_code == 200:
        data = response.json()
        access_token = data['access']
        refresh_token = data['refresh']
        access_token_expiration_time = time.time() 
        refresh_token_expiration_time = time.time() 
        return access_token

    else:
        return None

######################        ###########################

def refresh_access_token():
    global access_token, refresh_token, access_token_expiration_time

    data = {
        "refresh": refresh_token,
    }

    response = requests.post(refresh_url, data=data)

    if response.status_code == 200:
        data = response.json()
        access_token = data['access']
        access_token_expiration_time = time.time() 
        return access_token

    else:
        return None

######################         ###########################

def is_access_token_expired():
    if time.time() - access_token_expiration_time >=600: # 10 minutes
        return True
    else:
        return False

def is_refresh_token_expired():
    if time.time() - refresh_token_expiration_time >=1200: #20 minutes
        return True
    else:
        return False


######################          ###########################

def token():
    global access_token, access_token_expiration_time 
    if access_token is None :
        access_token = get_access_token()
    elif is_access_token_expired() == True:
        access_token = refresh_access_token()
        if access_token is None:
            access_token = get_access_token()
    elif is_refresh_token_expired() == True:
        access_token=get_access_token()
        if access_token is None:
            access_token = get_access_token()
    return access_token



