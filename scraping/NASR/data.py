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

    if res.status_code != 200 or as_json['status'] != 'OK' or as_json.get('status') == 'REQUEST_DENIED':
        print (url)
        print (res.json())
        exit(1)
    sleep(.1)

    return as_json.get('results')


DATA_NAME = 'data_so_far.pkl'

def write_data(data):
    with open (DATA_NAME, 'wb') as outfile:
        pickle.dump (data, outfile)

def read_data():

    with open(DATA_NAME, 'rb') as infile:
        res = pickle.load(infile)
    return res

DATA_CSV_NAME = 'program_data.csv'
df = pd.read_csv(DATA_CSV_NAME, encoding = "ISO-8859-1")


class G():
    program_name = 5
    community_area_index = 3
    shipping_address = 9
    city =  "Chicago"
    shipping_zip = 11

def get_address(line):

    community_area_index = line[G.community_area_index]
    shipping_address = line[G.shipping_address]
    city =  "Chicago"
    shipping_zip = line[G.shipping_zip]
    program_name = line[G.program_name]

    res =  shipping_address if shipping_address else program_name

    add = [res, "Chicago", "IL", shipping_zip]
    add = [x for x in add if x]
    return ','.join(add)

#write_data({})
def main():

    data = read_data()
    with open(DATA_CSV_NAME,encoding='utf-8') as infile:
        


        for line in reader:
            continue
            address = get_address(line)
            if address in data:
                print ("Address already in data .... {}".format(address))
            else:
                print ("Making request for {}".format(address))
                res = make_request(address)
                data[address] = res
                write_data(data) 
                print ("Now have {} entries".format(len(data)))

main()
#foo = read_data()
#print (len(foo))