from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from rest_framework import viewsets

from profile_api import models

from rest_framework.authentication import TokenAuthentication

from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.settings import api_settings

from profile_api import permissions

from rest_framework import filters

from django.shortcuts import render

import tweepy

from profile_api import serializers

class HelloApiView(APIView):
    """Test API View"""
    serializer_class=serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""

        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})
    
    def post(self, request):
        """Create a hello message with our name"""
        serializer=self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name=serializer.validated_data.get('name')
            message=f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                            )
        
    def put(self, request, pk=None):
        """Handle updating an object"""

        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle partial update of object"""

        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""

        return Response({'method': 'DELETE'})
    
class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class=serializers.HelloSerializer

    def list(self, request):
        """Return a hello message."""

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLS using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})
    
    def create(self, request):
        """Create a new hello message."""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""

        return Response({'http_method': 'DELETE'})
    
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating, creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class UserLoginApiView(ObtainAuthToken):
   """Handle creating user authentication tokens"""
   renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES    

def fetch_tweets(request):
    # Twitter API credentials
    consumer_key = 'XYDeFd0WTHXQHxvdhHMAPdWTM'
    consumer_secret = 'GCdnP2o8Isd4fQmILyazRlW6e9Dr8azwWD0ZH8LPG0oslsYNOC'
    access_token = '1403750537183383552-9IT0ZTzHcjDgqMXuDVRurd5wFNCoAG'
    access_token_secret = '3PnxiqLxTK6PvQ28YnQ9oc62BQi71y2slkNQE3lzQNuCp'

    # Authenticate to Twitter API
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    # Fetch tweets from two public accounts (example: 10 tweets from each account)
    tweets = api.home_timeline(count=10)
    # account1_tweets = api.user_timeline(screen_name='Virat Kohli', count=10)
    # account2_tweets = api.user_timeline(screen_name='Sachin Tendulkar', count=10)

    # Combine tweets from both accounts
    tweets = account1_tweets + account2_tweets

    # Render the tweets in a template
    return render(request, 'tweets.html', {'tweets': tweets})
