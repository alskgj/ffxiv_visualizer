"""
    modules.uwu
    ===========

    functions specific to uwu
"""


def uwu_progress(combatants: set):
    if 'Titan' in combatants:
        progress = 'Titan'
    elif 'Ifrit' in combatants:
        progress = 'Ifrit'
    else:
        progress = 'Garuda'
    return progress
