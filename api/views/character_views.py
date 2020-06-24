from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.character import Character
from ..serializers import CharacterSerializer, UserSerializer

# Create your views here.
class Characters(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request):
        """Index request"""
        # characters = Character.objects.all()
        characters = Character.objects.filter(owner=request.user.id)
        data = CharacterSerializer(characters, many=True).data
        return Response(data)

    serializer_class = CharacterSerializer
    def post(self, request):
        """Create request"""
        # Add user to request object
        request.data['character']['owner'] = request.user.id
        # Serialize/create character
        character = CharacterSerializer(data=request.data['character'])
        if character.is_valid():
            m = character.save()
            return Response(character.data, status=status.HTTP_201_CREATED)
        else:
            return Response(character.errors, status=status.HTTP_400_BAD_REQUEST)

class CharacterDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        character = get_object_or_404(Character, pk=pk)
        data = CharacterSerializer(character).data
        # Only want to show owned characters?
        # if not request.user.id == data['owner']:
        #     raise PermissionDenied('Unauthorized, you do not own this character')
        return Response(data)

    def delete(self, request, pk):
        """Delete request"""
        character = get_object_or_404(Character, pk=pk)
        if not request.user == character.owner:
            raise PermissionDenied('Unauthorized, you do not own this character')
        character.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        if request.data['character'].get('owner', False):
            del request.data['character']['owner']

        # Locate Character
        character = get_object_or_404(Character, pk=pk)
        # Check if user is  the same
        if not request.user == character.owner:
            raise PermissionDenied('Unauthorized, you do not own this character')

        # Add owner to data object now that we know this user owns the resource
        request.data['character']['owner'] = request.user.id
        # Validate updates with serializer
        ms = CharacterSerializer(character, data=request.data['character'])
        if ms.is_valid():
            ms.save()
            print(ms)
            return Response(ms.data)
        return Response(ms.errors, status=status.HTTP_400_BAD_REQUEST)
