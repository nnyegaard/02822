__author__ = 'nnyegaard'

import flickrapi
import json

api_key = "43f96ceebd1427512a63ae71266e54ca"

flickr = flickrapi.FlickrAPI(api_key, cache=True)

photos = flickr.photos_search(tags=["Denmark"], format='json', bbox=[8, 13, 55, 58], page=2)
jdata = json.loads(photos[14:-1])

print "Saved our raw json data with pprint."

try:

    with open("rawjsondata.txt", "w") as f:
        f.write(json.dumps(jdata, separators=(',', ':'), indent=4))

except IOError as e:
    print e


print "Saved only the photo list of the json data."

try:

    with open("photolist.txt", "w") as f:
        f.write(json.dumps(jdata["photos"]["photo"], separators=(',', ':'), indent=4))

except IOError as e:
    print e