"""
    db_filler
    =========

    Goes through all log files and puts them into mongodb

    Creates one database 'logs' with two collections:
    - 'encounters':
        Containing information such as active participants, location and
        start time for each extracted encounter.
    - 'processed':
        Maintains a list of already processed logfiles. This allows for only
        going through new files on a rerun, instead of all logfiles.
"""

import glob
import os

import log_parser
import config

import pymongo
from pymongo import errors


class DBApi:
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.encounters = self.client['logs']['encounters']
        self.processed = self.client['logs']['processed']

        # see https://docs.mongodb.com/manual/indexes/
        # this mainly ensure that there are not duplicate entries
        self.encounters.create_index([('start', pymongo.ASCENDING)], unique=True)
        self.processed.create_index([('document', pymongo.ASCENDING)], unique=True)

    def file_already_processed(self, file) -> bool:
        """
        :return: True if the file was already processed
        """
        file_size = os.stat(file).st_size
        data = self.processed.find_one({'document': file})
        if (
                data and 'size' in data
                and data['size'] == file_size
        ):
            return True
        return False

    def mark_file_processed(self, file):
        """
        Marks file as processed
        """
        file_size = os.stat(file).st_size
        self.processed.update_one(
            filter={'document': file},
            update={"$set": {
                'processed': True,
                'document': file,
                'size': file_size}
            },
            upsert=True)

    def save_encounter(self, encounter: log_parser.Fight, file: str):
        data = {
            'document': file,
            'location': encounter.location,
            'start': encounter.start,
            'end': encounter.end,
            'combatants': sorted(list(encounter.combatants)),
            'status': encounter.status
        }
        try:
            self.encounters.insert_one(data)
        except pymongo.errors.DuplicateKeyError:
            print(f'skipping insertion of [{encounter}]')
            # this should never happen! we tried to insert a fight that
            # was already in, even though we are in an unprocessed logfight.

    def __del__(self):
        self.client.close()
        print('going to sleep now...')


def update_db():
    """
    Goes over all logfiles stored in config.LOG_PATH, extracts all fights found
    and stores them in the db.
    """
    persistence = DBApi()

    for file in glob.glob(config.LOG_PATH+r'\*.log'):
        if persistence.file_already_processed(file):
            continue

        encounters = log_parser.LogParser(file).extract_fights()
        for encounter in encounters:
            persistence.save_encounter(encounter, file)

        persistence.mark_file_processed(file)


if __name__ == '__main__':
    update_db()
