import django
from faker import Faker
from tqdm import tqdm
from django.contrib.auth.models import User
from kyykka.models import Team, Season, PlayersInTeam, CurrentSeason, Match, Throw, Player
import random, pytz

fake = Faker('fi_FI')


def initGen():
    '''
    Generates dummy Seasons, Teams and populates teams with Users.
    Create superuser with credentials 'test test'
    '''
    User.objects.create_superuser('test', '', 'test')
    seasonGen()
    teamGen(30)
    matchGen()


def seasonGen(amount=3):
    year = 2019
    for _ in range(amount):
        season = Season.objects.create(year=year)
        if year == 2019:
            CurrentSeason.objects.create(season=season)
        year = year - 1



# Generate Users


def userGen(amount, return_users=False):
    users = []
    for _ in (range(amount)):
        try:
            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            user = User.objects.create_user(email, email, 'test')
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            # user.player.number = random.randint(1,100)
            Player.objects.create(user=user, number=random.randint(1, 100))
            users.append(user)
        except Exception as e:
            print(e)
            pass
    if return_users:
        return users


def teamGen(amount):
    print('Generating fake teams\n')
    for i in tqdm(range(amount)):
        try:
            name = fake.company()
            abbreviation = fake.company_suffix()
            team = Team.objects.create(name=name, abbreviation=abbreviation)
        except:
            name = fake.ean13()
            abbreviation = fake.ean8()
            team = Team.objects.create(name=name, abbreviation=abbreviation)
            pass
        populateTeam(team)


def populateTeam(team):
    print('Generating fake users for team ', team)
    players = userGen(6, True)
    season = CurrentSeason.objects.first().season
    PlayersInTeam.objects.create(
        season=season, team=team, player=players.pop(), is_captain=True)
    for p in players:
        PlayersInTeam.objects.create(season=season, team=team, player=p)


def matchGen():
    season = CurrentSeason.objects.first().season
    exclude = []
    print('\nGenerating fake matches.')
    for home in tqdm(Team.objects.all()):
        exclude.append(home.id)
        for away in Team.objects.all().exclude(id__in=exclude):
            match = Match.objects.create(
                season=season,
                match_time=fake.date_time_between(start_date="-60y", end_date="now",
                                                  tzinfo=pytz.timezone("Europe/Helsinki")),
                home_first_round_score=random.randint(0, 100),
                home_second_round_score=random.randint(0, 100),
                away_first_round_score=random.randint(0, 100),
                away_second_round_score=random.randint(0, 100),
                home_team=home,
                away_team=away,
                is_validated=random.choice([True, False])
            )
            throwGen(match)


def throwGen(match):
    '''
    Generate throws for both teams in the match.
    2 rounds, 4 players per round, 4 throws per player per round
    '''
    season = CurrentSeason.objects.first().season
    for team in [match.home_team, match.away_team]:
        for throw_round in range(1, 3):
            for throw_turn, player in enumerate(team.players.all().order_by('?')[:4]):
                Throw.objects.create(
                    match=match,
                    player=player,
                    team=team,
                    season=season,
                    throw_turn=throw_turn + 1,
                    throw_round=throw_round,
                    score_first=random.randint(-1, 7),
                    score_second=random.randint(-1, 7),
                    score_third=random.randint(-1, 7),
                    score_fourth=random.randint(-1, 7),
                )
                # for throw_number in range(1,5):
                #     Throw.objects.create(
                #         match=match,
                #         player=player,
                #         team=team,
                #         season=season,
                #         throw_turn=throw_turn + 1,
                #         throw_number=throw_number,
                #         throw_round=throw_round,
                #         score=random.randint(-1,7)
                #     )
