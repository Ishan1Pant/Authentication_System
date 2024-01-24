from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import MyUserSerializer,LoginSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer


# Create your views here.

class userRegisterView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer=MyUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg':'Success'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class userLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                return Response({"msg":"login Successfull"},status=status.HTTP_200_OK)
            else:
                return Response({"Errors":{"Non_field_errors":["Invalid Useraname of Password"]}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
