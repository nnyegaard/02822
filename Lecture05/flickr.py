import json
import flickrapi
import treepredict

api_key = "43f96ceebd1427512a63ae71266e54ca"
flickr = flickrapi.FlickrAPI(api_key, cache=True)


def get_photo_data():
    jdata_indland = []

    print "Downloading inland photos"
    #bbox gives 250 per page
    photos_inland = flickr.photos_search(tags=['forest', 'nature', 'grass', 'graes', 'skov'], format='json',
                                         bbox=[8, 55, 13, 58], extras='geo')
    jdata_indland += (json.loads(photos_inland[14:-1])["photos"]["photo"])

    print jdata_indland[0]
    print "Saved our inland photo json data with pprint."

    try:
        with open("photos.txt", "w") as f:
            f.write(json.dumps(jdata_indland, separators=(',', ':'), indent=4))
    except IOError as e:
        print e


def load_data_from_file(): # Return a str with the data
    try:
        with open("photos.txt", "r") as file:
            photo_data = file.read()
            return photo_data
    except IOError as e:
        print e


my_photo_data = load_data_from_file()


def print_my_data():
    print "My data:"
    print my_photo_data


for dic in json.loads(my_photo_data):
    print  dic
print
print "One"
print json.loads(my_photo_data)[0]
if __name__ == "__main__":
    print
    get_photo_data()
    #print photo_data
    #print
    #flickrtree = treepredict.buildtree(photo_data, scoref=treepredict.variance)
    #treepredict.drawtree(flickrtree, "flickr.jpg")