import requests
import json
import time
import os


ROOT_PATH = "/Users/elfsong/PycharmProjects/FB"
RESOURCE_PATH = os.path.join(ROOT_PATH, "resource")
twitter_data = os.path.join(RESOURCE_PATH, "twitterdata.json")
opening_data = os.path.join(RESOURCE_PATH, "opening.json")

def get_data(url, type):
    data = requests.get(url)

    nextpage = True
    with open(opening_data, 'a') as outfile:
        while nextpage is True:
            r = json.loads((data.content).decode())
            print(r)
            if 'next_page_token' not in r.keys():
                nextpage = False
            else:
                print(r['next_page_token'])
                time.sleep(3)
                data = requests.get(url + "&pagetoken=" + r['next_page_token'] + "")

            for results in r["results"]:
                print(results)
                output = {}
                output['location'] = (results['geometry']['location']['lat'], results['geometry']['location']['lng'])
                output['type'] = type
                outfile.write(json.dumps(output) + "\n")

            print(nextpage)


def get_police_data():
    get_data("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-37.809469,144.958230&radius=20000&type=police&keyword=police&key=AIzaSyBmcobOSNebi_UTBUoBfkfaDyvr4bXgT7U", "police")

def get_open_shops():
    get_data("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-37.809469,144.958230&radius=20000&keyword=shops&opennow=true&key=AIzaSyBmcobOSNebi_UTBUoBfkfaDyvr4bXgT7U", "openshops")

def get_open_resturants():
    get_data("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-37.809469,144.958230&radius=20000&keyword=resturants&opennow=true&key=AIzaSyBmcobOSNebi_UTBUoBfkfaDyvr4bXgT7U", "openresturants")


def get_open_other():
    get_data("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-37.809469,144.958230&radius=20000&keyword=night&opennow=true&key=AIzaSyBmcobOSNebi_UTBUoBfkfaDyvr4bXgT7U", "openother")
    get_data("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-37.809469,144.958230&radius=20000&keyword=hotel&opennow=true&key=AIzaSyBmcobOSNebi_UTBUoBfkfaDyvr4bXgT7U", "openother")
    get_data("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-37.809469,144.958230&radius=20000&keyword=bar&opennow=true&key=AIzaSyBmcobOSNebi_UTBUoBfkfaDyvr4bXgT7U", "openother")
    get_data("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-37.809469,144.958230&radius=20000&keyword=club&opennow=true&key=AIzaSyBmcobOSNebi_UTBUoBfkfaDyvr4bXgT7U", "openother")



def get_open_seveneleven():
    get_data("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-37.809469,144.958230&radius=20000&keyword=seveneleven&opennow=true&key=AIzaSyBmcobOSNebi_UTBUoBfkfaDyvr4bXgT7U", "seveneleven")


def get_all_data():
    get_police_data()
    get_open_shops()
    get_open_resturants()
    get_open_other()
    get_open_seveneleven()


get_all_data()
