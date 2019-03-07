from faker import Faker
from django.contrib.auth.models import User
from kyykka.models import Team, Season, PlayersInTeam, CurrentSeason

fake = Faker('fi_FI')

def initGen():
    '''
    Generates dummy Seasons, Teams and populates teams with Users.
    Create superuser with credentials 'test test'
    '''
    User.objects.create_superuser('test', '', 'test')
    seasonGen()
    teamGen(10)

def seasonGen(amount=3):
    print('Generating seasons\n')
    year = 2019
    for _ in range(amount):
        season = Season.objects.create(year=year)
        if year == 2019:
            CurrentSeason.objects.create(season=season)
        year = year - 1
        print(year)

# Generate Users
def userGen(amount, return_users=False):
    users = []
    for _ in range(amount):
        try:
            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            user = User.objects.create_user(email, email, 'test')
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            users.append(user)
            print(first_name, last_name, email)
        except:
            pass
    if return_users:
        return users

def teamGen(amount):
    print('Generating fake teams\n')
    for i in range(amount):
        try:
            name = fake.company()
            abbreviation = fake.company_suffix()
            team = Team.objects.create(name=name, abbreviation=abbreviation)
        except:
            name = fake.ean13()
            abbreviation = fake.ean8()
            team = Team.objects.create(name=name, abbreviation=abbreviation)
            pass
        print('\n Generated team', name, abbreviation, '\n')
        populateTeam(team)

def populateTeam(team):
    print('Generating fake userse for team ', team)
    players = userGen(6, True)
    season = CurrentSeason.objects.first().season
    PlayersInTeam.objects.create(season=season, team=team, player=players.pop(), is_captain=True)
    for p in players:
        PlayersInTeam.objects.create(season=season, team=team, player=p)
