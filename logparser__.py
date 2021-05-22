"""
- detect encounters
- some stats for encounters

api:
lp = LogParser('sample_logs/Network_20700_20201103.log')
fights = lp.encounters


sample logs
===========

contains an ucob fight (actually the first evening of progging ucob)
sample_logs/Network_20700_20201103.log


turns out tracking the start of a fight is indeed messy, see
https://github.com/quisquous/cactbot/blob/42e0330836568f71a3b972475689bc9daf9da67b/ui/oopsyraidsy/oopsyraidsy.js#L510

"""
from glob import glob
import logging
import datetime
import constants
import re
from constants import LogTypes, ActorControlTypes, LogLineType
import typing

from termcolor import colored

# plotting
import pandas
import seaborn as sns
import matplotlib.pyplot as plt


class Encounter:
    def __init__(self, start: datetime.datetime, duration: datetime.timedelta, fight: constants.Fights):

        if not isinstance(fight, constants.Fights):
            logging.error(f"Unknown fight {fight}")
            fight = constants.Fights.UNKNOWN
        self.fight = fight

        self.start = start
        self.duration = duration
        self.date = start.date()

    def __str__(self):
        return f'Encounter ({self.start}) [{self.duration}]'

    def __repr__(self):
        return self.__str__()


class Line:

    identifier_mapping = {
        0x00: LogTypes.LogLine,
        0x01: LogTypes.ChangeZone,
        0x02: LogTypes.ChangePrimaryPlayer,
        0x03: LogTypes.AddCombatant,
        0x0c: LogTypes.PlayerStats,
        0x0b: LogTypes.PartyList,
        0x26: LogTypes.NetworkStatusEffect,
        0x1a: LogTypes.NetworkBuff,
        0x1c: LogTypes.NetworkRaidMarker,
        0x22: LogTypes.NetworkNameToggle,
        0x27: LogTypes.NetworkUpdateHP,

        0x15: LogTypes.NetworkAbility,
        0x25: LogTypes.NetworkActionSync,
        0x14: LogTypes.NetworkStartsCasting,
        0x1e: LogTypes.NetworkBuffRemove,

        0x16: LogTypes.NetworkAOEAbility,
        0x17: LogTypes.NetworkCancelAbility,
        0x18: LogTypes.NetworkDoT,
        0x1f: LogTypes.NetworkGauge,
        0x24: LogTypes.LimitBreak,
        0x1b: LogTypes.NetworkTargetIcon,

        0x19: LogTypes.NetworkDeath,
        0x21: LogTypes.ActorControlLine,
        0x04: LogTypes.RemoveCombatant,
        0x23: LogTypes.NetworkTether,
        0xfb: LogTypes.Debug


    }

    def __init__(self, raw_line: str):
        self.raw_line = raw_line
        self.line = raw_line.split('|')
        self.identifier = int(self.line[0])

        if self.identifier in self.identifier_mapping:
            self.type = self.identifier_mapping[self.identifier]
        else:
            self.type = LogTypes.Unknown

    # use a property here to only do this (costly) conversion when needed
    @property
    def time(self) -> datetime.datetime:
        return self.extract_time(self.raw_line)

    @property
    def printable_time(self):
        return self.time.strftime("%d/%m/%y %H:%M:%S")

    @staticmethod
    def extract_time(line) -> datetime.datetime:
        date_string = re.findall(r'.*\|(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+\d{2}:00)', line)[0]
        date_string = date_string.replace('0+', '+')
        return datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f%z')

    def __str__(self):
        if self.type is not LogTypes.Unknown:
            return f'{self.type.name}: {self.raw_line}'
        else:
            return f'UNKNOWN:{self.identifier}: {self.raw_line}'


def ucob_progress_time_based(duration: datetime.timedelta):
    # todo make this generic, maybe observer pattern
    if duration > constants.enrage_time_nael_twintania:
        progress = "Golden Bahamut Prime"
    elif duration > constants.enrage_time_bahamut_prime:
        progress = "Nael/Twintania"
    elif duration > constants.enrage_time_nael:
        progress = "Bahamut Prime"
    elif duration > constants.enrage_time_twintania:
        progress = "Nael deus Darnus"
    else:
        progress = "Twintania"
    return progress


def ucob_progress(combatants: set):
    # todo make this generic, maybe observer pattern
    # todo - add nael/twintania and golden bahamut prime
    if 'Bahamut Prime' in combatants:
        progress = 'Bahamut Prime'
    elif 'Nael Deus Darnus' in combatants:
        progress = 'Nael deus Darnus'
    else:
        progress = 'Twintania'
    return progress


