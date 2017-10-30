import json
import csv
import cPickle as pickle
import os
import requests
import psycopg2

def fars_files():
    PATH = 'FARS'
    for filename in os.listdir(PATH):
        file_path = PATH + '/' + filename
        file = open(file_path, 'r')
        reader = csv.reader(file)
        yield reader

def crash_vins():
    vins_in_crash = [] # leaving this a list because the same truck could be a crash over multiple years
    for reader in fars_files():
        used_vins = set() # were seeing dupes
        for row in reader:
            vin = row[12]
            if vin not in used_vins:
                used_vins.add(vin)
                vins_in_crash.append(vin)
    return vins_in_crash
                    
def get_vin_info():
    vins = crash_vins()
    crashes = {}
    vins_s = ";".join(vins)
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/'
    post_fields = {'format': 'json', 'data':vins_s}
    r = requests.post(url, data=post_fields)
    r = r.json()
    results = r['Results']
    for result in results:
        if result['Make'] != '' and result['Model'] != '':
            if result['Series'] != '' or result['GVWR'] != '':
                model_info = (result['Make'], result['Model'], result['Series'], result['GVWR'])
                if model_info in crashes:
                    crashes[model_info] += 1
                else:
                    crashes[model_info] = 1

    crash_file = open('crashprevalence.txt', 'wb')
    pickle.dump(crashes, crash_file)
    crash_file.close()

def crashes_per_model():
    prevalence_file = open('prevalence2.txt', 'rb')
    prevalence = pickle.load(prevalence_file)
    prevalence_file.close()

    crash_file = open('crashprevalence.txt', 'rb')
    crash_prevalence = pickle.load(crash_file)
    crash_file.close

    crash_stats = {}

    for truck, num_trucks in prevalence.iteritems():
        if truck in crash_prevalence:
            crashes = crash_prevalence[truck]
            c_per_m = crashes/float(num_trucks) * 100
            # print "vehicle:", vehicle, "crashes:", crashes, "num_trucks:", num_trucks, 'c per m:', c_per_m
            crash_stats[truck] = (crashes, num_trucks, c_per_m)
        else:
            crash_stats[truck] = (0, num_trucks, 0)

    return crash_stats


def crash_per_class(crash_stats):
    classes = {}
    for truck, v in crash_stats.iteritems():
        t_class = truck[3]
        model_prev = v[1]
        crash_prev = v[0]
        if t_class in classes:
            m, c = classes[t_class]
            m += model_prev
            c += crash_prev
            classes[t_class] = (m, c)
        else:
            classes[t_class] = (model_prev, crash_prev)


    for c, v in classes.iteritems():
        if len(c) < 60 and c[:7] != "Class 2":
            print c, float(v[1])/v[0]*100, v[1], v[0]


crash_stats = crashes_per_model()
# print len(crash_stats)
# print crash_stats

try:
    con = psycopg2.connect(DATABASE_URI)

    table_name = "Trucks"
except:
    print "I am unable to connect to the database"
# # print crash_stats
# crash_per_class(crash_stats)


