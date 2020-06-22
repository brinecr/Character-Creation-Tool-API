from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.mango import Mango
from ..serializers import MangoSerializer, UserSerializer

# Create your views here.
class Mangos(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request):
        """Index request"""
        # mangos = Mango.objects.all()
        mangos = Mango.objects.filter(owner=request.user.id)
        data = MangoSerializer(mangos, many=True).data
        return Response(data)

    serializer_class = MangoSerializer
    def post(self, request):
        """Create request"""
        # Add user to request object
        request.data['mango']['owner'] = request.user.id
        # Serialize/create mango
        mango = MangoSerializer(data=request.data['mango'])
        if mango.is_valid():
            m = mango.save()
            return Response(mango.data, status=status.HTTP_201_CREATED)
        else:
            return Response(mango.errors, status=status.HTTP_400_BAD_REQUEST)

class MangoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        mango = get_object_or_404(Mango, pk=pk)
        data = MangoSerializer(mango).data
        # Only want to show owned mangos?
        # if not request.user.id == data['owner']:
        #     raise PermissionDenied('Unauthorized, you do not own this mango')
        return Response(data)

    def delete(self, request, pk):
        """Delete request"""
        mango = get_object_or_404(Mango, pk=pk)
        if not request.user.id == mango['owner']:
            raise PermissionDenied('Unauthorized, you do not own this mango')
        mango.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        if request.data['mango'].get('owner', False):
            del request.data['mango']['owner']

        # Locate Mango
        mango = get_object_or_404(Mango, pk=pk)
        # Check if user is  the same
        if not request.user.id == mango['owner']:
            raise PermissionDenied('Unauthorized, you do not own this mango')

        # Add owner to data object now that we know this user owns the resource
        request.data['mango']['owner'] = request.user.id
        # Validate updates with serializer
        ms = MangoSerializer(mango, data=request.data['mango'])
        if ms.is_valid():
            ms.save()
            print(ms)
            return Response(ms.data)
        return Response(ms.errors, status=status.HTTP_400_BAD_REQUEST)
