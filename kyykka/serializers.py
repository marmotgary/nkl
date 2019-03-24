from rest_framework import serializers
from kyykka.models import Team, Season, PlayersInTeam, Match, Throw, CurrentSeason
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Avg, Count, Min, Sum, F, Q
from django.db import IntegrityError



def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')

class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.EmailField()
    first_name = serializers.CharField(validators=[required], max_length=30)
    last_name = serializers.CharField(validators=[required], max_length=150)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            user = User.objects.create_user(validated_data['username'],
                                            validated_data['username'],
                                            validated_data['password'])
            user.first_name = validated_data['first_name']
            user.last_name = validated_data['last_name']
            return True, None
        except IntegrityError as e:
            return False, "Email is already taken"


class LoginUserSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")
class SharedPlayerSerializer(serializers.ModelSerializer):
    def get_player_name(self,obj):
        return obj.first_name + " " + obj.last_name

    def get_score_total(self, obj):
        try:
            return int(Throw.objects.filter(season=self.context.get('season'), player=obj, score__gt=0).aggregate(Sum('score'))['score__sum'])
        except TypeError:
            return 0

    def get_match_count(self, obj):
        return Match.objects.filter(season=self.context.get('season'), throw__player=obj).distinct().count()

    def get_rounds_total(self, obj):
        return obj.throw_set.count() // 4

    def get_team(self, obj):
        try:
            team = TeamSerializer(obj.team_set.get(playersinteam__season=self.context.get('season'))).data
        except Team.DoesNotExist:
            team = None
        return team

    def get_pikes_total(self, obj):
        self.pikes = obj.throw_set.filter(season=self.context.get('season'), player=obj, score=-1).count()
        return self.pikes

    def get_zeros_total(self, obj):
        self.zeros = Throw.objects.filter(season=self.context.get('season'), player=obj, score=0).count()
        return self.zeros

    def get_gteSix_total(self, obj):
        return Throw.objects.filter(season=self.context.get('season'), player=obj, score__gte=6).count()

    def get_throws_total(self, obj):
        self.throws = Throw.objects.filter(season=self.context.get('season'), player=obj).count()
        return self.throws

    def get_pike_percentage(self, obj):
        pike_count = self.pikes
        total_count = self.throws
        try:
            pike_percentage = round((pike_count / total_count)*100, 2)
        except ZeroDivisionError:
            pike_percentage = 0
        return pike_percentage

    def get_score_per_throw(self, obj):
        return None

    def get_avg_throw_turn(self, obj):
        return None

    class Meta:
        model = User

class PlayerListSerializer(SharedPlayerSerializer):
    team = serializers.SerializerMethodField()
    player_name = serializers.SerializerMethodField()
    score_total = serializers.SerializerMethodField()
    rounds_total = serializers.SerializerMethodField()
    pikes_total = serializers.SerializerMethodField()
    zeros_total = serializers.SerializerMethodField()
    gteSix_total = serializers.SerializerMethodField()
    throws_total = serializers.SerializerMethodField()
    pike_percentage = serializers.SerializerMethodField()
    score_per_throw = serializers.SerializerMethodField()
    avg_throw_turn = serializers.SerializerMethodField()
    scaled_points = serializers.SerializerMethodField()
    scaled_points_per_round = serializers.SerializerMethodField()
    def get_scaled_points(self, obj):
        return None
    def get_scaled_points_per_round(self, obj):
        return None
    class Meta:
        model = User
        fields = ('id', 'player_name', 'team', 'score_total', 'rounds_total',
                    'pikes_total', 'zeros_total', 'gteSix_total', 'throws_total', 'pike_percentage',
                    'score_per_throw', 'scaled_points', 'scaled_points_per_round', 'avg_throw_turn')