class ChangeZone:

    DUMMY = 'dummy'
    # can be used to detect start of fight
    instance_to_enemy = {
        'TheUnendingCoilOfBahamutUltimate': 'Twintania',
        'EdensVerseIconoclasm': 'The Idol Of Darkness',
        'EdensVerseIconoclasmSavage': 'The Idol Of Darkness',
        'EdensVerseRefulgence': 'Shiva',
        'EdensVerseRefulgenceSavage': 'Shiva',
        'DeltascapeV40Savage': 'Neo Exdeath',


        'Kugane': DUMMY,
        'other': DUMMY
    }

    def __init__(self, line: Line):
        self.id = line.line[2]
        self.ingame_name = line.line[3]
        try:
            self.name = constants.zone_ids[self.id]
        except KeyError:
            self.name = 'other'

        if self.name in self.instance_to_enemy:
            self.enemy = self.instance_to_enemy[self.name]
        else:
            self.enemy = 'idk'

    def __str__(self):
        return f"ChangeZone to {self.ingame_name}"


class ActorControlLine:
    # ucob seems to be 80037569
    def __init__(self, line: Line):
        self.line = line
        self.instance_id = line.line[2]
        try:
            self.actor_type = constants.actor_control_types_mapping[line.line[3]]
        except KeyError:
            # print(f"unknown type {line.line[3]}")
            self.actor_type = ActorControlTypes.UnknownActorControl7

    def __str__(self):
        value = f'{self.line.printable_time} {self.actor_type.name}'
        if self.actor_type is ActorControlTypes.FadeIn:
            value = colored(value, 'red')
        elif self.actor_type is ActorControlTypes.Victory:
            value = colored(value, 'green')
        return value


class NetworkDeathLine:
    """NetworkDeath: 25|2020-11-03T17:19:06.7650000+01:00|1078C8E1|Spicy Meatballs|4000F989|Idolatry||7a76805311ad075036b25d3d6ed4735e
    """

    def __init__(self, line: Line):
        self.victim = line.line[3]
        self.killer = line.line[5]
        if not self.killer:
            self.killer = '[?]'

    def __str__(self):
        return f'{self.killer} killed {self.victim}...'


class NetworkAbility:
    """From: https://github.com/quisquous/cactbot/blob/main/docs/LogGuide.md#15-networkability
    21|2020-11-03T21:41:45.1000000+01:00|106A1180|Shypai Priest|1D12|Malefic III|40015B1B|Twintania|750003|
    169B0000|1B|1D128000|0|0|0|0|0|0|0|0|0|0|0|0|5533785|5533785|10000|10000|0|1000|0|-15|0|-4.792213E-05|42687|
    42687|10000|10000|0|1000|0.8391724|11.52051|-5.960464E-08|-3.109187|00004D5E|1d883299c6c1eb50bf770cc5c9d5b8e3
    """
    def __init__(self, line: Line):
        self.line = line
        self.caster = line.line[3]
        self.ability = line.line[5]
        self.target_id = line.line[6]
        self.target = line.line[7]
        self.damage = int(int(line.line[9], 16)/(16**4))

    def __str__(self):
        return f'{self.line.printable_time} {self.caster} uses {self.ability} on {self.target_id}:{self.target}, for {self.damage} damage.'


class LogLine:

    """This refers to loglines of type 00, not any logline"""

    def __init__(self, line: Line):
        self.line = line
        try:
            self.type = LogLineType(int(line.line[2], 16))
        except ValueError:
            self.type = LogLineType.UNKNOWN

        self.id = line.line[2]
        self.origin = line.line[3]  # empty if not from player
        self.message = line.line[4]

    def __str__(self):
        # value = f'{self.type.name}: [{self.origin}] {self.message}, raw:{self.line.raw_line}'
        value = f'{self.type.name}: {self.message}, raw:{self.line.raw_line}'

        if self.type is LogLineType.PLAYERMESSAGE:
            value = f'{self.line.printable_time} {self.type.name}: [{self.origin}] {self.message}'
            value = colored(value, 'cyan')

        if self.type is LogLineType.COUNTDOWNMESSAGE and self.message == 'Engage!':
            value = colored(f'{self.line.printable_time} Engage!', 'yellow')

        return value

# not sure if this is a good idea
# class ChangeZoneLine(Line):
#     def __init__(self, line):
#         super(ChangeZoneLine, self).__init__(line)


class Fight:
    def __init__(self, start: datetime.datetime, end: datetime.datetime, location: str, status: str, combatants: set):
        self.combatants = combatants  # used to detect progress in ucob
        self.start = start
        self.end = end
        self.location = location
        self.status = status
        self.duration = self.end - self.start

        minutes = self.duration.seconds // 60
        seconds = self.duration.seconds - minutes * 60
        self.printable_duration = f'{minutes}:{seconds}'


    def __repr__(self):
        return f'{self.start.strftime("%d/%m/%y %H:%M:%S")} [{self.printable_duration}] {self.status} in {self.location}'


