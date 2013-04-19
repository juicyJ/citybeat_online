from MongoDB import MongoDBInterface
from AlarmInterface import AlarmDataInterface

class EventQuery(MongoDBInterface):
    
    def __init__(self, address, port):
        super(EventQuery, self).__init__(address, port)
    
    def _CheckPhoto(self, photo, word):
        if word is None:
            return True
        if not photo['caption'] is None:
            text = photo['caption']['text']
            if word in text:
                return True
        return False


    def QueryEventsByKeyword(self, conditions=None, word=None, limit=-1):
        allEvents = self.GetAllItems(conditions)
        validEvents = []
        for event in allEvents:
            if len(validEvents) >= limit and not limit == -1:
                return validEvents
            for photo in event['photos']:
                if self._CheckPhoto(photo, word):
                    validEvents.append(event)
                    break
        return validEvents
        
    def QueryPhotosByKeyword(self, conditions=None, word=None):
        photoURLs = []
        allEvents = self.GetAllItems(conditions)
        for event in allEvents:
            for photo in event['photos']:
                if self._CheckPhoto(photo, word):
                    photoURLs.append(photo['link'])
        return photoURLs            
        

def main():
    eq = EventQuery('grande', 27017)
    eq.SetDB('historic_alarm')
    eq.SetCollection('raw_event')
 

    events = eq.QueryEventsByKeyword()
    for event in events:
#       event['created_time'] = event['discovered_time']
        event['mid_lat'] = event['lat']
        event['mid_lng'] = event['lng']
        event['label'] = 'unlabeled'
        del event['lat']
        del event['lng']
        for photo in event['photos']:
            photo['label'] = 'unlabeled'
        eq.UpdateItem(event)
    
#   i = 0
#   numberOfPhotos = []
#   for event in events:
#       i = i + 1
#       numberOfPhotos.append(len(event['photos']))
#       print len(event['photos'])
#       print event['created_time']



if __name__ == '__main__':
    main()
    
    
    

# http://www.nba.com/games/20130107/BOSNYK/gameinfo.html   basketball event
# even we can know when start
# 2013-01-07 19:31:33.087495
# 40.750542 , -73.9931535

# the basketball on Jan 10th was not detected

# the basketball on Jan 10th was detected but with wrong date