from django.core.cache import cache
# TODO: Figure out why this causes a import loop?
# from kyykka.models import Season, CurrentSeason

def getFromCache(key, season_year = None):
    if season_year:
        key = key + "_" + str(season_year)
    # print("Get cache", key)
    # print(cache.get(key))
    return cache.get(key)


def setToCache(key, value, timeout=60 * 60 * 12, season_year=""):
    if value is None:
        value = 0
    if season_year:
        key = key + "_" + str(season_year)
    # print("Set cache", key)
    cache.set(key, value, timeout)


def reset_player_cache(player, season_year):
    """
    Resets all player_ caches for specified season
    """
    caches = [
        'player_' + str(player.id) + '_score_total_' + season_year,
        'player_' + str(player.id) + '_match_count_' + season_year,
        'player_' + str(player.id) + '_rounds_total_' + season_year,
        'player_' + str(player.id) + '_pikes_total_' + season_year,
        'player_' + str(player.id) + '_zeros_total_' + season_year,
        'player_' + str(player.id) + '_gteSix_total_' + season_year,
        'player_' + str(player.id) + '_throws_total_' + season_year,
        'player_' + str(player.id) + '_pike_percentage_' + season_year,
        'player_' + str(player.id) + '_score_per_throw_' + season_year,
        'player_' + str(player.id) + '_avg_throw_turn_' + season_year,
    ]
    # print(caches)
    cache.delete_many(caches)


def reset_match_cache(match, season_year = ""):
    """
    If the match is validated, stats of teams and players are affected as well.
    """
    caches = [
        'match_' + str(match.id) + '_home_score_total',
        'match_' + str(match.id) + '_away_score_total',
        'all_matches_' + season_year,
        'all_teams_' + season_year,
        'all_players_' + season_year,
    ]
    # print(caches)
    cache.delete_many(caches)


def cache_reset_key(key):
    cache.delete(key)
