import pprint
from bs4 import BeautifulSoup
import requests as r
import pickle
import csv
import pandas as pd
import pdb
from time import sleep
from sys import exit
from random import choice
from play import COMMMUNITY_DATA

def make_request(address):

    keys = [
    'AIzaSyDaRKlkAyfN0lm9zvhgbbrm0wAnAFdEtSQ',
    'AIzaSyD50A41PUmax5ZsgwPPFT0sgyCJ9MMTNt8',
    'AIzaSyASOcLWka_FEl1BFENfORYrnQiekGIN3Mo',
    'AIzaSyB3JqzTXYk1DDxumFNZn8sEDBRXqbaYgZc',
    ]

    key = choice(keys)

    url  = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={key}'
    res = r.get(url)
    as_json = res.json()
    if as_json.get("status") in {'UNKNOWN_ERROR', 'ZERO_RESULTS'}:
        print ("FUCK DUDE {} on {}".format(as_json.get("status"), url))
        return []

    if res.status_code != 200 or as_json.get('status') != 'OK':
        print (url)
        print (res.json())
        exit(1)
    sleep(.1)

    return as_json.get('results')


DATA_NAME = 'salil_data_so_far.pkl'

def write_data(data):
    with open (DATA_NAME, 'wb') as outfile:
        pickle.dump (data, outfile)

def read_data():

    with open(DATA_NAME, 'rb') as infile:
        res = pickle.load(infile)
    return res

def main():

    print ("THIS IS FOR SALIL")
    data = read_data()
    for community in COMMMUNITY_DATA:
        address = community + ", Chicago, IL"

        if address in data:
            print ("Address already in data .... {}".format(address))
        else:
            print ("Making request for {}".format(address))
            res = make_request(address)
            data[address] = res
            write_data(data) 
            print ("Now have {} entries".format(len(data)))

#main()
#write_data({})
foo = read_data()