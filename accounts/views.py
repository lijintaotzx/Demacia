# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lib.common_lib import CommonResponse
from lib.csrf_disable import CsrfExemptSessionAuthentication
from .serializers import UserSerializer, LoginSerializer, UserpeofileSerializer

# Create your views here.


comm = CommonResponse()

#用户注册
class AccountsViews(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self,request):
        s = UserSerializer(data=request.POST)
        if s.is_valid():
            User.objects.create_user(username=s.validated_data.get('username'), password=s.validated_data.get('password1'))
            return Response(comm.success({'username':s.validated_data.get('username'),
                                                      'password':s.validated_data.get('password1')},
                                                       'User Register'),
                                                        status = status.HTTP_201_CREATED)
        else:
            return Response(comm.error(s.errors,'User Register'),status = status.HTTP_400_BAD_REQUEST)


#用户登录
class LoginViews(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self,request):
        s = LoginSerializer(data=request.POST)
        if s.is_valid():
            username = s.validated_data['username']
            password = s.validated_data['password']
            user = auth.authenticate(username=username,password=password)
            if user:
                auth.login(request,user)
                return Response(comm.success(s.validated_data,'User Login'),status=status.HTTP_200_OK)
            return Response(comm.error('user password not exit!','User Login'),status=status.HTTP_400_BAD_REQUEST)
        return Response(s.errors)


#用户注销
class LogoutViews(APIView):

    # authentication_classes = (authentication.TokenAuthentication,)

    def get(self,request):
        auth.logout(request)
        return Response(comm.success({'logout is ok!'},'Logout'),status=status.HTTP_200_OK)


#用户信息相关
class UserprofileViews(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        print request.user.id
        return Response(123)

    def put(self,request):
        user = get_object_or_404(User,id=request.user.id)
        print type(request.POST)
        print type(request.FILES)
        s = UserpeofileSerializer(user.userprofile,data=request.POST)
        if s.is_valid():
            s.save()
            img = UserpeofileSerializer(user.userprofile, data=request.FILES)
            if img.is_valid():
                img.save()
            return Response(comm.success(s.data,'Userprofile put success!'),status=status.HTTP_200_OK)
        return Response(comm.error(s.errors, 'Userprofile put error!'),status=status.HTTP_400_BAD_REQUEST)


