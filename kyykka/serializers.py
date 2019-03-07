from rest_framework import serializers
from kyykka.models import Team, Season, PlayersInTeam, Match, Throw, CurrentSeason
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'abbreviation', 'players')
