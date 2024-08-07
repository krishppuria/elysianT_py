from utils.respone import errorResponse, successResponse
from .models import Account
from rest_framework.decorators import api_view
from . import serializers
from rest_framework import status
from config.jwtToken import get_tokens, verify_token, dataWithObjectId
import bcrypt
from datetime import datetime
from bson import ObjectId
from django.core.mail import send_mail
from django.template.loader import render_to_string
import requests
import os

# ----------------------------------------------------------------
# signup user
# ----------------------------------------------------------------

@api_view(['POST'])
def signup(request):
    try:

        email = request.data.get('email')

        # Email Already Exists
        email_already = Account.get(email.lower())
        if (email_already):
            return errorResponse("The email provided already exists.Please use a different email.")

        serializer = serializers.CandidateSignUp(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = bcrypt.hashpw(
                serializer.validated_data['password'].encode('utf-8'),
                bcrypt.gensalt()
            )
            serializer.validated_data['email'] = serializer.validated_data['email'].lower()
            user = Account.create(serializer.validated_data)
            data = get_tokens(user)
            url = os.environ.get('welcome_msg_url')
            response_message = requests.get(url)
            response = response_message.json()
            return successResponse(data, response['data'])
        return errorResponse(list(serializer.errors.values())[0][0])
    except Exception as e:
        return errorResponse("Some error occured!! Please try again")

