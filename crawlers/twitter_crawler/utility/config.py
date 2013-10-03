import os

instagram_client_id = '4d9231b411eb4ef69435b40eb83999d6'
instagram_client_secret = '204c565fa1244437b9034921e034bdd6'

instagram_API_pause = 0.1

#mongodb_address = 'grande'
mongodb_address = 'grande.rutgers.edu'
mongodb_port = 27017

class BaseConfig(object):
        min_lat = 40.690531
        max_lat = 40.823163
        min_lng = -74.058151
        max_lng = -73.857994
        region_percentage = 0.3
        min_elements = 8
        
        # grand : res ; joust : grad
        @staticmethod
        def getRegionListPath():
                cp = os.getcwd()
                path = '/*/users/kx19/citybeat_online/distributed_gp/utility/region_cache/' 
                if '/res/' in cp:
                        return path.replace('*', 'res')
                if '/grad/' in cp:
                        return path.replace('*', 'grad')
              # in my pc
                return cp + '\\region_cache\\'

class InstagramConfig(BaseConfig):
    photo_db = 'citybeat_production'
    event_db = 'citybeat_production'
    prediction_db = 'citybeat_production'
    #online setting
    photo_collection = 'photos'
    event_collection = 'online_candidate_instagram'
    prediction_collection = 'online_prediction_instagram'
    # in seconds
    merge_time_interval = 1
    zscore = 3
    min_phots = 8
    # bottom left: 40.690531,-74.058151
    # bottom right: 40.823163,-73.857994
    photo_min_lat = 40.690531
    photo_max_lat = 40.823163
    photo_min_lng = -74.058151
    photo_max_lng = -73.857994
    # cut the region into region_N * region_M subregions
    # try 10*10, 15*15, 20*20, 25*25
    #region_N = 25
    #region_M = 25

class TwitterConfig(BaseConfig):
    # we have not yet moved tweets from citybeat to production
    tweet_db = 'citybeat_production'
    event_db = 'citybeat_production'
    prediction_db = 'citybeat_production'
    tweet_collection = 'tweets'
    prediction_collection = 'online_prediction_twitter'
    event_collection = 'online_candidate_twitter'
    # grand : res ; joust : grad
    
if __name__ == '__main__':
    print BaseConfig.getRegionListPath()