import operator
import types

from config import InstagramConfig
from photo_interface import PhotoInterface
from mongodb_interface import MongoDBInterface
from tweet_interface import TweetInterface

class Region:
	
	def __init__(self, region):
		# this init method supports three types of input
		if type(region) is types.DictType:
			self._region = region
		else:
			if type(region) is types.ListType:
				self._region = {}
				self._region['min_lat'] = region[0]
				self._region['min_lng'] = region[1]
				self._region['max_lat'] = region[2]
				self._region['max_lng'] = region[3]
			else:
				self._region = region.toDict()
			
	def insideRegion(self, coordinate):
		# coordinates must be formatted as [lat, lng]
		lat = coordinate[0]
		lng = coordinate[1]
		if self._region['min_lat'] > lat or lat > self._region['max_lat']:
			return False
		if self._region['min_lng'] > lng or lng > self._region['max_lng']:
			return False
		return True
	
	def toDict(self):
		return self._region
	
	def toTuple(self):
		return (self._region['min_lat'], self._region['min_lng'], self._region['max_lat'], self._region['max_lng'])
	
	def display(self):
		print self._region
				
	def getMidCoordinates(self):
		return ((self._region['min_lat'] + self._region['max_lat'])/2, (self._region['min_lng'] + self._region['max_lng'])/2)
		
	def divideRegions(self, n, m):
		# this method only works when the "region" is the whole region
		# divde the whole NYC into n*m rectangular regions
		lat_offset = 	(self._region['max_lat'] - self._region['min_lat']) / n
		lng_offset = 	(self._region['max_lng'] - self._region['min_lng']) / m
		region_list = []
		for i in xrange(0, n):
			low_lat = self._region['min_lat'] + i * lat_offset
			high_lat = low_lat + lat_offset
			for j in xrange(0, m):
				low_lng = self._region['min_lng'] + j * lng_offset
				high_lng = low_lng + lng_offset
				coordinates = [low_lat, low_lng, high_lat, high_lng]
				r = Region(coordinates)
				region_list.append(r)
		return region_list
	
	def filterRegions(self, region_list, percentage=InstagramConfig.region_percentage,test=False, n=10, m=10, documentType='photo'):
		assert documentType in ['photo', 'tweet']
		if test:
			#n and m should be set if test is true
			#this is only for test
			new_region_list = []
			#folder = '/res/users/kx19/Citybeat/CityBeat/distributed_gp/utility/region_cache/'
			folder = '/grad/users/kx19/citybeat_online/distributed_gp/utility/region_cache/'
			file_name = str(n)+'_'+str(m)+'.txt'
			fid = open(folder + file_name)
			for line in fid:
				region = line.split()
				for i in xrange(0,4):
					region[i] = float(region[i])
				region = Region(region)
				new_region_list.append(region)
			return new_region_list
			
		# this method should not be a member of this class
		# TODO: change the period to one week
		
		end_time = 1499704845
		begin_time = 1299704845
#		end_time = 1359704845 - 7*3600*24
#		begin_time = end_time - 14*3600*24
		if documentType == 'photo':
			documentInterface = PhotoInterface()
		else:
			documentInterface = TweetInterface()
		document_cur = documentInterface.rangeQuery(period=[str(begin_time), str(end_time)])
		region_number = len(region_list)
		number_document_in_region = [0]*region_number
		bad_documents = 0
		total_documents = 0
		for document in document_cur:
			total_documents += 1
			lat = float(document['location']['latitude'])
			lng = float(document['location']['longitude'])
			flag = 0
			for i in xrange(region_number):
				if region_list[i].insideRegion([lat, lng]):
					number_document_in_region[i] += 1
					flag = 1
					break
			if flag == 0:
				bad_documents += 1
				
		print str(bad_documents) + ' out of ' + str(total_documents) + ' documents are bad(not in NY)'
		
		region_tuples = []
		for i in xrange(0, region_number):
			region_tuples.append((region_list[i], number_document_in_region[i]))
		
		region_tuples.sort(key=operator.itemgetter(1), reverse=True)

		valid_region_number = int(0.5 + 1.0 * region_number * percentage)
		valid_regions = []
		
#		print region_tuples[valid_region_number-1][1]

		for i in xrange(0, valid_region_number):
			region = region_tuples[i][0]
			lat = (self._region['min_lat'] + self._region['max_lat'])/2
			lng = (self._region['min_lng'] + self._region['max_lng'])/2
			cnt = region_tuples[i][1]
		
		for i in xrange(0, valid_region_number):
			valid_regions.append(region_tuples[i][0])
		
		return valid_regions

if __name__=="__main__":
	coordinates = [InstagramConfig.photo_min_lat, InstagramConfig.photo_min_lng,
	               InstagramConfig.photo_max_lat, InstagramConfig.photo_max_lng]
	nyc = Region(coordinates)
	region_list = nyc.divideRegions(25, 25)
	region_list = nyc.filterRegions(region_list, test=False, n=25, m=25, documentType='tweet')
	for region in region_list:
		region = region.toDict()
		#print region['min_lat'], region['min_lng'], region['max_lat'], region['max_lng']
