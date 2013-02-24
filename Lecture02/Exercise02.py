__author__ = 'nnyegaard'

import flickrapi
import json

api_key = "43f96ceebd1427512a63ae71266e54ca"

flickr = flickrapi.FlickrAPI(api_key, cache=True)


def getPhotoInland():
    jdata_indland = []

    for page in xrange(1, 17):
        print "Downloading page %r of inland photos" % page
        #bbox gives 250 per page, so 4x250 = 1000 or 2x500
        photos_inland = flickr.photos_search(tags=['forest', 'nature', 'grass', 'graes', 'skov'], format='json',
                                             bbox=[8, 55, 13, 58], page=page, extras='geo')
        jdata_indland += (json.loads(photos_inland[14:-1])["photos"]["photo"])

    print "Saved our inland photo json data with pprint."

    try:
        with open("inland_photo_list.txt", "w") as f:
            f.write(json.dumps(jdata_indland, separators=(',', ':'), indent=4))
    except IOError as e:
        print e


def getPhotosSea():
    jdata_sea = []

    for page in xrange(1, 17):
        print "Downloading page %r of sea photos" % page
        #bbox gives 250 per page, so 4x250 = 1000 or 2x500
        photos_sea = flickr.photos_search(tags=['beach', 'sea', 'water', 'vand', 'havet'], format='json',
                                          bbox=[8, 55, 13, 58],
                                          page=page, extras='geo')
        jdata_sea += (json.loads(photos_sea[14:-1])["photos"]["photo"])

    print "Saved our sea photo list json data with pprint."

    try:
        with open("sea_photo_list.txt", "w") as f:
            f.write(json.dumps(jdata_sea, separators=(',', ':'), indent=4))
    except IOError as e:
        print e


if __name__ == '__main__':
    getPhotosSea()
    getPhotoInland()