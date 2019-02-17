from django.db import models

# Create your models here.

class Users(models.Model):
    userID = models.IntegerField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=64)
    email = models.EmailField()
    userRole = models.ForeignKey(UserRoles)

class Matches(models.Model):
    match_id = models.IntegerField()
    season_id = models.IntegerField()
    match_time = models.DateField()
    home_first_round_score = models.IntegerField()
    home_second_round_score = models.IntegerField()
    away_first_round_score = models.IntegerField()
    away_second_round_score = models.IntegerField()
    home_team_id = models.ForeignKey(Teams)
    away_team_id = models.ForeignKey(Teams)
    is_validated = models.BooleanField(initial=False)

class PlayersInTeams(models.Model):
    id = models.IntegerField(primary_key=True) 
    season_id = models.IntegerField() 
    team_id = models.ForeignKey(Teams)
    player_id = models.ForeignKey(Users)


class Teams(models.Model):
    team_id = models.IntegerField()  
    name = models.CharField()
    abbreviation = models.CharField(max_length=10)
    captain_id = models.IntegerField()

class TeamsInSeason(models.Model):
    class Meta:
        unique_together = (('season_id', 'team_id'),)

    season_id = models.IntegerField() 
    team_id = models.ForeignKey(Teams) 

class Throws(models.Model):
    throw_id = models.IntegerField()  
    match_id = models.ForeignKey(Matches)
    player_id = models.ForeignKey(Users)
    season_id = models.IntegerField()
    throw_type_id = models.ForeignKey(ThrowTypes)
    score = models.CharField(max_length=2)

class ThrowTypes(models.Model):
    throw_type_id = models.IntegerField()
    throw_order_ingame = models.CharField()

class UserRoles(models.Model):
    ROLES = (
        (1,'Admin'),
        (2,'captain'),
        (3,'player'),
        )
    id = models.IntegerField(primary_key=True)  
    role = models.CharField(max_length=6,choices=ROLES)

class News(models.Model):
    header = models.TextField()
    date = models.DateTimeField()
    text = models.TextField()