class PlayerDetailSerializer(SharedPlayerSerializer):
    team = serializers.SerializerMethodField()
    player_name = serializers.SerializerMethodField()
    score_total = serializers.SerializerMethodField()
    match_count = serializers.SerializerMethodField()
    rounds_total = serializers.SerializerMethodField()
    pikes_total = serializers.SerializerMethodField()
    zeros_total = serializers.SerializerMethodField()
    ones_total = serializers.SerializerMethodField()
    twos_total = serializers.SerializerMethodField()
    threes_total = serializers.SerializerMethodField()
    fours_total = serializers.SerializerMethodField()
    fives_total = serializers.SerializerMethodField()
    throws_total = serializers.SerializerMethodField()
    gteSix_total = serializers.SerializerMethodField()
    pike_percentage = serializers.SerializerMethodField()
    zero_percentage = serializers.SerializerMethodField()
    score_per_throw = serializers.SerializerMethodField()
    avg_throw_turn = serializers.SerializerMethodField()
    matches = serializers.SerializerMethodField()

    def get_ones_total(self, obj):
        return Throw.objects.filter(season=self.context.get('season'), player=obj, score=1).count()

    def get_twos_total(self, obj):
        return Throw.objects.filter(season=self.context.get('season'), player=obj, score=2).count()

    def get_threes_total(self, obj):
        return Throw.objects.filter(season=self.context.get('season'), player=obj, score=3).count()

    def get_fours_total(self, obj):
        return Throw.objects.filter(season=self.context.get('season'), player=obj, score=4).count()

    def get_fives_total(self, obj):
        return Throw.objects.filter(season=self.context.get('season'), player=obj, score=5).count()

    def get_gteSix_total(self, obj):
        self.throws = Throw.objects.filter(season=self.context.get('season'), player=obj, score__gte=6).count()
        return self.throws

    def get_zero_percentage(self, obj):
        zero_count = self.zeros
        total_count = self.throws
        try:
            pike_percentage = round((zero_count / total_count)*100, 2)
        except ZeroDivisionError:
            pike_percentage = 0
        return pike_percentage

    def get_matches(self, obj):
        try:
            matches = Match.objects.filter(throw__player=obj, season=self.context.get('season')).distinct()
            matches = UserMatchSerializer(matches, many=True, context={'user_id':obj.id}).data
        except Match.DoesNotExist:
            matches = None
        return matches

    class Meta:
        model = User
        fields = (
                'id', 'player_name', 'team', 'score_total', 'match_count',
                'rounds_total', 'zeros_total', 'ones_total', 'twos_total', 'threes_total',
                'fours_total', 'fives_total', 'gteSix_total', 'pikes_total', 'throws_total', 'pike_percentage',
                'zero_percentage', 'score_per_throw', 'avg_throw_turn', 'matches',
                  )

class UserMatchSerializer(serializers.ModelSerializer):
    throws = serializers.SerializerMethodField()


    def get_throws(self, obj):
        try:
            user = self.context.get('user_id')
            throws = obj.throw_set.filter(player=user)
            # rounds = UserRoundThrowSerializer(throws, many=True).data
            rounds = UserThrowSerializer(throws, many=True).data
        except Throw.DoesNotExist:
            rounds = None
        return rounds

    class Meta:
        model = Match
        fields = ('id', 'match_time', 'home_team', 'away_team', 'throws')

class UserRoundThrowSerializer(serializers.Serializer):
    first_round = serializers.SerializerMethodField()
    second_round = serializers.SerializerMethodField()

    def get_first_round(self, obj):
        # throws = obj.filter(throw_round=1)
        throws = None
        throws = UserThrowSerializer(obj).data
        return throws

    def get_second_round(self, obj):
        return 2

class UserThrowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Throw
        fields = ('id', 'throw_round', 'throw_turn', 'throw_number', 'score')

class PlayerNameSerializer(SharedPlayerSerializer):
    player_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'player_name')


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('id', 'name', 'abbreviation')

