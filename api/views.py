from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from kyykka.models import User, Team
from kyykka.serializers import *


@api_view(['GET'])
def user_list(request):
    """
    List all users.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)

# class UserDetail(APIView):
#     def get(self, request, format=None):
#

@api_view(['GET'])
def user_detail(request, pk):
    """
    Retrieve a user.
    """
    try:
        user = User.objects.prefetch_related('throw_set').get(pk=pk)
        # user = UserSerializer.setup_eager_loading(user)
        # user = user.prefetch_related('throw_set')
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)


@api_view(['GET'])
def team_list(request):
    """
    List all teams.
    """
    if request.method == 'GET':
        teams = Team.objects.all()
        serializer = TeamPlayerSerializer(teams, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def team_detail(request, pk):
    """
    Retrieve a team.
    """
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TeamPlayerSerializer(team)
        return Response(serializer.data)
