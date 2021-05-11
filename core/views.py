from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken

from .models import Link


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST', 'GET', 'DELETE', 'PUT'])
def links(request):
    if request.method=='POST':
        data = {}
        status_code = 201

        user = request.user
        link = Link.objects.create(
            user=user,
            text=request.data['text'],
            url=request.data['url']
        )

        return Response(data, status_code)

    elif request.method=='GET':
        status_code = 200

        user_links = Link.objects.filter(user=request.user)

        data = {'links': []}
    
        for link_model in user_links:
            link = {
                'id': link_model.id,
                'text': link_model.text,
                'url': link_model.url
            }

            data['links'].append(link)

        return Response(data, status_code)
    
    elif request.method=='DELETE':
        status_code = 200

        link_id = request.data['id']

        Link.objects.get(id=link_id).delete()

        return Response({}, status_code)

    elif request.method=='PUT':
        link = Link.objects.get(id=request.data['id'])
        link.text = request.data['text']
        link.url=request.data['url']
        link.save()

        return Response()






class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
