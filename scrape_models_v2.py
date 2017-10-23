import requests
import cPickle as pickle
import json

def load_trucks():
    with open('out_all.txt', 'r') as infile:
        trucks = json.load(infile)
    return trucks

def clear_files():
    prevelance = {}
    file_name = 'prevelance.txt'
    output = open(file_name, 'wb')
    pickle.dump(prevelance, output)
    output.close()

def get_models(start, end, prevelance, trucks):
    vins = []
    for truck in trucks[start: end]:
        vin =  truck['vin']
        vins.append(vin)

    vins_s = ";".join(vins)

    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/'# + vins_s + '?format=json'
    post_fields = {'format': 'json', 'data':vins_s};
    r = requests.post(url, data=post_fields)
    r = r.json()
    results = r['Results']
    for result in results:
        model_info = (result['Manufacturer'], result['Make'], result['Model'], result['Series'], result['GVWR'])
        if model_info in prevelance:
            prevelance[model_info] += 1
        else:
            prevelance[model_info] = 1

    file_name = 'prevelance.txt'
    output = open(file_name, 'wb')
    pickle.dump(prevelance, output)
    output.close()


def run_all_models():
    # clear_files()
    trucks = load_trucks()
    total_trucks = len(trucks)
    for i in range(5000, total_trucks, 1000):
        prevelance_file = open('prevelance.txt', 'rb')
        prevelance = pickle.load(prevelance_file)
        prevelance_file.close()
        start, end = i, i+1000
        print start, end
        if end < total_trucks:
            get_models(start, end, prevelance, trucks)
        else:
            get_models(start, total_trucks, prevelance, trucks)

# run_all_models()
