from sodapy import Socrata
import json

endpoint = 'https://data.ny.gov/resource/qegy-i7es.json'
path = "data.ny.gov"
# client = Socrata("sandbox.demo.socrata.com", None)
client = Socrata(path, None)
# print client.get("nimj-3ivp", where="depth > 300", order="magnitude DESC", exclude_system_fields=False)

output = client.get('qegy-i7es', where="maximum_gross_weight > 14000", limit=50000, offset=190000)

with open('out6.txt', 'w') as outfile:
	json.dump(output, outfile)

client.close()