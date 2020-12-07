from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from kyykka.models import Season, CurrentSeason, Match, Team, Player, PlayersInTeam, Throw
from kyykka.serializers import MatchListSerializer
import datetime, json
from django.test import override_settings


class UserRegistration(APITestCase):
    """ Test user registration """

    def test_user_registration_success(self):
        url = reverse("register")
        data = {'username': '1@test.account',
                'first_name': 'Test',
                'last_name': 'Account',
                'password': 'password',
                'number': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, '1@test.account')
        self.assertEqual(User.objects.get().first_name, 'Test')
        self.assertEqual(User.objects.get().last_name, 'Account')
        self.assertEqual(User.objects.get().player.number, str(1))

    def test_user_registration_duplicate_email(self):
        url = reverse("register")
        data = {'username': '1@test.account',
                'first_name': 'Test',
                'last_name': 'Account',
                'password': 'password',
                'number': 1}
        self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incorrect_email(self):
        url = reverse("register")
        data = {'username': 'not_email',
                'first_name': 'Test',
                'last_name': 'Account',
                'password': 'password',
                'number': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_string_as_number(self):
        url = reverse("register")
        data = {'username': '1@test.account',
                'first_name': 'Test',
                'last_name': 'Account',
                'password': 'password',
                'number': 'ab'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_large_number(self):
        url = reverse("register")
        data = {'username': '1@test.account',
                'first_name': 'Test',
                'last_name': 'Account',
                'password': 'password',
                'number': 123}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        


class PlayerReservation(APITestCase):
    """ Test player reservation API """

    def setUp(self):
        Season.objects.create(year=2020)
        season = Season.objects.create(year=2021)
        CurrentSeason.objects.create(season = season)
        team1 = Team.objects.create(name="Team 1", abbreviation="T1")
        team2 = Team.objects.create(name="Team 2", abbreviation="T2")
        User.objects.create_superuser('test', '', 'test')
        user1 = User.objects.create_user("email1", "email1", "password")
        user2 = User.objects.create_user("email2", "email2", "password")
        user3 = User.objects.create_user("email3", "email3", "password")
        user4 = User.objects.create_user("email4", "email4", "password")

        user1.first_name = "Captain"
        PlayersInTeam.objects.create(season=CurrentSeason.objects.first().season,
                                    team=team1, player=user1, is_captain=True)
        PlayersInTeam.objects.create(season=CurrentSeason.objects.first().season,
                                    team=team1, player=user2, is_captain=False)
        PlayersInTeam.objects.create(season=CurrentSeason.objects.first().season,
                                    team=team2, player=user4, is_captain=False)

    def test_get_reservation_list(self):
        url = reverse("reserve")
        self.client.login(username='email1', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(is_superuser=False).count(), len(response.data))

    def test_captain_reserve(self):
        url = reverse("reserve")
        data = {"player": User.objects.get(email="email3").id}
        self.client.login(username='email1', password='password')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_captain_reserve_reserved(self):
        url = reverse("reserve")
        data = {"player": User.objects.get(email="email4").id}
        self.client.login(username='email1', password='password')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_captain_reserve(self):
        url = reverse("reserve")
        data = {"player": User.objects.get(email="email3").id}
        self.client.login(username='email2', password='password')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class Stats(APITestCase):
    """ Test stats """

    TEST_CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
    }

    def setUp(self):
        Season.objects.create(year=2020)
        currentSeason = Season.objects.create(year=2021)
        CurrentSeason.objects.create(season = currentSeason)
        team1 = Team.objects.create(name="Team 1", abbreviation="T1")
        team2 = Team.objects.create(name="Team 2", abbreviation="T2")

        user1 = User.objects.create_user("test@captain.1", "test@captain.1", "password")
        PlayersInTeam.objects.create(season=currentSeason,
                                    team=team1, player=user1, is_captain=True)
        user2 = User.objects.create_user("test@captain.2", "test@captain.2", "password")
        PlayersInTeam.objects.create(season=currentSeason,
                                    team=team2, player=user2, is_captain=True)

        for i in range (1,9):
            u = User.objects.create_user("test@user."+str(i), "test@user."+str(i), "password")
            if i < 5:
                team = team1
            else:
                team = team2
            PlayersInTeam.objects.create(season=currentSeason,
                                    team=team, player=u, is_captain=False)
        match1 = Match.objects.create(
            season=currentSeason,
            match_time=datetime.datetime(2021, 1, 1, 19, 30),
            field=1,
            home_team=team1,
            away_team=team2,
            home_first_round_score=50,
            home_second_round_score=50,
            away_first_round_score=50,
            away_second_round_score=50,
            is_validated=True
        )
        match2 = Match.objects.create(
            season=currentSeason,
            match_time=datetime.datetime(2021, 1, 2, 19, 30),
            field=1,
            home_team=team2,
            away_team=team1,
            home_first_round_score=50,
            home_second_round_score=50,
            away_first_round_score=50,
            away_second_round_score=50,
            is_validated=True
        )
        for round in range(1,3):
            for turn in range(1,5):
                player = User.objects.get(email="test@user."+str(turn))
                Throw.objects.create(
                    match=match1,
                    player=player,
                    team=team1,
                    season=currentSeason,
                    throw_round=round,
                    throw_turn=turn,
                    score_first="h",
                    score_second=0,
                    score_third=1,
                    score_fourth=2
                )

    @override_settings(CACHES=TEST_CACHES)
    def test_pikes_from_player_list(self):
        url = reverse("player-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(is_superuser=False).count(), len(response.data))
        self.assertEqual(response.data[2]["pikes_total"], 2)

    @override_settings(CACHES=TEST_CACHES)
    def test_pikes_from_player_detail(self):
        player = User.objects.get(email="test@user.1")
        url = "/api/players/"+str(player.id)+"/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pikes_total"], 2)

    @override_settings(CACHES=TEST_CACHES)
    def test_pikes_from_team_page(self):
        player = User.objects.get(email="test@user.1")
        url = "/api/teams/"+str(Team.objects.get(name="Team 1").id)+"/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pikes_total"], 8)
        for p in response.data["players"]:
            if p["id"] == player.id:
                self.assertEqual(int(p["pikes_total"]), 2)



# class GetAllMatches(APITestCase):
#     """ Test module for GET MatchList API  """

#     def setUp(self):
#         Team.objects.create(name="Team 1", abbreviation="T1")
#         Team.objects.create(name="Team 2", abbreviation="T2")
#         Match.objects.create()
#         Match.objects.create()
#         Match.objects.create()

#     def testGetAllMatches(self):
#         response = self.client.get(reverse('matches-list'))
#         matches = Match.objects.all()
#         serializer = MatchListSerializer(matches, many=True)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


