from django.core.cache import cache


def getFromCache(key):
    print("Get cache", key)
    # print(cache.get(key))
    return cache.get(key)


def setToCache(key, value, timeout=3600):
    # print("Set cache", key)
    if value is None:
        value = 0
    cache.set(key, value, timeout)


def reset_player_cache(player):
    caches = [
        'player_' + str(player.id) + '_score_total',
        'player_' + str(player.id) + '_match_count',
        'player_' + str(player.id) + '_rounds_total',
        'player_' + str(player.id) + '_pikes_total',
        'player_' + str(player.id) + '_zeros_total',
        'player_' + str(player.id) + '_gteSix_total',
        'player_' + str(player.id) + '_throws_total',
        'player_' + str(player.id) + '_pike_percentage'
        'player_' + str(player.id) + '_score_per_throw'
        'player_' + str(player.id) + '_avg_throw_turn'
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