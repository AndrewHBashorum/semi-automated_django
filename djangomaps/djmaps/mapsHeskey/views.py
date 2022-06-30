from django.shortcuts import render
import re
from geopy.geocoders import GoogleV3
from pyproj import Proj, transform
import logging
import json
# Create your views here.
def default_map(request):
    print('IM here okay ')
    mapbox_access_token = 'pk.eyJ1IjoiYW5kcmV3YmFzaCIsImEiOiJjbDRkeWE5ZzAwY3dyM2VtbWVpd3VlM3RmIn0.M52OtwZ6It_mXAR2pBppKg'
    return render(request, 'default2.html',{
        'mapbox_access_token' : mapbox_access_token
    })


def request_page(request):
    if(request.GET.get('mybtn')):
        arr = []
        with open('/Users/andrewbashorm/Dropbox/auto_processing/json_files/67_HA4_9BY.json') as json_file:
            data = json.load(json_file)

        arr2 = single_spatial_to_list(data['main_site']['geom'])
        arr.append(arr2)

        with open('/Users/andrewbashorm/Dropbox/auto_processing/json_files/67_HA4_9BY.json') as json_file:
            data = json.load(json_file)

        arr2 = single_spatial_to_list(data['left_site']['geom'])
        arr.append(arr2)

        with open('/Users/andrewbashorm/Dropbox/auto_processing/json_files/67_HA4_9BY.json') as json_file:
            data = json.load(json_file)

        arr2 = single_spatial_to_list(data['right_site']['geom'])
        arr.append(arr2)

        mapbox_access_token = 'pk.eyJ1IjoiYW5kcmV3YmFzaCIsImEiOiJjbDRkeWE5ZzAwY3dyM2VtbWVpd3VlM3RmIn0.M52OtwZ6It_mXAR2pBppKg'
        house_id, house_number, postcode, xt, yt, long_center, lat_center = geo_locate_houses_alt(str((request.GET.get('mytextbox'))))

        return render(request, 'default.html', {
            'mapbox_access_token': mapbox_access_token,
            'long_center': long_center,
            'lat_center': lat_center,
            'data': arr
        })

def single_spatial_to_list(g):

    """!@brief Converts MULTIPOLYGON string list to clean list with both x,y points

    @return list containing x,y points

    @param geom: MULTIPOLYGON string to clean
    """

    g = g.replace("MULTIPOLYGON", "")
    g = g.replace("(", "")
    g = g.replace(")", "")
    g = g.replace(",", " ")
    g = g.replace('"', " ")
    g = g.replace("'", " ")
    g = g.split()

    arr = []
    for i in range(0,len(g),2):
        arr1 = []
        arr1.append(float(g[i]))
        arr1.append(float(g[i+1]))
        arr.append(arr1)
    return arr

def find_id(address):
    """!@brief Uses Regrex to craft house id from full address

    @return id: House id = house num = _ + postcode
    @return house_number: Number of house in address
    @return postcode: UK postcode
    @author Andrew Bashorum
    @param address: Full house address

    """
    reobj = re.compile(r'(\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b)')  # Regrex for Postcode in UK
    matchobj = reobj.search(address)
    if matchobj:
        postcode = matchobj.group(1)
        postcode = postcode.replace(" ", "_")
        address = address.split(' ')
        house_number = address[0]
        id = address[0] + '_' + postcode
        return id, house_number, postcode
    else:
        return None, None, None




def geo_locate_houses_alt(address):
        GOOGLE_API_KEY = 'AIzaSyAcQIYA9e_qvw7MBLBzqLXMe4m8VIN2agY'
        geolocator = GoogleV3(api_key=GOOGLE_API_KEY)
        location = geolocator.geocode(address)

        # get coord in EPSG:27700
        input = Proj(init='EPSG:4326')
        output = Proj(init='EPSG:4326')
        xd, yd = transform(input, output, location.longitude, location.latitude)

        input = Proj(init='EPSG:4326')
        output = Proj(init='EPSG:27700')
        xt, yt = transform(input, output, location.longitude, location.latitude)

        id_house, house_number, postcode = find_id(address)

        return id_house, house_number, postcode, xt, yt, xd, yd
