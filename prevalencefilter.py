import cPickle as pickle

"""
Used to filter prevalences such that make and model info in mandatory and that there must be at least 50 of the truck registered in the NYS

Note: with this we have reduced the total number of trucks we are looking at from around 170,000 to 131,253
"""

prevalence_file = open('prevelance.txt', 'rb')
prevalence = pickle.load(prevalence_file)
prevalence_file.close()

filtered_prevalence = {}
for k, v in prevalence.iteritems():
	k = (k[1:])
	# print k[3]
	if k[2] != '' or k[3] != '': # remove trucks without both series or weight class
		if k[0] != '' and k[1] != '': # remove trucks without either make or model
			if k in filtered_prevalence:
				filtered_prevalence[k] += v
			else:
				filtered_prevalence[k] = v


filtered_prevalence = {k:v for k,v in filtered_prevalence.items() if v >= 50} # must have 50 or more truck of this type

prevalence_file2 = open('prevalence2.txt', 'wb')
pickle.dump(filtered_prevalence, prevalence_file2)
prevalence_file2.close()
