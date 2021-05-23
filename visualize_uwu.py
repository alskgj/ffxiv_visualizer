import constants
from modules.uwu import uwu_progress
import db_filler

import pymongo

# plotting
import pandas
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.dpi'] = 300


def visualize(data: pandas.DataFrame):
    plt.figure()
    sns.set_theme()
    sns.set_style('ticks')
    if 'progress' in data:
        g = sns.scatterplot(y='duration', x=data.index, data=data, hue='progress')
    else:
        g = sns.scatterplot(y='duration', x=data.index, data=data)

    g.set(xlabel='pull number', ylabel='duration (in seconds)')

    # plt.savefig('result.png', dpi=300)
    plt.show()


if __name__ == '__main__':
    db_filler.update_db()

    client = pymongo.MongoClient()
    col = client['logs']['encounters']

    encounters = col.find({'location': constants.Locations.UWU})
    durations, progress = [], []
    for encounter in encounters:
        durations.append((encounter['end'] - encounter['start']).seconds)
        progress.append(uwu_progress(encounter['combatants']))

    data = pandas.DataFrame(data={'duration': durations, 'progress': progress})
    visualize(data)
