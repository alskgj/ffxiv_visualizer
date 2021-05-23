from log_parser import LogParser
file = "C:\\Users\\Dimitri\\AppData\\Roaming\\Advanced Combat Tracker\\FFXIVLogs\\Network_20900_20210522.log"

lp = LogParser(file)
for e in lp.extract_fights():
    print(e)
