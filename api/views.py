from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.db.models import Q
from rest_framework import status, viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_swagger.views import get_swagger_view
from rest_framework.mixins import UpdateModelMixin
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


def getRole(user):
    if user.groups.filter(name='captains').exists():
        role = '2'
    else:
        role = '1'
    return role


def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})


def ping(request):
    return JsonResponse({'result:': 'pong'})


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
        response.delete_cookie('role')
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


class ReservePlayerAPI(generics.GenericAPIView):
    serializer_class = ReserveCreateSerializer
    queryset = User.objects.all()

    def get(self, request):
        season = getSeason(request)
        queryset = User.objects.all()
        serializer = ReserveListSerializer(queryset, many=True, context={'season': season})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('kyykka.add_playersinteam'):
            return Response(status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        success, message = serializer.save()
        return Response({
            'success': success,
            'message': message,
        })


class ReservePlayerViewSet(viewsets.ViewSet):
    """
    This viewset provides `list` and `detail` actions.
    NOT CURRENTLY IN USE, ReservePlayerAPI is.
    """
    queryset = User.objects.all()

    def list(self, request):
        season = getSeason(request)
        self.queryset.filter(playersinteam__season=season)
        serializer = ReserveListSerializer(self.queryset, many=True, context={'season': season})
        return Response(serializer.data)

    def create(self, request):
        serializer = ReserveCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response(None)
        # serializer = ReserveCreateSerializer
        # serializer.is_valid(raise_exception=True)
        # success, message = serializer.save()


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()

    def list(self, request, format=None):
        season = getSeason(request)
        self.queryset.filter(playersinteam__season=season)
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
            count=Count('pk', filter=Q(score_first=-1)) + Count('pk', filter=Q(score_second=-1)) + Count('pk', filter=Q(
                score_third=-1)) + Count('pk', filter=Q(score_fourth=-1))).aggregate(Sum('count'))['count__sum']
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
        serializer = MatchDetailSerializer(match, context={'season': season})
        return Response(serializer.data)


class ThrowAPI(generics.GenericAPIView, UpdateModelMixin):
    serializer_class = ThrowSerializer
    queryset = Throw.objects.all()

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
