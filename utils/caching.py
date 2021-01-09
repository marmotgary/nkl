from django.core.cache import cache
# TODO: Figure out why this causes a import loop?
# from kyykka.models import Season, CurrentSeason

def getFromCache(key, season_year = None):
    # print("Get cache", key)
    # print(cache.get(key))
    if season_year:
        key = key + "_" + str(season_year)
    return cache.get(key)


def setToCache(key, value, timeout=60 * 60 * 12, season_year=""):
    # print("Set cache", key)
    if value is None:
        value = 0
    if season_year:
        key = key + "_" + str(season_year)
    cache.set(key, value, timeout)


def reset_player_cache(player, season_year):
    # Called after a throw is saved, can only be current season
    caches = [
        'player_' + str(player.id) + '_score_total' + season_year,
        'player_' + str(player.id) + '_match_count' + season_year,
        'player_' + str(player.id) + '_rounds_total' + season_year,
        'player_' + str(player.id) + '_pikes_total' + season_year,
        'player_' + str(player.id) + '_zeros_total' + season_year,
        'player_' + str(player.id) + '_gteSix_total' + season_year,
        'player_' + str(player.id) + '_throws_total' + season_year,
        'player_' + str(player.id) + '_pike_percentage' + season_year,
        'player_' + str(player.id) + '_score_per_throw' + season_year,
        'player_' + str(player.id) + '_avg_throw_turn' + season_year,
    ]
    cache.delete_many(caches)


def reset_match_cache(match):
    """
    If the match is validated, stats of teams and players are affected as well.
    """
    caches = [
        'match_' + str(match.id) + '_home_score_total',
        'match_' + str(match.id) + '_away_score_total',
        'all_matches',
        'all_teams',
        'all_players',
    ]
    cache.delete_many(caches)


def cache_reset_key(key):
    cache.delete(key)
