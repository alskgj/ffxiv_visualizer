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


def find_slices(lines):
    in_instance = 0
    slices = []
    current_start = 0
    for i, line in enumerate(lines):

        if re.match(constants.e12s['start_pattern'], line) and in_instance == 0:
            in_instance, current_start = 1, i

        elif in_instance and line.startswith('01|'):
            in_instance = 0
            slices.append((current_start, i))

    return slices


class Encounter:
    def __init__(self, start: datetime.datetime, duration: datetime.timedelta, phase, progress):
        self.start = start
        self.duration = duration
        self.date = start.date()
        self.phase = phase
        self.progress = progress

    def __str__(self):
        return f'Encounter ({self.start}) [{self.duration}]'

    def __repr__(self):
        return self.__str__()

def extract_time(line) -> datetime.datetime:
    date_string = re.findall(r'.*\|(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+\d{2}:00)', line)[0]
    date_string = date_string.replace('0+', '+')
    return datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f%z')


def extract_fights(lines, slices) -> typing.List[Encounter]:

    in_fight, start = False, None
    encounters = []

    for start, end in slices:
        phase = 2
        for line in lines[start:end]:
            # there are some fights which don't have that line, but they are super short -
            # maybe those are fights where the logger was dead before they started?
            if 'Engage!' in line:
                in_fight = True
                start = extract_time(line)

            if "Eden's Promise" in line:
                phase = 1

            if in_fight and str(constants.ACTOR_CONTROL_LINES_WIPE) in line:
                in_fight = False
                fight_duration = extract_time(line) - start
                encounters.append(Encounter(start, fight_duration, phase=phase, progress='wipe'))
                phase = 2

            elif str(constants.ACTOR_CONTROL_LINES_WIPE) in line:
                start = extract_time(line)
                in_fight = False

            elif in_fight and "40000003" in line: # win
                in_fight = False
                fight_duration = extract_time(line) - start
                encounters.append(Encounter(start, fight_duration, phase=phase, progress='clear'))
                phase = 2

            elif "Eden's Promise uses Thrum of Discord." in line: # win
                in_fight = False
                fight_duration = extract_time(line) - start
                encounters.append(Encounter(start, fight_duration, phase=phase, progress='clear'))
                phase = 2

            elif "40000003" in line:
                print('hmm', line)

    return encounters


def visualize(encounters: typing.List[Encounter]):
    durations = [encounter.duration.seconds for encounter in encounters]


    data = {
        'duration': durations,
        'progress': [encounter.progress for encounter in encounters],
        'date': [encounter.date for encounter in encounters]
    }

    print(data['duration'])


    data = pandas.DataFrame(data=data)
    sns.set_theme()
    sns.set_style('ticks')
    g = sns.scatterplot(y='duration', hue='progress', x=data.index, data=data)
    g.set(xlabel='pull number', ylabel='duration (in seconds)')
    plt.show()


if __name__ == '__main__':

    all_fights = []
    #for log_path in glob('e12s logs/Network_20707_20210119.log'):
    for log_path in glob('short_e12s logs/*.log'):

        with open(log_path, encoding='utf-8') as fo:
            lines = [l.strip() for l in fo.readlines()]

            slices = find_slices(lines)

            fights = extract_fights(lines, slices)
            # if any([f.duration.seconds > 490 for f in fights]):
            #     print(log_path)
            all_fights += fights

    print(visualize([fight for fight in all_fights if fight.phase == 1]))
    print(len([fight for fight in all_fights if fight.phase == 2]))


