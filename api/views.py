from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.db.models import Q
from rest_framework import status, viewsets, generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_swagger.views import get_swagger_view
from rest_framework.mixins import UpdateModelMixin
from rest_framework.throttling import AnonRateThrottle
from kyykka.models import User, Team
from kyykka.serializers import *
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
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


def getRole(user):
    if user.playersinteam_set.get(season=CurrentSeason.objects.first().season).is_captain:
        role = '1'
    else:
        role = '0'
    return role


@ensure_csrf_cookie
def csrf(request):
    return HttpResponse(status=status.HTTP_200_OK)


def ping(request):
    return JsonResponse({'result:': 'pong'})


class IsCaptain(permissions.BasePermission):
    """
    Permission check to verify that user is captain in the right team.
    """
    def has_permission(self, request, view):
        try:
            return request.user.playersinteam_set.get(season=CurrentSeason.objects.first().season).is_captain
        except PlayersInTeam.DoesNotExist as e:
            return False


class IsCaptainForThrow(permissions.BasePermission):
    """
    Permission check to verify if user is captain in the right team for a throw
    """
    def has_object_permission(self, request, view, obj):
        try:
            return request.user == obj.match.home_team.playersinteam_set.filter(
                season=CurrentSeason.objects.first().season,
                is_captain=True
            ).first().player
        except AttributeError as e:
            print('has_object_permission', request.user.id, obj)
            return False


class MatchDetailPermission(permissions.BasePermission):
    """
    If patching is_validated, user needs to be captain of the away_team
    Else user needs to be captain of the away_team (patchin round scores)
    """
    def has_object_permission(self, request, view, obj):
        if 'is_validated' in request.data and len(request.data) == 1:
            return request.user == obj.away_team.playersinteam_set.filter(season=CurrentSeason.objects.first().season,
                                                                          is_captain=True).first().player
        if 'is_validated' not in request.data:
            return request.user == obj.home_team.playersinteam_set.filter(season=CurrentSeason.objects.first().season,
                                                                          is_captain=True).first().player

class LoginAPI(generics.GenericAPIView):
    """
    Creates session for user upon successful login
    Set cookies sessionid and role (1 for player, 2 for captain)
    """
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        role = getRole(user)
        response = HttpResponse(json.dumps({'success': True,
                                            'user': UserSerializer(user).data,
                                            'role': role}))
        return response


class LogoutAPI(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        response = HttpResponse(json.dumps({'success': True}))
        # response.delete_cookie('role')
        response.delete_cookie('csrftoken')
        return response


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        success, message, user = serializer.save()
        login(request, user)
        return Response({
            'success': success,
            'message': message,
            'user': UserSerializer(user).data,
            'role': '0'
        })


class ReservePlayerAPI(generics.GenericAPIView):
    serializer_class = ReserveCreateSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated, IsCaptain]

    def get(self, request):
        season = getSeason(request)
        queryset = User.objects.all()
        serializer = ReserveListSerializer(queryset, many=True, context={'season': season})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        success, message = serializer.save()
        return Response({
            'success': success,
            'message': message,
        })


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()

    def list(self, request, format=None):
        season = getSeason(request)
        self.queryset = self.queryset.filter(playersinteam__season=season)
        serializer = PlayerListSerializer(self.queryset, many=True, context={'season': season})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        season = getSeason(request)
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = PlayerDetailSerializer(user, context={'season': season})
        return Response(serializer.data)


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Team.objects.all()

    def list(self, request):
        season = getSeason(request)
        self.queryset = self.queryset.filter(playersinteam__season=season).distinct()
        serializer = TeamListSerializer(self.queryset, many=True, context={'season': season})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        season = getSeason(request)
        team = get_object_or_404(self.queryset, pk=pk)
        # Do these querys only once here, instead of doing them 2 times at serializer.
        throws_total = Throw.objects.filter(season=season, team=team).count() * 4
        pikes_total = Throw.objects.filter(season=season, team=team).annotate(
            count=Count('pk', filter=Q(score_first='h')) + Count('pk', filter=Q(score_second='h')) + Count('pk', filter=Q(
                score_third='h')) + Count('pk', filter=Q(score_fourth='h'))).aggregate(Sum('count'))['count__sum']
        zeros_total = Throw.objects.filter(season=season, team=team).annotate(
            count=Count('pk', filter=Q(score_first=0)) + Count('pk', filter=Q(score_second=0)) + Count('pk', filter=Q(
                score_third=0)) + Count('pk', filter=Q(score_fourth=0))).aggregate(Sum('count'))['count__sum']
        context = {
            'season': season,
            'throws_total': throws_total,
            'pikes_total': pikes_total,
            'zeros_total': zeros_total,
        }
        serializer = TeamDetailSerializer(team, context=context)
        return Response(serializer.data)


class MatchList(APIView):
    """
    List all matches
    """
    # throttle_classes = [AnonRateThrottle]
    queryset = Match.objects.all()

    def get(self, request):
        season = getSeason(request)
        self.queryset = self.queryset.filter(season=season)
        serializer = MatchListSerializer(self.queryset, many=True, context={'season': season})
        return Response(serializer.data)


class MatchDetail(APIView):
    """
    Retrieve or update a Match instance
    """
    # throttle_classes = [AnonRateThrottle]
    queryset = Match.objects.all()
    permission_classes = [MatchDetailPermission]

    def get(self, request, pk):
        season = getSeason(request)
        match = get_object_or_404(self.queryset, pk=pk)
        serializer = MatchDetailSerializer(match, context={'season': season})
        return Response(serializer.data)

    def patch(self, request, pk ,format=None):
        match = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(request, match)
        serializer = MatchScoreSerializer(match, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThrowAPI(generics.GenericAPIView, UpdateModelMixin):
    serializer_class = ThrowSerializer
    queryset = Throw.objects.all()
    permission_classes = [IsAuthenticated, IsCaptain, IsCaptainForThrow]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
