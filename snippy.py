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
    start_line = 0
    phase_1_slices = []
    phase_2_slices = []
    for i, line in enumerate(lines):

        # if line.startswith('01|'):
        #     print(i, line)

        if re.match(constants.e12s['start_pattern'], line) and in_instance == 0:
            in_instance, current_start = 1, i
            start_line = i

        elif re.match(constants.e12s['start_pattern'], line) and in_instance == 1:
            in_instance, current_start = 2, i
            phase_1_slices.append((start_line, i))
            start_line = i


        elif in_instance and line.startswith('01|'):

            slice = (start_line, i)
            start_line = i
            if in_instance == 1:
                phase_1_slices.append(slice)
            elif in_instance == 2:
                phase_2_slices.append(slice)

            in_instance = False

    return {
        'p1': phase_1_slices,
        'p2': phase_2_slices
    }

class Encounter:
    def __init__(self, start: datetime.datetime, duration: datetime.timedelta, progress):
        self.start = start
        self.duration = duration
        self.date = start.date()
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
    # ensure we only parse ucob fights
    in_fight, start = False, None
    encounters = []
    kill_count = {}
    for start, end in slices:
        for line in lines[start:end]:
            # there are some fights which don't have that line, but they are super short -
            # maybe those are fights where the logger was dead before they started?
            if 'Engage!' in line:
                in_fight = True
                start = extract_time(line)

            # yields the same (incomplete data) as parsing NetworkDeaths
            # if in_fight and line.startswith('00|') and 'defeated' in line:
            #     print(line)

            if in_fight and str(constants.ACTOR_CONTROL_LINES_WIPE) in line:
                in_fight = False
                fight_duration = extract_time(line) - start
                encounters.append(Encounter(start, fight_duration, progress='wipe'))

                # if fight_duration < datetime.timedelta(seconds=510):
                #     encounters.append(Encounter(start, fight_duration, progress='wipe'))
                # else:
                #     encounters.append(Encounter(start, datetime.timedelta(seconds=510), progress='clear'))
            elif str(constants.ACTOR_CONTROL_LINES_WIPE) in line:
                start = extract_time(line)

                in_fight = False


            elif in_fight and "40000003" in line:
                in_fight = False
                fight_duration = extract_time(line) - start
                encounters.append(Encounter(start, fight_duration, progress='clear'))

                print(line)

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
    g = sns.scatterplot(y='duration', x=data.index, hue='progress', data=data)
    g.set(xlabel='pull number', ylabel='duration (in seconds)')
    plt.show()

if __name__ == '__main__':

    all_fights = []
    for log_path in glob('e12s logs/Network_20707_20210119.log'):
    # for log_path in glob('e12s logs/*.log'):

        with open(log_path, encoding='utf-8') as fo:
            lines = [l.strip() for l in fo.readlines()]

            p = 0
            a = True
            for i in range(490167, 674713):
                l = lines[i]
                if 'Oracle' in l and a:

                        p = 100
                if p > 0:
                    print(p, l)
                    p -= 1

    print(find_slices(lines))
    all_fights += extract_fights(lines, find_slices(lines)['p1'])

    print(visualize(all_fights))