class TeamListSerializer(serializers.ModelSerializer):
    matches_won = serializers.SerializerMethodField()
    matches_lost = serializers.SerializerMethodField()
    matches_tie = serializers.SerializerMethodField()
    matches_played = serializers.SerializerMethodField()
    score_total = serializers.SerializerMethodField()

    def get_matches_won(self, obj):
        home_wins = obj.home_matches.filter(season=self.context.get('season')).annotate(home = F('home_first_round_score') + F('home_second_round_score'), \
         away = F('away_first_round_score') + F('away_second_round_score')).filter(home__gt=F('away')).count()
        away_wins = obj.away_matches.filter(season=self.context.get('season')).annotate(home = F('home_first_round_score') + F('home_second_round_score'), \
         away = F('away_first_round_score') + F('away_second_round_score')).filter(away__gt=F('home')).count()
        return home_wins + away_wins

    def get_matches_lost(self, obj):
        home_loses = obj.home_matches.filter(season=self.context.get('season')).annotate(home = F('home_first_round_score') + F('home_second_round_score'), \
         away = F('away_first_round_score') + F('away_second_round_score')).filter(away__gt=F('home')).count()
        away_loses = obj.away_matches.filter(season=self.context.get('season')).annotate(home = F('home_first_round_score') + F('home_second_round_score'), \
         away = F('away_first_round_score') + F('away_second_round_score')).filter(home__gt=F('away')).count()
        return home_loses + away_loses
    def get_matches_tie(self, obj):
        home_ties = obj.home_matches.filter(season=self.context.get('season')).annotate(home = F('home_first_round_score') + F('home_second_round_score'), \
         away = F('away_first_round_score') + F('away_second_round_score')).filter(home__exact=F('away')).count()
        away_ties = obj.away_matches.filter(season=self.context.get('season')).annotate(home = F('home_first_round_score') + F('home_second_round_score'), \
         away = F('away_first_round_score') + F('away_second_round_score')).filter(away__exact=F('home')).count()
        return home_ties + away_ties
    def get_matches_played(self, obj):
        return Match.objects.filter(season=self.context.get('season')).filter(Q(home_team=obj) | Q(away_team=obj)).count()
    def get_score_total(self, obj):
        return Throw.objects.filter(score__gt=0, team=obj, season=self.context.get('season')).aggregate(Sum('score'))['score__sum']

    class Meta:
        model = Team
        fields = ('id', 'name', 'abbreviation', 'matches_won', 'matches_lost', 'matches_tie',
                    'matches_played', 'score_total')

class TeamDetailSerializer(serializers.ModelSerializer):
    score_total = serializers.SerializerMethodField()
    match_count = serializers.SerializerMethodField()
    pikes_total = serializers.SerializerMethodField()
    zeros_total = serializers.SerializerMethodField()
    zero_first_throw_total = serializers.SerializerMethodField()
    pike_first_throw_total = serializers.SerializerMethodField()
    throws_total = serializers.SerializerMethodField()
    gteSix_total = serializers.SerializerMethodField()
    pike_percentage = serializers.SerializerMethodField()
    zero_percentage = serializers.SerializerMethodField()
    score_per_throw = serializers.SerializerMethodField()
    matches = serializers.SerializerMethodField()
    players = serializers.SerializerMethodField()


    def get_score_total(self, obj):
        try:
            return int(Throw.objects.filter(score__gt=0, team=obj, season=self.context.get('season')).aggregate(Sum('score'))['score__sum'])
        except TypeError:
            return 0
    def get_match_count(self, obj):
        return Match.objects.filter(season=self.context.get('season'), throw__team=obj).distinct().count()
    def get_throws_total(self, obj):
        return self.context.get('throws_total')
    def get_pikes_total(self, obj):
        return self.context.get('pikes_total')
    def get_zeros_total(self, obj):
        return self.context.get('zeros_total')
    def get_zero_first_throw_total(self, obj):
        return Throw.objects.filter(season=self.context.get('season'), team=obj, score=0, throw_turn=1, throw_number=1).count()
    def get_pike_first_throw_total(self, obj):
        return Throw.objects.filter(season=self.context.get('season'), team=obj, score=-1, throw_turn=1, throw_number=1).count()
    def get_gteSix_total(self, obj):
        return Throw.objects.filter(season=self.context.get('season'), team=obj, score__gte=6).count()
    def get_pike_percentage(self, obj):
        try:
            pike_percentage = round((self.context.get('pikes_total') / self.context.get('throws_total'))*100, 2)
        except ZeroDivisionError:
            pike_percentage = 0
        return pike_percentage
    def get_zero_percentage(self, obj):
        try:
            zero_percentage = round((self.context.get('zeros_total') / self.context.get('throws_total'))*100, 2)
        except ZeroDivisionError:
            zero_percentage = 0
        return zero_percentage
    def get_score_per_throw(self, obj):
        return None
    def get_matches(self, obj):
        return None
    def get_players(self, obj):
        users = obj.players
        return PlayerListSerializer(users,many=True).data


    class Meta:
        model = Team
        fields = ('id', 'name', 'abbreviation', 'score_total', 'match_count', 'pikes_total',
                    'zeros_total', 'zero_first_throw_total', 'pike_first_throw_total',
                    'throws_total', 'gteSix_total', 'pike_percentage', 'zero_percentage',
                    'score_per_throw', 'matches', 'players')

