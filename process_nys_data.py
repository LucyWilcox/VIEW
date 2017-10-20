import json
import csv
import cPickle as pickle
import os
from bs4 import BeautifulSoup as bs
from lxml import html
import requests
import urllib
from html.parser import HTMLParser
import time

'''
WMI and Model from: https://vpic.nhtsa.dot.gov/mid/home/displayfile/32488
'''


FREIGHTLINER_WMI = set({'FU', 'FV', 'AK', 'AL'})
NAVISTAR_WMI = set({'HT', 'HS', 'HV', 'HP', 'HC', 'KA', 'B4', 'T4', 'WE'})

def get_model_class(rest):
    model_class = 'Glider' # looks like basically everything that doesn't have a class number is 'glider'
    model_info = rest.split('Class')
    if len(model_info) > 1:
        model_class = model_info[1].strip(' ')
    return model_class

def make_fl_models():
    # run once creates pickled object
    # for Freightliner trucks only
    models = {}
    with open('freightlinermodels.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            row = row[0]
            code, rest = row[:2], row[2:]
            if 'Conventional' in rest:
                rest = rest.split('Conventional')
                model = rest[0]
                model_class = get_model_class(rest[1])
                models[code] = (model, model_class)
            elif "COE" in rest:
                rest = rest.split('COE')
                model = rest[0]
                model_class = get_model_class(rest[1])
                models[code] = (model, model_class)
            elif "Coe" in rest:
                rest = rest.split('Coe')
                model = rest[0]
                model_class = get_model_class(rest[1])
                models[code] = (model, model_class)
            else:
                print 'error', rest

    output = open('flmodels.txt', 'wb')
    pickle.dump(models, output)
    output.close()

def get_ns_models():
    output = open('flmodels.txt', 'rb')
    models = pickle.load(output)
    output.close()
    navistar_vin = set()
    with open('out_all.txt', 'r') as infile:
        trucks = json.load(infile)
        for truck in trucks:
            vin =  truck['vin']
            manufacture = vin[1:3]
            if manufacture in NAVISTAR_WMI:
                UNDERWEIGHT = set({'A', 'B', 'C', 'D'})
                weight = vin[7]
                if weight not in UNDERWEIGHT and len(vin) is 17:
                    # vin = vin[:-5]
                    # vin = vin + "00000"
                    navistar_vin.add(vin)
    print len(navistar_vin)
    return navistar_vin

def make_ns_models():
    # run once creates pickled object
    # for Navistar trucks only
    url = 'http://www.vin-decoder.org/details?vin='
    models = {}
    navistar_vins = list(get_ns_models())
    for vin in navistar_vins:
        model_id = vin[:5]
        if model_id not in models:
            try:
                r = urllib.urlopen(url + vin).read()
                soup = bs(r, 'html.parser')
                title = soup.find_all('div', class_='title')
                title = str(title[1].find('h2').contents[0])
                title = title.split('-')[0] #strip vin
                title = title[5:] #strip year
                models[model_id] = title
                time.sleep(10) #careful now
            except:
                print "failed", vin
    output = open('nsmodels.txt', 'wb')
    pickle.dump(models, output)
    output.close()


def get_models():
    fl_file = open('flmodels.txt', 'rb')
    fl_models = pickle.load(fl_file)
    fl_file.close()
    ns_file = open('nsmodels.txt', 'rb')
    ns_models = pickle.load(ns_file)
    ns_file.close()
    model_prevalence = {}
    with open('out_all.txt', 'r') as infile:
        trucks = json.load(infile)
        for truck in trucks:
            vin =  truck['vin']
            manufacture = vin[1:3]
            if manufacture in FREIGHTLINER_WMI:
                model = vin[4:6]
                if model in fl_models:
                    model_info = fl_models[model]
                    if model_info in model_prevalence:
                        model_prevalence[model_info] += 1
                    else:
                        model_prevalence[model_info] = 1
            elif manufacture in NAVISTAR_WMI:
                model = vin[:5]
                if model in ns_models:
                    model_info = ns_models[model]
                    if model_info in model_prevalence:
                        model_prevalence[model_info] += 1
                    else:
                        model_prevalence[model_info] = 1
    return model_prevalence

def fars_files():
    PATH = 'FARS'
    for filename in os.listdir(PATH):
        file_path = PATH + '/' + filename
        file = open(file_path, 'r')
        reader = csv.reader(file)
        yield reader
    # file.close() # here??

def fars_reader():
    fl_file = open('flmodels.txt', 'rb')
    fl_models = pickle.load(fl_file)
    fl_file.close()
    ns_file = open('nsmodels.txt', 'rb')
    ns_models = pickle.load(ns_file)
    ns_file.close()
    crashes = {}
    navistar_vin = set()
    for reader in fars_files():
        used_vins = set() # were seeing dupes
        for row in reader:
            vin = row[12]
            if vin not in used_vins:
                used_vins.add(vin)
                manufacture = vin[1:3]
                if manufacture in FREIGHTLINER_WMI:
                    model = vin[4:6]
                    if model in fl_models:
                        model_info = fl_models[model]
                        if model_info in crashes:
                            crashes[model_info] += 1
                        else:
                            crashes[model_info] = 1
                elif manufacture in NAVISTAR_WMI:
                    model = vin[:5]
                    if model in ns_models:
                        model_info = ns_models[model]
                        if model_info in crashes:
                            crashes[model_info] += 1
                        else:
                            crashes[model_info] = 1
    return crashes

def crashes_per_model(crashes, model_prevalence):
    crash_stats = {}
    for truck in crashes:
        if truck in model_prevalence:
            prevalance = model_prevalence[truck]
            c_per_m = crashes[truck]/float(prevalance)
            print "model:", truck, "  crashes:", crashes[truck], "  prevalance:", prevalance, "  per crash:", c_per_m*100
            crash_stats[truck] = (crashes, prevalance, c_per_m*100)
        else:
            print "model:", truck, "prevalance:", prevalance, "no crashes"
            crash_stats[truck] = (0, prevalance, 0)
    return crash_stats



# make_ns_models()                  
crashes = fars_reader()
model_prevalence  = get_models()
crashes_per_model(crashes, model_prevalence)