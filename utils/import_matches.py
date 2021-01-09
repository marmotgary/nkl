# -*- coding: utf-8 -*-
# Run this through shell - put matches.csv into  root folder

import csv, datetime
from django.db import transaction
from kyykka.models import Team, Match, CurrentSeason


def import_matches():
    """
    Import matches from matches.csv
    """
    with open('matches.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        with transaction.atomic():
            for row in readCSV:
                date_time_str = row[0].replace("'", "")
                home = row[1]
                away = row[2]
                field = row[3]
                date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                home_team = Team.objects.get(abbreviation=home)
                away_team = Team.objects.get(abbreviation=away)
                field_num = field[-1]
                Match.objects.create(
                    season=CurrentSeason.objects.first().season,
                    match_time=date_time_obj,
                    field=field_num,
                    home_team=home_team,
                    away_team=away_team
                )
