# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout

from ..serializers import UserSerializer, ChangePasswordSerializer
from ..models.user import User

class SignUp(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    def post(self, request):
        user = UserSerializer(data=request.data['credentials'])
        if user.is_valid():
            u = user.save()
            return Response(user.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

class SignIn(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request):
        creds = request.data['credentials']
        # We can pass our email and password along with the request to the
        # `authenticate` method. If we had used the default user, we would need
        # to send the `username` instead of `email`.
        user = authenticate(request, email=creds['email'], password=creds['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({
                    'id': user.id,
                    'email': user.email,
                    'token': user.get_auth_token(user)
                })
            else:
                return Response({ 'msg': 'The account is inactive.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({ 'msg': 'The username and/or password is incorrect.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class SignOut(generics.DestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def delete(self, request):
        # Remove this token from the user
        request.user.delete_token(request.user)
        # Logout will remove all session data
        logout(request)
        return Response({}, status=status.HTTP_200_OK)

class ChangePassword(generics.UpdateAPIView):
    permission_classes=(IsAuthenticated,)

    def partial_update(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data['passwords'])
        if serializer.is_valid():
            print(serializer)
            if not user.check_password(serializer.data['old']):
                return Response({ 'msg': 'Wrong password'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            # set_password will also hash the password
            user.set_password(serializer.data['new'])
            user.save()

            return Response({}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
