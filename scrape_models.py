import json
import csv
import cPickle as pickle
from bs4 import BeautifulSoup as bs
import urllib
import time

# Peterbilt vin info: https://vpic.nhtsa.dot.gov/mid/home/displayfile/6211
# Freightliner vin info: https://vpic.nhtsa.dot.gov/mid/home/displayfile/32488, https://vpic.nhtsa.dot.gov/mid/home/displayfile/32228

FREIGHTLINER_WMI = set({'1FU', '1FV', '2FU', '2FV' '3AK', '3AL', '4UZ'})
NAVISTAR_WMI = set({'HT', 'HS', 'HV', 'HP', 'HC', 'KA', 'B4', 'T4', 'WE'})
HINO_WMI = set({'JHA', 'JHB', '5PV', '2AY'})
MACK_WMI = set({'1M1', '1M2', '1M3', '1M4'})
FORD_WMI = set({''})
#Isuzu

def get_models(manufacture_wmi, manufacture):
    vins = set()
    with open('out_all.txt', 'r') as infile:
        trucks = json.load(infile)
        for truck in trucks:
            vin =  truck['vin']
            if manufacture in set({'ns'}):
                manufacture_code = vin[1:3]
            else:
                manufacture_code = vin[:3]
            if manufacture_code in manufacture_wmi:
                vins.add(vin)
    return vins

def make_models(manufacture_wmi, manufacture):
    # run once per manufacture creates pickled object
    url = 'http://www.vin-decoder.org/details?vin='
    models = {}
    vins = list(get_models(manufacture_wmi, manufacture))
    for vin in vins:
        if manufacture is 'fl':
            model_id = vin[:6]
        else:
            model_id = vin[:5]
        if model_id not in models:
            try:
                r = urllib.urlopen(url + vin).read()
                soup = bs(r, 'html.parser')
                title = soup.find_all('div', class_='title')
                title = str(title[1].find('h2').contents[0])
                title = title.split('-')[0] #strip vin
                title = title[5:] #strip year
                weights = {"class 3": soup.find('td', string='10,001 - 14,000 Pounds'), 
                        'class 4': soup.find('td', string='14,001 - 16,000 Pounds'), 
                        'class 5': soup.find('td', string='16,001 - 19,500 Pounds'),
                        'class 6': soup.find('td', string='19,501 - 26,000 Pounds'),
                        'class 7': soup.find('td', string='26,001 - 33,000 Pounds'),
                        'class 8': soup.find('td', string='33,000+ Pounds')}
                weight = [k for k, v in weights.iteritems() if v is not None]
                if len(weight) is 0:
                    models[model_id] = False # adding so we don't hit the site for these
                else:
                    weight = weight[0]
                    models[model_id] = (manufacture, title, weight)
            except:
                pass
            time.sleep(3) #careful now

    models = { k:v for k, v in models.items() if v} 
    file_name = manufacture + 'models.txt'
    output = open(file_name, 'wb')
    pickle.dump(models, output)
    output.close()

# make_models(HINO_WMI, 'hino')
# make_models(NAVISTAR_WMI, 'ns')
# make_models(FREIGHTLINER_WMI, 'fl')
# make_models(MACK_WMI, 'mack')