from event_interface import EventInterface
from base_feature import BaseFeature
from photo_interface import PhotoInterface
from photo import Photo
from region import Region
from event import Event
from text_parser import TextParser
from stopwords import Stopwords

import operator
import string
import types
import random
import math

ei = EventInterface()
ei.setDB('AmazonMT')
ei.setCollection('candidate_event_25by25_merged')

events = ei.getAllDocuments()

duplicates = 0
for event in events:
    e = Event(event)
    flag = e.removeDuplicatePhotos()
    if flag > 0:
        print e.getPhotoNumber(), e.getActualValue()
        ei.updateDocument(e)