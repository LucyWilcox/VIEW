import json
import csv
import cPickle as pickle
import os

'''

'''

FREIGHTLINER_WMI = set({'FU', 'FV', 'AK', 'AL'})
NAVISTAR_WMI = set({'HT', 'HS', 'HV', 'HP', 'HC', 'KA', 'B4', 'T4', 'WE'})
HINO_WMI = set({'JHA', 'JHB', '5PV', '2AY'})
MACK_WMI = set({'1M1', '1M2', '1M3', '1M4'})

def get_models():
    fl_file = open('flmodels.txt', 'rb')
    models = pickle.load(fl_file)
    fl_file.close()
    ns_file = open('nsmodels.txt', 'rb')
    models.update(pickle.load(ns_file))
    ns_file.close()
    hino_file = open('hinomodels.txt', 'rb')
    models.update(pickle.load(hino_file))
    hino_file.close()

    return models

def get_model_prevelance(models):
    model_prevalence = {}
    with open('out_all.txt', 'r') as infile:
        trucks = json.load(infile) # all trucks registered in NYS
        for truck in trucks:
            vin =  truck['vin']
            manufacture_2 = vin[1:3]
            manufacture_3 = vin[:3]
            model_5 = vin[:5]
            model_6 = vin[:6]
            model_info = None

            if model_6 in models:
                model_info = models[model_6]
            elif model_5 in models:
                model_info = models[model_5]

            if model_info:
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
        
def fars_reader(models):
    crashes = {}
    for reader in fars_files():
        used_vins = set() # were seeing dupes
        for row in reader:
            vin = row[12]
            if vin not in used_vins:
                used_vins.add(vin)
                manufacture_2 = vin[1:3]
                manufacture_3 = vin[:3]
                model_5 = vin[:5]
                model_6 = vin[:6]
                model_info = None

                if model_6 in models:
                    model_info = models[model_6]
                elif model_5 in models:
                    model_info = models[model_5]
                    
                if model_info:
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

    return crash_stats


models = get_models()
crashes = fars_reader(models)
model_prevalence  = get_model_prevelance(models)
crashes_per_model(crashes, model_prevalence)