"""

    logfinder
    =========

    finds all log-files matching certain criteria such as "contains encounters
    in uwu, with player 'Luthercreed Kero'".

"""

import glob
import log_parser

import pymongo
from pymongo import errors

def update_db():
    client = pymongo.MongoClient()
    db = client['logs']
    collection = db['encounters']

    LOG_PATH = r'C:\Users\Dimitri\AppData\Roaming\Advanced Combat Tracker\FFXIVLogs'
    # storage key uniquely identifying filter params

    # see https://docs.mongodb.com/manual/indexes/
    collection.create_index([('start', pymongo.ASCENDING)], unique=True)
    db['processed'].create_index([('document', pymongo.ASCENDING)], unique=True)

    processed = db['processed'].find({'processed': True})
    processed = [file['document'] for file in processed]

    for file in glob.glob(LOG_PATH+r'\*.log'):
        if file in processed:
            continue

        db['processed'].update_one(
            filter={'document': file},
            update={"$set": {'processed': False, 'document': file}},
            upsert=True
        )

        encounters = log_parser.LogParser(file).extract_fights()

        for encounter in encounters:
            data = {
                'document': file,
                'location': encounter.location,
                'start': encounter.start,
                'end': encounter.end,
                'combatants': sorted(list(encounter.combatants)),
                'status': encounter.status
            }
            try:
                collection.insert_one(data)
            except pymongo.errors.DuplicateKeyError:
                print(f'skipping insertion of [{encounter}]')
                # this should never happen! we tried to insert a fight that
                # was already in, even though we are in an unprocessed logfight.

        db['processed'].update_one(
            filter={'document': file},
            update={"$set": {'processed': True, 'document': file}},
            upsert=True
        )


    client.close()

if __name__ == '__main__':
    update_db()