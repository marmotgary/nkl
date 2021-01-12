import datetime
import json

from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Q, Sum
from django.http import Http404, HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from kyykka.models import (CurrentSeason, Match, PlayersInTeam, Season, Team,
                           Throw, User)
from kyykka.serializers import (CreateUserSerializer, LoginUserSerializer,
                                MatchDetailSerializer, MatchListSerializer,
                                MatchScoreSerializer, PlayerDetailSerializer,
                                PlayerListSerializer, ReserveCreateSerializer,
                                ReserveListSerializer, TeamDetailSerializer,
                                TeamListSerializer, ThrowSerializer,
                                UserSerializer)
from rest_framework import generics, permissions, status, viewsets
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_swagger.views import get_swagger_view
from utils.caching import (cache_reset_key, getFromCache, reset_match_cache,
                           setToCache, reset_player_cache)

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
    try:
        if user.playersinteam_set.get(season=CurrentSeason.objects.first().season).is_captain:
            role = '1'
        else:
            role = '0'
    except PlayersInTeam.DoesNotExist as e:
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
            if request.user.is_superuser:
                return True
            return request.user.playersinteam_set.get(season=CurrentSeason.objects.first().season).is_captain
        except PlayersInTeam.DoesNotExist as e:
            return False


class IsCaptainForThrow(permissions.BasePermission):
    """
    Permission check to verify if user is captain in the right team for updaing throws
    """
    def has_object_permission(self, request, view, obj):
        try:
            if request.user.is_superuser:
                return True
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
        if request.user.is_superuser:
            return True
        if 'is_validated' in request.data and len(request.data) == 1:
            return request.user == obj.away_team.playersinteam_set.filter(season=CurrentSeason.objects.first().season,
                                                                          is_captain=True).first().player
        if 'is_validated' not in request.data:
            return request.user == obj.home_team.playersinteam_set.filter(season=CurrentSeason.objects.first().season,
                                                                          is_captain=True).first().player


# @method_decorator(ensure_csrf_cookie, name='dispatch')
# @method_decorator(csrf_protect, name='dispatch')
class LoginAPI(generics.GenericAPIView):
    # TODO: Verify what happens if eg. two browsers are used, and session ends in other one. 
    """
    Creates session for user upon successful login
    Set sessionid and CSRF to cookies
    Return User, role and team_id
    """
    serializer_class = LoginUserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        role = getRole(user)
        try:
            team_id = user.playersinteam_set.filter(season=CurrentSeason.objects.first().season).first().team.id
        except (PlayersInTeam.DoesNotExist, AttributeError) as e:
            team_id = None
        response = Response({
            'success': True,
            'user': UserSerializer(user).data,
            'role': role,
            'team_id': team_id
            })
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
    permission_classes = [IsAuthenticated, IsCaptain]

    def get(self, request):
        season = getSeason(request)
        queryset = User.objects.filter(is_superuser=False).order_by("first_name")
        serializer = ReserveListSerializer(queryset, many=True, context={'season': season})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        success, message = serializer.save()
        if success is False:
            return Response({
            'success': success,
            'message': message,
            }, status=400)
        else: # Success 200
            return Response({
                'success': success,
                'message': message,
            })


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List all players that are in a team for the season beingh queried. 
    """
    queryset = User.objects.all()

    def list(self, request, format=None):
        season = getSeason(request)
        key = 'all_players_' + str(season.year)
        all_players = getFromCache(key)
        if all_players is None:
            self.queryset = self.queryset.filter(playersinteam__season=season)
            serializer = PlayerListSerializer(self.queryset, many=True, context={'season': season})
            all_players = serializer.data
            setToCache(key, all_players)
        return Response(all_players)

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
        key = 'all_teams_' + str(season.year)
        all_teams = getFromCache(key)
        if all_teams is None:
            self.queryset = self.queryset.filter(playersinteam__season=season).distinct()
            serializer = TeamListSerializer(self.queryset, many=True, context={'season': season})
            all_teams = serializer.data
            setToCache(key, all_teams)
        return Response(all_teams)

    def retrieve(self, request, pk=None):
        season = getSeason(request)
        try:
            team = get_object_or_404(self.queryset, pk=pk)
        except ValueError:
            # pk probably not integer?
            raise Http404
        # Do these querys only once here, instead of doing them 2 times at serializer.
        throws = Throw.objects.filter(match__is_validated=True, season=season, team=team)
        throws_total = throws.count() * 4
        pikes_total = throws.annotate(
            count=Count('pk', filter=Q(score_first='h')) + Count('pk', filter=Q(score_second='h')) + Count('pk', filter=Q(
                score_third='h')) + Count('pk', filter=Q(score_fourth='h'))).aggregate(Sum('count'))['count__sum']
        zeros_total = throws.annotate(
            count=Count('pk', filter=Q(score_first=0)) + Count('pk', filter=Q(score_second=0)) + Count('pk', filter=Q(
                score_third=0)) + Count('pk', filter=Q(score_fourth=0))).aggregate(Sum('count'))['count__sum']
        context = {
            'season': season,
            'throws_total': throws_total,
            'pikes_total': pikes_total,
            'zeros_total': zeros_total,
            'throw_set':  throws,
        }
        serializer = TeamDetailSerializer(team, context=context)
        return Response(serializer.data)


class MatchList(APIView):
    """
    List all matches
    """
    # throttle_classes = [AnonRateThrottle]
    # queryset = Match.objects.filter(match_time__lt=datetime.datetime.now() + datetime.timedelta(weeks=2))
    queryset = Match.objects.all()

    def get(self, request):
        season = getSeason(request)
        key = 'all_matches_' + str(season.year)
        all_matches = getFromCache(key)
        if all_matches is None:
            self.queryset = self.queryset.filter(season=season)
            serializer = MatchListSerializer(self.queryset, many=True, context={'season': season})
            all_matches = serializer.data
            setToCache(key, all_matches)
        return Response(all_matches)


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
        season = getSeason(request)
        match = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(request, match)
        # Update user session (so that it wont expire..)
        request.session.modified = True
        serializer = MatchScoreSerializer(match, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            player_ids = match.throw_set.all().values_list("player__id", flat=True).distinct()
            for id in player_ids:
                reset_player_cache(id, str(season.year))
            reset_match_cache(match, season_year=str(season.year))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThrowAPI(generics.GenericAPIView, UpdateModelMixin):
    serializer_class = ThrowSerializer
    queryset = Throw.objects.all()
    permission_classes = [IsAuthenticated, IsCaptain, IsCaptainForThrow]

    def patch(self, request, *args, **kwargs):
        cache_reset_key('all_teams')  # Updating throw score affects total score of team.
        return self.partial_update(request, *args, **kwargs)
