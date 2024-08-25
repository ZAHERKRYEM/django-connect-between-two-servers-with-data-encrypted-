
import requests
from .cipher import decryption
from .token import token
from django.http import HttpResponse

def personal(request,id):
    url='http://127.0.0.1:8000/personal/'+str(id)
    access_token=token()
    headers = {'Authorization': 'Bearer ' + access_token}
    response=requests.get(url, headers=headers)
    if response.status_code == 404:
        return HttpResponse('Notfound')
    personal_before=response.json()
    personal,verify=decryption(personal_before)
    if verify ==False:
        return HttpResponse('Man in the Middle')
    return HttpResponse(f'before : {personal_before}  \n  after : {personal}')

