from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken


# Create your views here.
@api_view(['POST'])
def register_user(request : Request):

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = User.objects.create_user(username, email, password)
        user.save()
    except Exception as error:
        return Response({"msg" : "Couldn't Create user", "error" : error})

    return Response({"msg" : "User Created Successfuly"}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
def login_user(request : Request):

    username_from_client = request.data.get("username")
    password_from_client = request.data.get("password")

    user = authenticate(request, username=username_from_client, password=password_from_client)

    if user is None:
        return Response({"msg" : "user not found. Please check your credentials"}, status=status.HTTP_403_FORBIDDEN)
    
    token = AccessToken.for_user(user)

    return Response({"msg" : "user is authenticated successfully!", "token" : str(token)})


@api_view(['POST'])
def change_password(request : Request):
    
    username_from_client = request.data.get("username")
    new_password = request.data.get("new_password")
    
    try:
        user = User.objects.get(username=username_from_client)
        user.set_password(new_password)
        user.save()
    except Exception as error:
        return Response({"msg" : "chamging password failed", "error" : error})
    
    return Response({"msg" : "changed password successfully"})
        
        