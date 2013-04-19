from MongoDB import MongoDBInterface
from AlarmInterface import AlarmDataInterface


def QueryFromDB():
    mdbi = MongoDBInterface('grande', 27017)
    mdbi.SetDB('historic_alarm')
    mdbi.SetCollection('raw_event')
    
    lat = '40.750542'
    lng = '-73.9931535'
    conditions = {'lat':lat, 'lng':lng}
    events = mdbi.GetAllItems(conditions)
    i = 0
    numberOfPhotos = []
    for event in events:
        i = i + 1
        numberOfPhotos.append(len(event['photos']))
        print len(event['photos'])
        print event['created_time']


def main():
    QueryFromDB()

if __name__ == '__main__':
    main()
    
    
    
# http://www.nba.com/games/20130107/BOSNYK/gameinfo.html   basketball event
# even we can know when start
# 2013-01-07 19:31:33.087495
# 40.750542 , -73.9931535

# the basketball on Jan 10th was not detected

# the basketball on Jan 11th was detected but with wrong date