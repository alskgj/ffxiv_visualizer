import constants

import typing
from glob import glob

# parsing
import re
import datetime

# plotting
import pandas
import seaborn as sns
import matplotlib.pyplot as plt


class NetworkDeath:
    def __init__(self, raw_line):
        line = raw_line.split('|')
        if line[0] != '25':
            print("faulty network death line...")
            self.victim = None
            self.killer = None
            self.datetime = None
            return

        self.victim = line[3]
        self.killer = constants.kill_mechanics[line[5]]
        self.datetime = Parser.extract_time(raw_line)

    def __str__(self):
        return f'{self.victim} was killed by {self.killer}'



class Encounter:
    def __init__(self, start: datetime.datetime, duration: datetime.timedelta, kill_count: dict):
        self.start = start
        self.duration = duration
        self.date = start.date()
        self.kill_count = kill_count

        if self.duration > constants.enrage_time_nael_twintania:
            self.progress = "Golden Bahamut Prime"
        elif self.duration > constants.enrage_time_bahamut_prime:
            self.progress = "Nael/Twintania"
        elif self.duration > constants.enrage_time_nael:
            self.progress = "Bahamut Prime"
        elif self.duration > constants.enrage_time_twintania:
            self.progress = "Nael deus Darnus"
        else:
            self.progress = "Twintania"

    def __str__(self):
        return f'Encounter ({self.start}) [{self.duration}]'

    def __repr__(self):
        return self.__str__()


class Parser:
    def __init__(self, path):
        with open(path, 'r', encoding='utf-8') as fo:
            self.lines = [line.strip() for line in fo.readlines()]

    def find_slices(self):
        slices = []
        in_ucob = False
        current_start = -1
        for i, line in enumerate(self.lines):
            if re.match(r'01\|.+the Unending Coil of Bahamut \(Ultimate\)\|', line):
                print(line)
                in_ucob, current_start = True, i
            elif in_ucob and line.startswith('01|'):
                in_ucob = False
                slices.append((current_start, i))
        return slices

    @staticmethod
    def extract_time(line) -> datetime.datetime:
        date_string = re.findall(r'.*\|(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+\d{2}:00)', line)[0]
        date_string = date_string.replace('0+', '+')
        return datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f%z')

    def extract_fights(self) -> typing.List[Encounter]:

        # ensure we only parse ucob fights
        slices = self.find_slices()
        in_fight, start = False, None
        encounters = []
        kill_count = {}
        for start, end in slices:
            for line in self.lines[start:end]:
                # there are some fights which don't have that line, but they are super short -
                # maybe those are fights where the logger was dead before they started?
                if not in_fight and 'Engage!' in line:
                    in_fight = True
                    start = self.extract_time(line)

                if in_fight and line.startswith(f'{constants.NetworkDeath}|'):
                    death = NetworkDeath(line)
                    if death.killer == 'Edge of the map':
                        continue

                    if death.killer not in kill_count:
                        kill_count[death.killer] = 1
                    else:
                        kill_count[death.killer] += 1

                # yields the same (incomplete data) as parsing NetworkDeaths
                # if in_fight and line.startswith('00|') and 'defeated' in line:
                #     print(line)

                if in_fight and str(constants.ACTOR_CONTROL_LINES_WIPE) in line:
                    in_fight = False
                    fight_duration = self.extract_time(line) - start
                    encounters.append(Encounter(start, fight_duration, kill_count))
                    kill_count = {}  # reset killcount



        return encounters


def visualize(encounters: typing.List[Encounter]):
    durations = [encounter.duration.seconds for encounter in encounters]
    progress = [encounter.progress for encounter in encounters]

    data = {
        'duration': durations,
        'progress': progress,
        'date': [encounter.date for encounter in encounters]
    }



    data = pandas.DataFrame(data=data)
    sns.set_theme()
    sns.set_style('ticks')
    g = sns.scatterplot(y='duration', x=data.index, data=data, hue='progress')
    g.set(xlabel='pull number', ylabel='duration (in seconds)')
    plt.show()


if __name__ == '__main__':

    all_encounters = []
    for log_path in glob('sample_logs/*.log'):
        all_encounters += Parser(log_path).extract_fights()

    visualize(all_encounters)