class LogParser:


    def __init__(self, log_path: str):
        with open(log_path, 'r', encoding='utf-8') as fo:
            self.lines = [line.strip() for line in fo.readlines()]
        self.log_path = log_path

        # for i, line in enumerate(self.lines[338027-15+1751:338027+6000]):

    def extract_fights(self) -> typing.List[Fight]:

        # for i, line in enumerate(self.lines[338027-5:338027+4000]):

        in_fight = False
        fight_start = None
        fight_location = None
        fights = []
        fight_combatants = set()
        zone = None

        for i, line in enumerate(self.lines):
            l = Line(line)

            # detect instance -
            #  TODO use this to distinguish between multiple battles featuring the same enemies, such as e7s and e7
            if l.type is LogTypes.ChangeZone:
                zone = ChangeZone(l)

            # detect start of fight
            if l.type is LogTypes.NetworkAbility and not in_fight:
                na = NetworkAbility(l)

                if na.target in constants.object_ids:
                    fight_combatants = set()
                    # fight_location = constants.object_ids[na.target]
                    fight_location = zone.name
                    in_fight = True
                    fight_start = na.line.time

                # players start with '10', enemies with '40'
                elif na.target_id.startswith('40') and na.target:
                    pass
                    # print(f'unknown enemy {na.target} with id {na.target_id} in zone {zone.name if zone else None}')

            # list all combatants
            if l.type is LogTypes.NetworkAbility:
                na = NetworkAbility(l)
                fight_combatants.add(na.target)

            # detect end of fight
            elif l.type is LogTypes.ActorControlLine and in_fight:
                acl = ActorControlLine(l)
                if acl.actor_type in [ActorControlTypes.FadeIn, ActorControlTypes.Victory]:  # wipe or victory
                    fight_end = acl.line.time
                    status = 'Victory' if acl.actor_type is ActorControlTypes.Victory else 'Wipe'
                    fight = Fight(fight_start, fight_end, fight_location, status, combatants=fight_combatants)
                    print(f'{fight} with {fight_combatants}')
                    in_fight = False
                    fights.append(fight)

        # fights = [fight for fight in fights if fight.location == 'UCoB']
        return fights


def visualize(encounters: typing.List[Fight]):
    durations = [encounter.duration.seconds for encounter in encounters]

    data = {
        'duration': durations,
        'date': [encounter.start.date() for encounter in encounters]
    }

    if all([e.location == 'TheUnendingCoilOfBahamutUltimate' for e in encounters]):
        data['progress'] = [ucob_progress(e.combatants) for e in encounters]

    data = pandas.DataFrame(data=data)
    sns.set_theme()
    sns.set_style('ticks')
    if 'progress' in data:
        g = sns.scatterplot(y='duration', x=data.index, data=data, hue='progress')
    else:
        g = sns.scatterplot(y='duration', x=data.index, data=data)

    g.set(xlabel='pull number', ylabel='duration (in seconds)')
    plt.show()


def export_to_csv(encounters: typing.List[Fight], path="most_recent.csv"):
    """
    Creates something like
    Twintania,25,35,44,44,12,26,,46,9,28,90,56,50,87,40
    Nael,,,,,,,150,,,,,,,,,,,,,,,,,

    :param encounters:
    :param path:
    :return:
    """

    if not all([e.location == 'TheUnendingCoilOfBahamutUltimate' for e in encounters]):
        raise NotImplementedError('only ucob is supported atm')

    data = {
        'duration': [encounter.duration.seconds for encounter in encounters],
        'progress': [ucob_progress(e.combatants) for e in encounters]
    }

    phases = ["Twintania", "Nael deus Darnus", "Bahamut Prime", "Nael and Twintania", "Golden Bahamut Prime"]

    csv_lines = [p + "," for p in phases] + ["pull number, "]
    pull_number = 0
    for duration, progress in zip(data['duration'], data['progress']):

        for i, phase in enumerate(phases):
            if progress == phase:
                csv_lines[i] += str(duration) + ","
            else:
                csv_lines[i] += ","
        csv_lines[5] += f'{pull_number},'
        pull_number += 1

    for i, line in enumerate(csv_lines):
        csv_lines[i] = line + "\n"

    with open(path, 'w') as fo:
        fo.writelines(csv_lines)


if __name__ == '__main__':
    # lp = LogParser(r'sample_logs/Network_20700_20201103.log')
    # visualize([f for f in lp.extract_fights() if f.location == 'TheUnendingCoilOfBahamutUltimate'])

    all_encounters = []
    for log_path in glob('new_ucob/*.log'):
    # for log_path in glob('sample_logs/*.log'):
    #for log_path in glob('new_ucob/*419.log'):
        print(log_path)
        all_encounters += LogParser(log_path).extract_fights()

    all_encounters = [f for f in all_encounters if f.location == 'TheUnendingCoilOfBahamutUltimate']
    # print(all_encounters)
    visualize(all_encounters)
    export_to_csv(all_encounters)
