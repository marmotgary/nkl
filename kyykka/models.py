from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=128, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)
    players = models.ManyToManyField(User, through='PlayersInTeam')

    def __str__(self):
        return '%s' % (self.abbreviation)

class Season(models.Model):
    year = models.CharField(max_length=4, unique=True)
    teams = models.ManyToManyField(Team, blank=True)

    def __str__(self):
        return 'Season %s' % (self.year)

class CurrentSeason(models.Model):
    season = models.OneToOneField(Season, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Current Season'

    def __str__(self):
        return 'Season %s' % (self.season.year)

class PlayersInTeam(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    is_captain = models.BooleanField(default=False)

    class Meta:
        unique_together = ('player', 'season')
        # Make sure are players allowed to change team during the season?

    def __str__(self):
        return '%s %s %s %s' % (self.season.year, self.team.abbreviation, self.player.first_name, self.player.last_name)

class Match(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    match_time = models.DateTimeField()
    home_first_round_score = models.IntegerField()
    home_second_round_score = models.IntegerField()
    away_first_round_score = models.IntegerField()
    away_second_round_score = models.IntegerField()
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    is_validated = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Matches'

    def __str__(self):
        return 'Match %s - %s %s' % (self.home_team, self.away_team, self.match_time)

# class ThrowType(models.Model):
#     throw_order_ingame = models.CharField()

class Throw(models.Model):
    '''
    throw_round determines is it first(1) or second(2) round of the match.
    throw_turn determines players' throwing turn: 1, 2, 3 or 4.
    throw_number determines is it players' 1st, 2nd, 3rd or 4th throw.
    '''
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    throw_round = models.IntegerField()
    throw_turn = models.IntegerField()
    # throw_number = models.IntegerField(null=True)
    score_first = models.CharField(max_length=2, null=True)
    score_second = models.CharField(max_length=2, null=True)
    score_third = models.CharField(max_length=2, null=True)
    score_fourth = models.CharField(max_length=2, null=True)

# TBD if used
# class UserRoles(models.Model):
#     ROLES = (
#         (1,'Admin'),
#         (2,'captain'),
#         (3,'player'),
#         )
#     role = models.CharField(max_length=6,choices=ROLES)

class News(models.Model):
    header = models.TextField()
    date = models.DateTimeField()
    text = models.TextField()
