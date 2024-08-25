
from rest_framework import generics,status
from rest_framework.response import Response
from django.http import HttpResponse
from .models import PersonalData
from .serializers import PersonalDataSerializer
from .renderers import CustomAesRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView,InvalidToken, TokenError,Request
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import  serialization
from rest_framework.response import Response  
from rest_framework import status  
import base64

######################    ###########################

class PersonalDataView(generics.RetrieveAPIView):
    renderer_classes = [CustomAesRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request,national_id):
        try:
            address = PersonalData.objects.get(national_id=national_id)
            serializer = PersonalDataSerializer(address)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        except PersonalData.DoesNotExist:
            return Response({"error": "PersonalData not found"}, status=status.HTTP_404_NOT_FOUND)


######################     ###########################

def generater(request):
    global private_key
    private_key=rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
    )
    public_key=private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return HttpResponse(public_key_pem, content_type='application/octet-stream')


######################           ###########################

class MyTokenObtainPairView(TokenObtainPairView):

    def post(self, request: Request, *args, **kwargs) -> Response:
        global private_key
        data={
            'username':private_key.decrypt(base64.b64decode(request.data['username']),padding.PKCS1v15()).decode(),
            'password':private_key.decrypt(base64.b64decode(request.data['password']),padding.PKCS1v15()).decode()
            }
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
