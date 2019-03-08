from rest_framework import serializers
from kyykka.models import Team, Season, PlayersInTeam, Match, Throw, CurrentSeason
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Min, Sum

class UserSerializer(serializers.ModelSerializer):
    score_total = serializers.SerializerMethodField()
    match_count = serializers.SerializerMethodField()
    pikes_total = serializers.SerializerMethodField()
    zeros_total = serializers.SerializerMethodField()
    throws_total = serializers.SerializerMethodField()

    def get_score_total(self, obj):
        return Throw.objects.filter(player=obj).aggregate(Sum('score'))['score__sum']

    def get_match_count(self, obj):
        return Match.objects.filter(throw__player=obj).distinct().count()

    # def get_pikes_total(self, obj):
    #     return Throw.objects.filter(player=obj)
    #
    # def get_zeros_total(self, obj):
    #     return Match.objects.filter(throw__player=obj).distinct().count()
    #
    # def get_throws_total(self, obj):
    #     return Match.objects.filter(throw__player=obj).distinct().count()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'score_total', 'match_count')

class TeamSerializer(serializers.ModelSerializer):
    players = serializers.SerializerMethodField()

    def get_players(self, obj):
        users = obj.players
        return UserSerializer(users,many=True).data


    class Meta:
        model = Team
        fields = ('id', 'name', 'abbreviation', 'players')