class SharedMatchSerializer(serializers.ModelSerializer):
    def get_home_score_total(self, obj):
        return obj.home_first_round_score + obj.home_second_round_score

    def get_away_score_total(self, obj):
        return obj.away_first_round_score + obj.away_second_round_score


class MatchListSerializer(SharedMatchSerializer):
    home_score_total = serializers.SerializerMethodField()
    away_score_total = serializers.SerializerMethodField()
    home_team = serializers.SerializerMethodField()
    away_team = serializers.SerializerMethodField()

    def get_home_team(self, obj):
        return TeamSerializer(obj.home_team).data

    def get_away_team(self, obj):
        return TeamSerializer(obj.away_team).data

    class Meta:
        model = Match
        fields = ('id', 'match_time', 'home_team', 'away_team', 'home_score_total', 'away_score_total')

class MatchDetailSerializer(SharedMatchSerializer):
    home_score_total = serializers.SerializerMethodField()
    away_score_total = serializers.SerializerMethodField()
    home_team = serializers.SerializerMethodField()
    away_team = serializers.SerializerMethodField()
    first_round = serializers.SerializerMethodField()
    second_round = serializers.SerializerMethodField()

    def get_second_round(self, obj):
        return MatchRoundSerializer(obj.throw_set.filter(throw_round=2), context={'home_team':obj.home_team, 'away_team':obj.away_team}).data

    def get_first_round(self, obj):
        return MatchRoundSerializer(obj.throw_set.filter(throw_round=1), context={'home_team':obj.home_team, 'away_team':obj.away_team}).data

    def get_home_team(self, obj):
        return MatchTeamSerializer(obj.home_team, context={'season': self.context.get('season')}).data

    def get_away_team(self, obj):
        return MatchTeamSerializer(obj.away_team, context={'season': self.context.get('season')}).data

    class Meta:
        model = Match
        fields = ('id', 'match_time', 'home_score_total', 'away_score_total', 'home_first_round_score', 'home_second_round_score',
                    'away_first_round_score', 'away_second_round_score', 'first_round', 'second_round', 'home_team', 'away_team', 'is_validated')

class MatchTeamSerializer(serializers.ModelSerializer):
    players = serializers.SerializerMethodField()

    def get_players(self, obj):
        return PlayerNameSerializer(obj.players.filter(playersinteam__season=self.context.get('season')), many=True).data

    class Meta:
        model = Team
        fields = ('id', 'name', 'abbreviation', 'players')

class MatchRoundSerializer(serializers.ModelSerializer):
    home = serializers.SerializerMethodField()
    away = serializers.SerializerMethodField()

    def get_home(self, qs):
        player_ids = qs.filter(team=self.context.get('home_team')).values_list('player__id', flat=True).distinct()
        players = User.objects.filter(id__in=player_ids)
        return MatchRowSerialzier(players, many=True, context={'throws':qs}).data

    def get_away(self, qs):
        player_ids = qs.filter(team=self.context.get('away_team')).values_list('player__id', flat=True).distinct()
        players = User.objects.filter(id__in=player_ids)
        return MatchRowSerialzier(players, many=True, context={'throws':qs}).data

    class Meta:
        model = Throw
        fields = ('home', 'away')

class MatchRowSerialzier(SharedPlayerSerializer):
    player_name = serializers.SerializerMethodField()
    score_total = serializers.SerializerMethodField()
    throws = serializers.SerializerMethodField()

    def get_throws(self, obj):
        throws = self.context.get('throws').filter(player=obj)
        return ThrowScoreSerialzier(throws, many=True).data
    def get_score_total(self, obj):
        throws = self.context.get('throws').filter(player=obj, score__gt=0)
        try:
            return int(throws.aggregate(Sum('score'))['score__sum'])
        except TypeError:
            return 0

    class Meta:
        model = User
        fields = ('player_name', 'score_total', 'throws')

class ThrowScoreSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Throw
        fields = ('score', 'throw_number')
