import csv

schoolfile  = 'school.csv'
bigfile = 'csa-data.csv'

ca2school={}
ca2data={}

with open(schoolfile) as f2:
    sreader = csv.DictReader(f2)
    for row in sreader:
        k = row['Community Area']
        v = {
            'Students Eligible': row['Students Eligible']
        }
        ca2school[k]=v

with open(bigfile) as f3:
    breader = csv.DictReader(f3)
    for row in breader:
        k = row['Community Area']
        v = {
            'Number': row['Number'],
            'Rate': row['Rate']
        }
        if k in ca2school:
            v['Students Eligible'] = ca2school[k]['Students Eligible']
        else:
            v['Students Eligible'] = 0
        ca2data[k]=v

with open('final-input.csv', 'w') as csvfile:
    fieldnames = ['Community Area','Number','Rate','Students Eligible']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for k,v in ca2data.iteritems():
        writer.writerow({'Community Area': k,'Number': v['Number'] ,'Rate': v['Rate'],'Students Eligible': v['Students Eligible']})
