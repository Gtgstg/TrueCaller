from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authentication import get_authorization_header,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from .serializers import *

class Spam(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        name = request.data.get('name', None)
        phone = request.data.get('phone', None)
        email = request.data.get('email', None)
        a = Contact.objects.filter(phone=phone).first()
        b = UserProfile.objects.filter(phone=phone).first()
        #check if it is already registered then we insert it's original name.
        if (b):
            spam = Spam(
                name=b.name,
                phone=phone,
                email=b.email
            )
            spam.save()
        elif(a):
            spam = Spam(
                name=a.name,
                phone=phone,
                email=a.email
            )
            spam.save()

        else:
            spam = Spam(
                name=name,
                phone=phone,
                email=email
            )
            spam.save()
        return Response(json.dumps({'message': "Contact marked as spam"}),status=status.HTTP_200_OK)

class Contacts(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contacts = Contact.objects
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        token = get_authorization_header(request).split()[1].decode("utf-8")
        name = request.data.get('name', None)
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)
        contact = Contact(
            name=name,
            phone=phone,
            email=email
        )
        contact.save()
        UserContactMapping(
            user=Token.objects.get(key=token).user,
            contact=contact
        ).save()

        return Response(json.dumps({'msg': 'Contact saved successfully','data': request.data}))


class Signup(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)

        user = User(
            username=username,
            password=password,
            email=email
        )

        user.set_password(password)
        user.save()

        UserProfile(
            user=user,
            phone=phone
        ).save()

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(token,status=status.HTTP_200_OK)
        else:
            return Response(json.dumps({'Error': "Error in signup"}),status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if (authenticate(username=username, password=password)):
            user = User.objects.get(username=username)
        else:
            return Response(json.dumps({'Error': "Invalid username/password"}, status=status.HTTP_400_BAD_REQUEST))
        if user:
            token, _ = Token.objects.get_or_create(user=user)

            return Response(token,status=status.HTTP_200_OK)
        else:
            return Response(json.dumps({'Error': "Invalid credentials"}),status=status.HTTP_400_BAD_REQUEST)


class SearchByName(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        name = request.data.get('name', None)
        print(name)
        a = Contact.objects.filter(name__startswith=name)
        a1 = User.objects.filter(username__startswith=name)
        a2= Spam.objects.filter(name__startswith=name)
        b = Contact.objects.filter(name__contains=name).exclude(name__startswith=name)
        b1 = User.objects.filter(username__contains=name).exclude(username__startswith=name)
        b2 = Spam.objects.filter(name__contains=name).exclude(name__startswith=name)
        unique=set()
        response = {"Spam":[],"Normal":[]}
        for contact in a2:
            if contact.phone in unique:
                continue
            unique.add(contact.phone)
            response["Spam"].append({
                'name': contact.name,
                'phone': contact.phone
            })
        for contact in a:
            if contact.phone in unique:
                continue
            unique.add(contact.phone)
            response["Normal"].append({
                'name': contact.name,
                'phone': contact.phone
            })
        for contact in a1:
            profile=UserProfile.objects.filter(user=contact).first()
            if profile.phone in unique:
                continue
            unique.add(profile.phone)
            response["Normal"].append({
                'name': contact.username,
                'phone': profile.phone
            })
        for contact in b2:
            if contact.phone in unique:
                continue
            unique.add(contact.phone)
            response["Spam"].append({
                'name': contact.name,
                'phone': contact.phone
            })
        for contact in b:
            if contact.phone in unique:
                continue
            unique.add(contact.phone)
            response["Normal"].append({
                'name': contact.name,
                'phone': contact.phone
            })
        for contact in b1:
            profile = UserProfile.objects.filter(user=contact).first()
            if contact.phone in unique:
                continue
            unique.add(profile.phone)
            response["Normal"].append({
                'name': contact.username,
                'phone': profile.phone
            })

        return Response(response,status=status.HTTP_200_OK)

class SearchByPhone(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        phone = request.data.get('phone', None)
        token = get_authorization_header(request).split()[1].decode("utf-8")
        user=Token.objects.get(key=token).user
        profile = UserProfile.objects.filter(phone=phone)

        if (profile):
            spam = Spam.objects.filter(phone=phone).first()
            response = {"Spam": [], "Normal": []}
            if spam:
                response["Spam"].append({
                    'name': spam.name,
                    'phone': spam.phone,
                    'email': spam.email
                })
            else:
                userprof=Token.objects.get(key=token).user
                response["Normal"].append({
                    'name': userprof.username,
                    'phone': phone,
                    'email': userprof.email
                })
            return Response(response,status=status.HTTP_200_OK)
        else:
            contacts = Contact.objects.filter(phone=phone)
            spam = Spam.objects.filter(phone=phone)
            response = {"Spam":[],"Normal":[]}
            unique=set()
            for contact in spam:
                if contact.phone in unique:
                    continue
                unique.add(contact.phone)
                userMap = UserContactMapping.objects.filter(user=contact, contact=user)
                if (userMap):
                    response["Spam"].append({
                        'name': contact.name,
                        'phone': contact.phone,
                        'email': contact.email
                    })
                else:
                    response["Spam"].append({
                        'name': contact.name,
                        'phone': contact.phone
                    })
            for contact in contacts:
                if contact.phone in unique:
                    continue
                unique.add(contact.phone)
                userMap=UserProfile.objects.filter(phone=contact.phone).first()
                if(userMap):
                    x = UserContactMapping.objects.filter(user=userMap.user,
                                                          contact=user).first()
                    if(x):
                        response["Normal"].append({
                            'name': contact.name,
                            'phone': contact.phone,
                            'email': contact.email
                        })
                    else:
                        response["Normal"].append({
                            'name': contact.name,
                            'phone': contact.phone
                        })
                else:
                    response["Normal"].append({
                        'name': contact.name,
                        'phone': contact.phone
                    })
            return Response(response,status=status.HTTP_200_OK)