import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from rest_framework.renderers import BaseRenderer
import json
from .signture import sign

AES_IV=b'whsbdhgntkgngmhk'
AES_SECRET_KEY=b'somerandomsecretsomerandomsecreg'

class CustomAesRenderer(BaseRenderer):
    media_type = 'application/octet-stream'
    format = 'aes'

    def render(self, data, media_type=None, renderer_context=None):
        data['ci']=list(sign(str(data)))
        plaintext = json.dumps(data)
        padded_plaintext = pad(plaintext.encode(), 16)
        cipher = AES.new(AES_SECRET_KEY, AES.MODE_CBC, AES_IV)
        ciphertext = cipher.encrypt(padded_plaintext)
        ciphertext_b64 = base64.b64encode(ciphertext).decode()
        return json.dumps(ciphertext_b64)
    
    
   
