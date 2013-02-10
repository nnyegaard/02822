__author__ = 'nnyegaard'

import flickrapi

api_key = "43f96ceebd1427512a63ae71266e54ca"


flickr = flickrapi.FlickrAPI(api_key)

photos = flickr.photos_search(tags=['Monty', 'Python'], format='json')


print photos