from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import MyUserSerializer,LoginSerializer,ProfileSerializer,ChangePassSerializer,ResetSerializer,FinalSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.

#Create Tokens
def get_tokens(user):
    refresh =RefreshToken.for_user(user)
    return{
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }

class userRegisterView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer=MyUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens(user)
            return Response({'token':token,'msg':'Success'},status=status.HTTP_201_CREATED)
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
                token=get_tokens(user)
                return Response({"token":token,"msg":"login Successfull"},status=status.HTTP_200_OK)
            else:
                return Response({"errors":{"Non_field_errors":["Invalid Useraname of Password"]}},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        serializer=ProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ChangePassView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post (self,request):
        serializer=ChangePassSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password Change Successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class SendEmailView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer=ResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"msg":"Password Reset Link sent successfully. Please check your Email"},status=status.HTTP_200_OK)
    
class ResetPassView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token):
        serializer=FinalSerializer(data=request.data,context={"uid":uid,"token":token})
        serializer.is_valid(raise_exception=True)
        return Response({"msg":"Password Changed Successfully"},status=status.HTTP_200_OK)