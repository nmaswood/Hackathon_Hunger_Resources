import os, json, csv

chi_geojsonFileName = 'comm-areas.geojson'
cook_geojsonFileName = 'ca-cook-county.geojson'

foodFileName = 'final-input.csv'

with open(chi_geojsonFileName) as f:
    chi_geodata = json.load(f)
with open(cook_geojsonFileName) as f1:
    cook_geodata = json.load(f1)

ca2data={}
with open(foodFileName) as f2:
    foodreader = csv.DictReader(f2)
    for row in foodreader:
        k = row['Community Area']
        v = {
            'Number': row['Number'],
            'Rate': row['Rate'],
            'Students Eligible': row['Students Eligible']
        }
        ca2data[k]=v

for feature in chi_geodata['features']:
    caname = feature['properties']['community'].title()

    if caname in ca2data:
        temp = ca2data[caname]['Number'].replace(',','')
        if 'na' in temp:
            temp = 0
        number = int(temp)
        if 'na' in ca2data[caname]['Rate']:
            rate = 0
        else:
            rate = float(ca2data[caname]['Rate'][:-1])/100

        if 'na' in ca2data[caname]['Students Eligible'] or ca2data[caname]['Students Eligible']=='0':
            students = 0
        else:
            students = float(ca2data[caname]['Students Eligible'][:-1])/100
    else:
        number = 0
        rate = 0
        students = 0

    feature['properties']['rate']=rate
    feature['properties']['number']=number
    feature['properties']['students']=students

for feature in cook_geodata['features']:
    caname = feature['properties']['city'].title()
    if caname in ca2data:
        print ca2data[caname]
        temp = ca2data[caname]['Number'].replace(',','')
        if 'na' in temp:
            temp = 0
        number = int(temp)
        if 'na' in ca2data[caname]['Rate']:
            rate = 0
        else:
            rate = float(ca2data[caname]['Rate'][:-1])/100

        if 'na' in ca2data[caname]['Students Eligible'] or ca2data[caname]['Students Eligible']=='0':
            students = 0
        else:
            students = float(ca2data[caname]['Students Eligible'][:-1])/100

    else:
        number = 0
        rate = 0
        students = 0

    feature['properties']['rate']=rate
    feature['properties']['number']=number
    feature['properties']['students']=students

    chi_geodata['features'].append(feature)


finalOutput = chi_geodata
with open('clean-output.geojson', 'w') as outfile:
    json.dump(finalOutput, outfile)
