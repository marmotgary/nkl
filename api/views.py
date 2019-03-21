from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_swagger.views import get_swagger_view
from kyykka.models import User, Team
from kyykka.serializers import *

schema_view = get_swagger_view(title='Pastebin API')

class UserList(APIView):
    """
    Return all users.
    """
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)

class UserDetail(APIView):
    """
    Retrieve data of a single user.
    Used when inspecting a single player's page
    """
    def get_object(self, pk):
        try:
            user = User.objects.prefetch_related('throw_set').get(pk=pk)
            return user
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        season_id = request.query_params.get('season')

        serializer = UserDetailSerializer(user, context={'season_id' : season_id})
        return Response(serializer.data)

class TeamList(APIView):
    """
    Return all users.
    """
    def get(self, request, format=None):
        try:
            season_id = request.query_params.get('season')
            if season_id:
                season = Season.objects.get(id=season_id)
            else:
                raise Season.DoesNotExist
        except Season.DoesNotExist:
            season = CurrentSeason.objects.first().season
        teams = Team.objects.all()
        serializer = TeamListSerializer(teams, many=True, context={'season':season})
        return Response(serializer.data)

class TeamDetail(APIView):
    """
    Retrieve data of a single user.
    Used when inspecting a single player's page
    """
    def get_object(self, pk):
        try:
            team = Team.objects.get(pk=pk)
            return team
        except Team.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        try:
            season_id = request.query_params.get('season')
            if season_id:
                season = Season.objects.get(id=season_id)
            else:
                raise Season.DoesNotExist
        except Season.DoesNotExist:
            season = CurrentSeason.objects.first().season
        team = self.get_object(pk)
        # Do these querys only once here, instead of doing them 2 times at serializer.
        throws_total = Throw.objects.filter(season=season, team=team).count()
        pikes_total = Throw.objects.filter(season=season, team=team, score=-1).count()
        zeros_total = Throw.objects.filter(season=season, team=team, score=0).count()
        context = {
            'season':season,
            'throws_total': throws_total,
            'pikes_total': pikes_total,
            'zeros_total': zeros_total,
        }
        serializer = TeamDetailSerializer(team, context=context)
        return Response(serializer.data)

class MatchList(APIView):
    """
    Return all matches
    """
    def get(self, request, format=None):
        try:
            season_id = request.query_params.get('season')
            if season_id:
                season = Season.objects.get(id=season_id)
            else:
                raise Season.DoesNotExist
        except Season.DoesNotExist:
            season = CurrentSeason.objects.first().season
        matches = Match.objects.filter(season=season)
        serializer = MatchListSerializer(matches, many=True, context={'season':season})
        return Response(serializer.data)

class MatchDetail(APIView):
    """
    Return data of a single match
    """
    def get_object(self, pk):
        try:
            match = Match.objects.get(pk=pk)
            return match
        except Match.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        match = self.get_object(pk)
        serializer = MatchDetailSerializer(match)
        return Response(serializer.data)
