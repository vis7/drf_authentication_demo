import json

from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail 
from rest_framework.response import Response
from rest_framework import status, authentication, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Customer
from .serializers import CustomerSerializer


class RegisterAPI(generics.GenericAPIView):
    serializer_class = CustomerSerializer

    def post(self, request, *args, **kwargs):
        data = {}
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            account.is_active = True
            account.save()
            token = Token.objects.get_or_create(user=account)[0].key
            data["message"] = "user registered successfully"
            data["email"] = account.email
            data["username"] = account.username
            data["token"] = token
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = {}
        request_body = json.loads(request.body)
        username = request_body['username']
        password = request_body['password']
        try:
            user = Customer.objects.get(username=username)
        except BaseException as e:
            return Response({"message":"Invalid username"}, status=status.HTTP_400_BAD_REQUEST)

        token = Token.objects.get_or_create(user=user)[0].key
        print(token)
        if not check_password(password, user.password):
            return Response({"message": "Incorrect login credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if user:
            if user.is_active:
                print(request.user)
                login(request, user)
                data["message"] = "user logged in"
                data["email_address"] = user.email
                response = {"data": data, "token": token}
                return Response(response)
            else:
                return Response({"message":"Account not active"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Account doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPI(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'User Logged out successfully'}, status=status.HTTP_200_OK)

class CustomerAPIView(APIView):
    serializer_class = CustomerSerializer

    def patch(self, request, pk, *args, **kwargs):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# reset password
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )

