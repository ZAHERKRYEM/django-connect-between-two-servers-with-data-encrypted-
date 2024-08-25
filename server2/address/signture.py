from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import  padding


def sign_data(data, private_key):
    signature = private_key.sign(
        data.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature

def sign(data):
    with open("private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
        backend=default_backend())

    signature_text = sign_data(data, private_key)
    return signature_text
