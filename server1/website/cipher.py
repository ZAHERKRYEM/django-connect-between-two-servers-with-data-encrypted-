from Crypto.Cipher import AES
import base64
from Crypto.Util.Padding import unpad
import json
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

###################### ###########################
def verify_signature(signature_text, data,public_key):
    try:
        public_key.verify(
            signature_text,
            data.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    
######################     ###########################
    
def decryption(data):
    with open("public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(
        f.read(),
        backend=default_backend())
    key =b'somerandomsecretsomerandomsecreg'
    iv =b'whsbdhgntkgngmhk'
    mode = AES.MODE_CBC
    cipher = AES.new(key, mode, iv)
    enc = base64.b64decode(data)
    decrypted_data = unpad(cipher.decrypt(enc),16)
    decrypted_data = json.loads(decrypted_data)
    values = {key: value for key, value in decrypted_data.items() if key != "ci"}
    verify=verify_signature(bytes(decrypted_data['ci']),str(values) , public_key)
    return values,verify
       
       
