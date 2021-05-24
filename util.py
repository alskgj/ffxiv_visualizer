
import json

import constants


def is_first_boss(zone_name: str, boss_name: str):
    """
    Given a zone_name and a boss_name returns true if the boss_name, can
    be used to detect the beginning of a fight.

    Uses both the constants.first_boss_per_zone as source of truth and the
    generated table from data/first_boss.json as fallback.

    >>> is_first_boss("Eden's Verse: Fulmination", 'Ramuh')
    True

    :return bool: Returns whether boss_name can be used to detect the beginning of the fight
    """
    table = constants.manual_bosses_per_zone
    with open('data/first_boss.json') as fo:
        fallback = json.load(fo)
    if zone_name in table and boss_name in table[zone_name]:
        return True
    if zone_name in fallback and boss_name in fallback[zone_name]:
        return True
    return False
