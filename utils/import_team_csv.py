# -*- coding: utf-8 -*-
# Run this through shell - put teamcaptains.csv into  root folder

import csv
from django.contrib.auth.models import User
from django.db import transaction
from kyykka.models import Team, PlayersInTeam, CurrentSeason, Season, Player


def murmeli():
    """
    Read and generate teams from a csv. If captain has an account, link it to the team
    """
    with open('teamscaptains.csv', encoding="utf8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        with transaction.atomic():
            for row in readCSV:
                team_name = row[0]
                team_abb = row[1]
                captain_name = row[2]
                user = None
                if captain_name.find('Darkkis') != -1:
                    user = User.objects.get(id=154)
                else:
                    first = captain_name.split(' ')[0]
                    last = captain_name.split(' ')[1]
                    try:
                        user = User.objects.get(first_name=first, last_name__icontains=last)
                    except User.DoesNotExist as e:
                        print('No User found', captain_name)
                        pass
                    except User.MultipleObjectsReturned as e:
                        print("MultibleObjects", captain_name)
                        pass
                team = Team.objects.create(
                    name=team_name,
                    abbreviation=team_abb
                )
                print('Created team', team.id, team)
                if user is not None:
                    PlayersInTeam.objects.create(
                        season=CurrentSeason.objects.first().season,
                        team=team,
                        player=user,
                        is_captain=True
                    )
                    print('Added captain for team', user)