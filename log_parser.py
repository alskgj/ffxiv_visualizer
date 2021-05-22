"""

    log_parser.py
    =============

    this module contains classes for parsing log files generated with
    ACT (Advanced Combat Tracker).
    Much of the information used is from:
    https://github.com/quisquous/cactbot/blob/main/docs/LogGuide.md

"""


from constants import LogTypes, ActorControlTypes
import typing
import datetime
import re
import constants
from termcolor import colored


class Fight:
    def __init__(self, start: datetime.datetime, end: datetime.datetime, location: str, status: str, combatants: set):
        self.combatants = combatants  # used to detect progress in ucob
        if '' in self.combatants:
            self.combatants.remove('')
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
        try:
            self.identifier = int(self.line[0])
        except ValueError:
            # this seems to happen rarely - maybe race conditions?
            # todo - do I need to do some error handling here?
            self.identifier = 9999

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

class NetworkAbility:
    """From: https://github.com/quisquous/cactbot/blob/main/docs/LogGuide.md#15-networkability
    21|2020-11-03T21:41:45.1000000+01:00|106A1180|Shypai Priest|1D12|Malefic III|40015B1B|Twintania|750003|
    169B0000|1B|1D128000|0|0|0|0|0|0|0|0|0|0|0|0|5533785|5533785|10000|10000|0|1000|0|-15|0|-4.792213E-05|42687|
    42687|10000|10000|0|1000|0.8391724|11.52051|-5.960464E-08|-3.109187|00004D5E|1d883299c6c1eb50bf770cc5c9d5b8e3
    """
    def __init__(self, line: Line):
        if len(line.line) != 47:
            raise NotImplementedError("Malformed line")

        self.line = line
        self.caster = line.line[3]
        self.ability = line.line[5]
        self.target_id = line.line[6]
        self.target = line.line[7]

        try:
            self.damage = int(int(line.line[9], 16)/(16**4))
        except ValueError:
            self.damage = 1
        except IndexError:
            self.damage = 2

    def __str__(self):
        return f'{self.line.printable_time} {self.caster} uses {self.ability} on {self.target_id}:{self.target}, for {self.damage} damage.'

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


class LogParser:

    def __init__(self, log_path: str):
        try:
            with open(log_path, 'r', encoding='latin-1') as fo:
                self.lines = [line.strip() for line in fo.readlines()]
        except UnicodeDecodeError as UDE:
            print(f"Got an UnicodeDecodeError handling {log_path}")
            self.lines = []
            raise UDE
        self.log_path = log_path

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
                try:
                    na = NetworkAbility(l)
                except NotImplementedError:
                    # malformed line
                    continue

                if na.target in constants.object_ids:
                    fight_combatants = set()
                    # fight_location = constants.object_ids[na.target]
                    fight_location = zone.name
                    in_fight = True
                    fight_start = na.line.time

                # players start with '10', enemies with '40'
                elif na.target_id.startswith('40') and na.target:
                    # print(f'unknown enemy {na.target} with id {na.target_id} in zone {zone.name if zone else None}')
                    pass

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
                    # print(f'{fight} with {fight_combatants}')
                    in_fight = False
                    fights.append(fight)
                    fight_combatants = set()


        # fights = [fight for fight in fights if fight.location == 'UCoB']
        return fights
