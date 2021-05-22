import constants
from logparser_uwu import uwu_progress
import logfinder

import pymongo

# plotting
import pandas
import seaborn as sns
import matplotlib.pyplot as plt


def visualize(data: pandas.DataFrame):
    sns.set_theme()
    sns.set_style('ticks')
    if 'progress' in data:
        g = sns.scatterplot(y='duration', x=data.index, data=data, hue='progress')
    else:
        g = sns.scatterplot(y='duration', x=data.index, data=data)

    g.set(xlabel='pull number', ylabel='duration (in seconds)')
    plt.show()


if __name__ == '__main__':
    logfinder.update_db()

    client = pymongo.MongoClient()
    col = client['logs']['encounters']

    encounters = col.find({'location': constants.Locations.UWU})
    durations, progress = [], []
    for encounter in encounters:
        durations.append((encounter['end'] - encounter['start']).seconds)
        progress.append(uwu_progress(encounter['combatants']))

    data = pandas.DataFrame(data={'duration': durations, 'progress': progress})
    visualize(data)
