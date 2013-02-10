__author__ = 'nnyegaard'

import flickrapi
import json

api_key = "43f96ceebd1427512a63ae71266e54ca"

flickr = flickrapi.FlickrAPI(api_key, cache=True)


photos = flickr.photos_search(tags=["Denmark"], format='json', bbox=[8, 13, 55, 58], page=2)
jdata = json.loads(photos[14:-1])

print json.dumps(jdata, separators = (',' , ':'), indent = 4)