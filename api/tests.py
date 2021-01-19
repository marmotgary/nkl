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
        self.assertEqual(response.data["success"], True)
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
        

class UserLogin(APITestCase):
    """ Test user login"""

    def setUp(self):
        season = Season.objects.create(year=2021)
        CurrentSeason.objects.create(season = season)
        team1 = Team.objects.create(name="Team 1", abbreviation="T1")
        team2 = Team.objects.create(name="Team 2", abbreviation="T2")
        user1 = User.objects.create_user("email1", "email1", "password")
        user2 = User.objects.create_user("email2", "email2", "password")
        user3 = User.objects.create_user("email3", "email3", "password")
        user4 = User.objects.create_user("email4", "email4", "password")

        user1.first_name = "Mr."
        user1.last_name = "Captain"
        Player.objects.create(user=user1, number=1)

        PlayersInTeam.objects.create(season=CurrentSeason.objects.first().season,
                                    team=team1, player=user1, is_captain=True)
        PlayersInTeam.objects.create(season=CurrentSeason.objects.first().season,
                                    team=team1, player=user2, is_captain=False)

    def test_login_captain(self):
        CAPTAIN_ROLE = "1"
        user = User.objects.get(username="email1")
        
        team = Team.objects.get(name="Team 1")
        url = reverse("login")
        data = {"username": "email1",
                "password": "password"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CAPTAIN_ROLE, response.data["role"])
        self.assertEqual(team.id, response.data["team_id"])
        self.assertEqual(user.player.number, response.data["user"]["player_number"])
        
    def test_login_user(self):
        USER_ROLE = "0"
        user = User.objects.get(username="email2")
        
        team = Team.objects.get(name="Team 1")
        url = reverse("login")
        data = {"username": "email2",
                "password": "password"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(USER_ROLE, response.data["role"])
        self.assertEqual(team.id, response.data["team_id"])

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
        self.assertEqual(response.data["success"], True)

    def test_captain_reserve_reserved(self):
        url = reverse("reserve")
        data = {"player": User.objects.get(email="email4").id}
        self.client.login(username='email1', password='password')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reserve_as_not_captain(self):
        url = reverse("reserve")
        data = {"player": User.objects.get(email="email3").id}
        self.client.login(username='email2', password='password')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PikeCountInStats(APITestCase):
    """ Verify that pikes are counted and shown correctly in stats """

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
                    score_fourth="e"
                )

    @override_settings(CACHES=TEST_CACHES)
    def test_pikes_from_player_list(self):
        url = reverse("player-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(is_superuser=False).count(), len(response.data))
        self.assertEqual(response.data[2]["pikes_total"], 2)

    # @override_settings(CACHES=TEST_CACHES)
    # def test_pikes_from_player_detail(self):
        # player = User.objects.get(email="test@user.1")
        # url = "/api/players/"+str(player.id)+"/"
        # response = self.client.get(url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data["pikes_total"], 2)

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


class SixCountInStats(APITestCase):
    """ Verify that sixes are counted and shown correctly in stats """

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

        match1 = Match.objects.create(
            season=currentSeason,
            match_time=datetime.datetime.now(),
            home_team=team1,
            away_team=team2,
            is_validated=True
        )
        match2 = Match.objects.create(
            season=currentSeason,
            match_time=datetime.datetime.now(),
            home_team=team2,
            away_team=team1,
            is_validated=True
        )
        match3 = Match.objects.create(
            season=currentSeason,
            match_time=datetime.datetime.now(),
            home_team=team2,
            away_team=team1,
            is_validated=False
        )
        # Generate exactly 8 legal sixes.
        Throw.objects.create(
                    match=match1, player=user1, team=team1, season=currentSeason, throw_round=1,
                    throw_turn=1, score_first=6, score_second=7, score_third='h', score_fourth='e'
        )
        Throw.objects.create(
                    match=match1, player=user1, team=team1, season=currentSeason, throw_round=2,
                    throw_turn=4, score_third=8, score_fourth=9
        )
        Throw.objects.create(
                    match=match2, player=user1, team=team1, season=currentSeason, throw_round=1,
                    throw_turn=1, score_first=6, score_second=7, score_third=8, score_fourth=9
        )
        # Match not validated, these sixes should not show up in stats
        Throw.objects.create(
                    match=match3, player=user1, team=team1, season=currentSeason, throw_round=1,
                    throw_turn=1, score_first=6, score_second=7, score_third="e"
        )
           


    @override_settings(CACHES=TEST_CACHES)
    def test_sixes_from_player_list(self):
        url = reverse("player-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["gteSix_total"], 8)

    # @override_settings(CACHES=TEST_CACHES)
    # def test_sixes_from_player_detail(self):
        # player = User.objects.get(email="test@captain.1")
        # url = "/api/players/"+str(player.id)+"/"
        # response = self.client.get(url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data["gteSix_total"], 8)

    @override_settings(CACHES=TEST_CACHES)
    def test_sixes_from_team_page(self):
        player = User.objects.get(email="test@captain.1")
        url = "/api/teams/"+str(Team.objects.get(name="Team 1").id)+"/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["gteSix_total"], 8)
        for p in response.data["players"]:
            if p["id"] == player.id:
                self.assertEqual(int(p["gteSix_total"]), 8)


class GetStatsWhenNoThrows(APITestCase):
    """ Verify that API behaves as expected when no throw objects are not associated to user """

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


    @override_settings(CACHES=TEST_CACHES)
    def test_get_player_list(self):
        url = reverse("player-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["score_total"], 0)
        self.assertEqual(response.data[0]["rounds_total"], 0)
        self.assertEqual(response.data[0]["pikes_total"], 0)
        self.assertEqual(response.data[0]["zeros_total"], 0)
        self.assertEqual(response.data[0]["gteSix_total"], 0)
        self.assertEqual(response.data[0]["throws_total"], 0)
        self.assertEqual(response.data[0]["pike_percentage"], 0)
        self.assertEqual(response.data[0]["score_per_throw"], 0)
        # self.assertEqual(response.data[0]["scaled_points"], 0)
        # self.assertEqual(response.data[0]["scaled_points_per_round"], 0)
        self.assertEqual(response.data[0]["avg_throw_turn"], 0)

    @override_settings(CACHES=TEST_CACHES)
    def test_get_team(self):
        player = User.objects.get(email="test@captain.1")
        url = "/api/teams/"+str(Team.objects.get(name="Team 1").id)+"/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["score_total"], 0)
        self.assertEqual(response.data["match_count"], 0)
        self.assertEqual(response.data["pikes_total"], 0)
        self.assertEqual(response.data["zeros_total"], 0)
        self.assertEqual(response.data["zero_first_throw_total"], 0)
        self.assertEqual(response.data["pike_first_throw_total"], 0)
        self.assertEqual(response.data["throws_total"], 0)
        self.assertEqual(response.data["gteSix_total"], 0)
        self.assertEqual(response.data["pike_percentage"], 0)
        self.assertEqual(response.data["zero_percentage"], 0)
        self.assertEqual(response.data["score_per_throw"], 0)
        for p in response.data["players"]:
            if p["id"] == player.id:
                self.assertEqual(int(p["gteSix_total"]), 0)

    # @override_settings(CACHES=TEST_CACHES)
    # def test_get_player_detail(self):
    #     player = User.objects.get(email="test@captain.1")
    #     url = "/api/players/"+str(player.id)+"/"
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data["score_total"], 0)
    #     self.assertEqual(response.data["match_count"], 0)
    #     self.assertEqual(response.data["rounds_total"], 0)
    #     self.assertEqual(response.data["zeros_total"], 0)
    #     self.assertEqual(response.data["ones_total"], 0)
    #     self.assertEqual(response.data["twos_total"], 0)
    #     self.assertEqual(response.data["threes_total"], 0)
    #     self.assertEqual(response.data["fours_total"], 0)
    #     self.assertEqual(response.data["fives_total"], 0)
    #     self.assertEqual(response.data["gteSix_total"], 0)
    #     self.assertEqual(response.data["pikes_total"], 0)
    #     self.assertEqual(response.data["throws_total"], 0)
    #     self.assertEqual(response.data["pike_percentage"], 0)
    #     self.assertEqual(response.data["zero_percentage"], 0)
    #     self.assertEqual(response.data["score_per_throw"], 0)
    #     self.assertEqual(response.data["avg_throw_turn"], 0)
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


