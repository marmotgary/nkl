from rest_framework import serializers
from kyykka.models import Team, Season, PlayersInTeam, Match, Throw, CurrentSeason
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Min, Sum

class UserListSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    score_total = serializers.SerializerMethodField()
    pikes_total = serializers.SerializerMethodField()
    zeros_total = serializers.SerializerMethodField()
    throws_total = serializers.SerializerMethodField()
    pike_percentage = serializers.SerializerMethodField()
    # score_per_throw = serializers.SerializerMethodField()
    season = CurrentSeason.objects.first().season


    def get_team(self, obj):
        try:
            team = TeamSerializer(obj.team_set.get(playersinteam__season=self.season)).data
        except Team.DoesNotExist:
            team = None
        return team

    def get_score_total(self, obj):
        return Throw.objects.filter(season=self.season, player=obj).aggregate(Sum('score'))['score__sum']

    def get_match_count(self, obj):
        return Match.objects.filter(season=self.season, throw__player=obj).distinct().count()

    def get_pikes_total(self, obj):
        self.pikes = obj.throw_set.filter(season=self.season, player=obj, score=-1).count()
        return self.pikes

    def get_zeros_total(self, obj):
        return Throw.objects.filter(season=self.season, player=obj, score=0).count()

    def get_throws_total(self, obj):
        self.throws = Throw.objects.filter(season=self.season, player=obj).count()
        return self.throws

    def get_pike_percentage(self, obj):
        pike_count = self.pikes
        total_count = self.throws
        try:
            pike_percentage = pike_count / total_count
        except ZeroDivisionError:
            pike_percentage = 0
        return 0

    # def get_score_per_throw(self, obj):
    #     Match

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'team', 'score_total',
                    'pikes_total', 'zeros_total', 'throws_total', 'pike_percentage')

class UserDetailSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    score_total = serializers.SerializerMethodField()
    match_count = serializers.SerializerMethodField()
    round_count = serializers.SerializerMethodField()
    pikes_total = serializers.SerializerMethodField()
    zeros_total = serializers.SerializerMethodField()
    throws_total = serializers.SerializerMethodField()
    sixes_total = serializers.SerializerMethodField()
    pike_percentage = serializers.SerializerMethodField()
    zero_percentage = serializers.SerializerMethodField()
    score_per_throw = serializers.SerializerMethodField()
    avg_throw_turn = serializers.SerializerMethodField()
    matches = serializers.SerializerMethodField()
    season = CurrentSeason.objects.first().season


    def get_team(self, obj):
        try:
            team = TeamSerializer(obj.team_set.get(playersinteam__season=self.season)).data
        except Team.DoesNotExist:
            team = None
        return team

    def get_score_total(self, obj):
        return int(Throw.objects.filter(season=self.season, player=obj).aggregate(Sum('score'))['score__sum'])

    def get_match_count(self, obj):
        return Match.objects.filter(season=self.season, throw__player=obj).distinct().count()

    def get_round_count(self, obj):
        return obj.throw_set.count() // 4

    def get_pikes_total(self, obj):
        self.pikes = obj.throw_set.filter(season=self.season, player=obj, score=-1).count()
        return self.pikes

    def get_zeros_total(self, obj):
        self.zeros = Throw.objects.filter(season=self.season, player=obj, score=0).count()
        return self.zeros

    def get_throws_total(self, obj):
        self.throws = Throw.objects.filter(season=self.season, player=obj).count()
        return self.throws

    def get_sixes_total(self, obj):
        self.throws = Throw.objects.filter(season=self.season, player=obj, score__gte=6).count()
        return self.throws

    def get_pike_percentage(self, obj):
        pike_count = self.pikes
        total_count = self.throws
        try:
            pike_percentage = round((pike_count / total_count)*100, 2)
        except ZeroDivisionError:
            pike_percentage = 0
        return pike_percentage

    def get_zero_percentage(self, obj):
        zero_count = self.zeros
        total_count = self.throws
        try:
            pike_percentage = round((zero_count / total_count)*100, 2)
        except ZeroDivisionError:
            pike_percentage = 0
        return pike_percentage


    def get_score_per_throw(self, obj):
        return None

    def get_avg_throw_turn(self, obj):
        return None

    def get_matches(self, obj):
        try:
            matches = Match.objects.filter(throw__player=obj).distinct()
            matches = UserMatchSerializer(matches, many=True).data
        except Match.DoesNotExist:
            matches = []
        return matches

    class Meta:
        model = User
        fields = (
                'id', 'first_name', 'last_name', 'team', 'score_total', 'match_count',
                'round_count', 'sixes_total', 'pikes_total', 'zeros_total', 'throws_total', 'pike_percentage',
                'zero_percentage', 'score_per_throw', 'avg_throw_turn', 'matches',
                  )

# class UserThrowSerializer(serializers.ModelSerializer):
#     round = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Throw
#         fields = ('id', 'throw_round', 'throw_', 'away_team')

class UserMatchSerializer(serializers.ModelSerializer):
    # round = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = ('id', 'match_time', 'home_team', 'away_team')

class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('id', 'name', 'abbreviation')


class TeamPlayerSerializer(serializers.ModelSerializer):
    players = serializers.SerializerMethodField()

    def get_players(self, obj):
        users = obj.players
        return UserListSerializer(users,many=True).data


    class Meta:
        model = Team
        fields = ('id', 'name', 'abbreviation', 'players')
