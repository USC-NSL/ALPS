import urllib2
import json
import os



# opening the required url, and printing corresponding metadata
def execute_url(url):
	url = url.replace(' ', '%20')

	print '=== generate_initial_point ==='
	print url
	
	# Send the GET request to the Place details service (using url from above)
	response = urllib2.urlopen(url)

	# Get the response and use the JSON library to decode the JSON
	json_raw = response.read()
	json_data = json.loads(json_raw)

	return json_data


# ====== main =====
if __name__ == '__main__':

	f_query_city = open("./config/query_city.info", "r")
	query_city = f_query_city.readline().rstrip()
	# query_state = f_query_city.readline().rstrip()

	work_dir = "./data/%s/" % query_city
	if not os.path.exists(work_dir):
		os.makedirs(work_dir)

	f_output = open(work_dir + "generate_initial_point_output.txt", "w")

	query_area = "34.061133, -118.314394, 34.076633, -118.290147"

	query = "[out:json];way[\"highway\"~\"primary|secondary|tertiary|residential\"](%s);out geom;" % query_area
	url = "http://overpass-api.de/api/interpreter?data=%s" % query

	json_data = execute_url(url)

	if (json_data is None):
		print "Error!"
	else:
		way_index = 0
		for element in json_data["elements"]:
			if (element["type"] == "way"):
				f_output.write("=== play with the %dth way ===\n" % way_index)
				f_output.write("%s\n" % element["id"])
				f_output.write("%d\n" % len(element["geometry"]))
				for node in element["geometry"]:
					lat = str(node["lat"])
					lng = str(node["lon"])
					f_output.write("%s,%s\n" % (lat, lng))

				way_index += 1

