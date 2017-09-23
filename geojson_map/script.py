import os, json, csv

gjfname = 'comm-areas.geojson'
fooddata = 'Food-Insecurity-Rates.csv'
with open(gjfname) as f:
    geodata = json.load(f)

ca2data={}
with open(fooddata) as f2:
    foodreader = csv.DictReader(f2)
    for row in foodreader:
        k = row['CA']
        v = (row['A'], row['P'])
        ca2data[k]=v

for feature in geodata['features']:
    caname = feature['properties']['community'].title()
    if caname in ca2data:
        a = ca2data[caname][0]
        p = ca2data[caname][1]
    else:
        a = 0
        p = 0

    feature['properties']['p']=p
    feature['properties']['a']=a
    print feature['properties']

op = geodata
with open('output.geojson', 'w') as outfile:
    json.dump(op, outfile)
