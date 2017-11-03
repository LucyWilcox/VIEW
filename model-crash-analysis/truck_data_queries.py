import psycopg2
import config as config
import numpy as np

DATABASE_URI = config.DATABASE_URI
TOTAL_MODELS = 339

"""
This is really just to analyize this data... code isn't top notch...
"""

def num_crashes():
    conn = psycopg2.connect(DATABASE_URI)
    curr = conn.cursor()
    curr.execute("SELECT crashes, prev FROM trucks")
    total_crashes = 0
    total_trucks = 0
    for r in curr:
        total_crashes += r[0]
        total_trucks += r[1]
    print total_crashes, total_trucks, float(total_crashes)*100/total_trucks
    curr.close()
    conn.close() 

# num_crashes()

def num_models_ex_gvwc():
    conn = psycopg2.connect(DATABASE_URI)
    curr = conn.cursor()
    curr.execute("SELECT * FROM trucks")
    models_id = dict()
    models_prev = dict()
    models_crashes = dict()
    for r in curr:
        make = r[1]
        model = r[2]
        series = r[3]
        idn = r[0]
        prev = r[5]
        crashes = r[6]
        info = (make, model, series)
        if info in models_id:
            models_id[info].append(idn)
            models_prev[info] += prev
            models_crashes[info] += crashes
        else:
            models_id[info] = [idn]
            models_prev[info] = prev
            models_crashes[info] = crashes

    model_ids = []
    model_crashes = []
    model_prev = []
    model_info = []

    for crashes, prevs, ids in zip(models_crashes.iteritems(), models_prev.iteritems(), models_id.iteritems()):
        idn = ids[1]
        model = crashes[0]
        crash = crashes[1]
        prev = prevs[1]
        model_ids.append(idn)
        model_crashes.append(crash)
        model_prev.append(prev)
        model_info.append(model)
        prec = float(crash)*100/prev
        if prec > 5:
            print model, crash, prev, prec
        if prec == 0:
            print model, crash, prev, prec

    # c_m = zip(models_crashes, model_prev)
    prec = [float(c)*100/p for c,p in zip(model_crashes, model_prev)]
    nprec = np.array([prec])

    print "10", np.percentile(nprec, 10)
    print "20", np.percentile(nprec, 20)
    print "30", np.percentile(nprec, 30)
    print "40", np.percentile(nprec, 40)
    print "50", np.percentile(nprec, 50)
    print "60", np.percentile(nprec, 60)
    print "70", np.percentile(nprec, 70)
    print "80", np.percentile(nprec, 80)
    print "90", np.percentile(nprec, 90)
    print "95", np.percentile(nprec, 95)
    print "100", np.percentile(nprec, 100)


        # crashes.append
    # print models_crashes, models_prev, models_id

    curr.close()
    conn.close() 

num_models_ex_gvwc()