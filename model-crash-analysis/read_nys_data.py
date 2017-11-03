import json

# with open('out5.txt', 'r') as infile:
# 	item_dict = json.load(infile)

# print len(item_dict)

with open('out_all.txt', 'w') as outfile:
	in1 = open('out.txt', 'r')
	in2 = open('out2.txt', 'r')
	in3 = open('out3.txt', 'r')
	in4 = open('out4.txt', 'r')
	in5 = open('out5.txt', 'r')
	item_dict1 = json.load(in1)
	item_dict2 = json.load(in2)
	item_dict3 = json.load(in3)
	item_dict4 = json.load(in4)
	item_dict5 = json.load(in5)
	item_dict_all = item_dict1 + item_dict2 + item_dict3 + item_dict4 + item_dict5
	json.dump(item_dict_all, outfile)
	print len(item_dict_all)


	#json.dump(output, outfile)