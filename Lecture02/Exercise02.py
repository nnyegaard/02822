__author__ = 'nnyegaard'

import flickrapi
import json

api_key = "43f96ceebd1427512a63ae71266e54ca"

flickr = flickrapi.FlickrAPI(api_key, cache=True)


def getPhotos():
    #bbox gives 250 per page, so 4x250 = 1000 or 2x500
    photos_sea = flickr.photos_search(tags=['beach', 'sea', 'water', 'vand', 'havet'], format='json',
                                      bbox=[8, 55, 13, 58],
                                      page=4)
    jdata_sea = json.loads(photos_sea[14:-1])

    photos_inland = flickr.photos_search(tags=['forest', 'nature', 'grass', 'graes', 'skov'], format='json',
                                         bbox=[8, 55, 13, 58], page=4)
    jdata_inland = json.loads(photos_inland[14:-1])

    print "Saved our raw json data with pprint."

    try:
        with open("rawjsondata_sea.txt", "w") as f:
            f.write(json.dumps(jdata_sea, separators=(',', ':'), indent=4))

        with open("rawjsondata_inland.txt", "w") as f:
            f.write(json.dumps(jdata_inland, separators=(',', ':'), indent=4))

    except IOError as e:
        print e

    print "Saved only the photo list of the json data."

    try:
        with open("photolist_sea.txt", "w") as f:
            f.write(json.dumps(jdata_sea["photos"]["photo"], separators=(',', ':'), indent=4))

        with open("photolist_inland.txt", "w") as f:
            f.write(json.dumps(jdata_inland["photos"]["photo"], separators=(',', ':'), indent=4))

    except IOError as e:
        print

        #print len(jdata_sea["photos"]["photo"])


try:
    with open("photolist_sea.txt", "r") as f:
        seaPhotos = f.read()

except IOError as e:
    print e

for x in json.loads(seaPhotos):
    print flickr.photos_geo_getLocation(photo_id=x["id"], format='json')[14:-1]

#print flickr.photos_geo_getLocation(photo_id=8143819572, format='json')