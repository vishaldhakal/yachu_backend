from django.shortcuts import render
from .serializers import CustomUserSerializer
from .models import CustomUser
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
# Create your views here.

class CustomUserListCreateView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role')

        user = CustomUser.objects.create_user(username=username, password=password, email=email, role=role)
        user.save()
        return Response({'message': 'User created successfully'})


