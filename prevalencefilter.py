prevelance_file = open('prevelance.txt', 'rb')
prevelance = pickle.load(prevelance_file)
prevelance_file.close()
p_v = prevelance.values()
sum_v = 0
for p in p_v:
    sum_v += p
