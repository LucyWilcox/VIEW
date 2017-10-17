import json
import csv
import cPickle as pickle

'''
WMI and Model from: https://vpic.nhtsa.dot.gov/mid/home/displayfile/32488
'''

def get_model_class(rest):
    model_class = 'Glider' # looks like basically everything that doesn't have a class number is 'glider'
    model_info = rest.split('Class')
    if len(model_info) > 1:
        model_class = model_info[1].strip(' ')
    return model_class

def access_models():
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


def get_models():
    FREIGHTLINER_WMI = set({'1FU', '1FV', '3AK', '3AL'})
    output = open('flmodels.txt', 'rb')
    models = pickle.load(output)
    output.close()
    total_trucks = 0
    model_prevalence = {}
    with open('out_all.txt', 'r') as infile:
        trucks = json.load(infile)
        for truck in trucks:
            vin =  truck['vin']
            manufacture = vin[:3]
            total_trucks += 1
            if manufacture in FREIGHTLINER_WMI:
                model = vin[4:6]
                if model in models:
                    model_info = models[model]
                    if model_info in model_prevalence:
                        model_prevalence[model_info] += 1 #maybe should do this by model code?
                    else:
                        model_prevalence[model_info] = 1
    # print model_prevalence
    # print total_trucks
    return model_prevalence

def fars2009():
    FREIGHTLINER_WMI = set({'1FU', '1FV', '3AK', '3AL'})
    output = open('flmodels.txt', 'rb')
    models = pickle.load(output)
    output.close()
    crashes = {}
    with open('FARS2009_dataset.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            vin = row[3]
            manufacture = vin[:3]
            if manufacture in FREIGHTLINER_WMI:
                model = vin[4:6]
                if model in models:
                    model_info = models[model]
                    if model_info in crashes:
                        crashes[model_info] += 1
                    else:
                        crashes[model_info] = 1
    return crashes


def crashes_per_model(crashes, model_prevalence):
    for truck in crashes:
        if truck in model_prevalence:
            prevalance = model_prevalence[truck]
            c_per_m = crashes[truck]/float(prevalance)
            print truck, c_per_m

                    
crashes = fars2009()
model_prevalence  = get_models()
crashes_per_model(crashes, model_prevalence)
# access_models()