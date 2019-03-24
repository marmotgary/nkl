from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from rest_framework import status, viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_swagger.views import get_swagger_view
from kyykka.models import User, Team
from kyykka.serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import json

schema_view = get_swagger_view(title='NKL API')

def getSeason(request):
    try:
        season_id = request.query_params.get('season')
        if season_id:
            season = Season.objects.get(id=season_id)
        else:
            raise Season.DoesNotExist
    except Season.DoesNotExist:
        season = CurrentSeason.objects.first().season
    return season

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

def ping(request):
    return JsonResponse({'result:': 'pong'})

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        response = HttpResponse(json.dumps({'success':True}))
        return response

class LogoutAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return HttpResponse(json.dumps({'success':True}))

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        response = HttpResponse(json.dumps({'success':True}))
        return response

class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        success, message = serializer.save()
        return Response({
            'success': True,
            'message': message,
        })

class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()

    def list(self, request, format=None):
        season = getSeason(request)
        serializer = PlayerListSerializer(self.queryset.filter(playersinteam__season=season), many=True, context={'season': season})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        season = getSeason(request)
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = PlayerDetailSerializer(user, context={'season' : season})
        return Response(serializer.data)

class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Team.objects.all()

    def list(self, request):
        season = getSeason(request)
        self.queryset = self.queryset.filter(season=season)
        serializer = TeamListSerializer(self.queryset, many=True, context={'season':season})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        season = getSeason(request)
        team = get_object_or_404(self.queryset, pk=pk)
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

class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Match.objects.all()

    def list(self, request):
        season = getSeason(request)
        self.queryset = self.queryset.filter(season=season)
        serializer = MatchListSerializer(self.queryset, many=True, context={'season': season})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        season = getSeason(request)
        match = get_object_or_404(self.queryset, pk=pk)
        serializer = MatchDetailSerializer(match, context={'season' : season})
        return Response(serializer.data)
