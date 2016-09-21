import json
import utm
import math
import urllib2

class node():
	def __init__(self, lat, lng, theta = 0):
		self.lat = float(lat)
		self.lng = float(lng)
		self.theta = float(theta)

# opening the required url, and printing corresponding metadata
def execute_url(url):
	url = url.replace(' ', '%20')

	print '=== generate_standing_point ==='
	print url
	
	# Send the GET request to the Place details service (using url from above)
	response = urllib2.urlopen(url)

	# Get the response and use the JSON library to decode the JSON
	json_raw = response.read()
	json_data = json.loads(json_raw)

	return json_data

# instead of convert it into x-y plane, here we calculate theta in lat-lng directly
def get_theta(origin, destination):
	theta = math.atan2(destination.lat - origin.lat, destination.lng - origin.lng) * 180 / math.pi
	return theta

def calculate_distance_in_degree(origin, destination):
	delta_lat = origin.lat - destination.lat
	delta_lng = origin.lng - destination.lng

	result = math.sqrt(delta_lat * delta_lat + delta_lng * delta_lng)

	return result

# ====== main =====
if __name__ == '__main__':

	query_city = open("./config/query_city.info", "r").readline().rstrip()

	work_dir = "./data/%s/" % query_city

	f_input = open(work_dir + "generate_initial_point_output.txt", "r")
	f_output = open(work_dir + "generate_standing_point_output.txt", "w")

	way_index = 0
	while (f_input.readline()):
		way_id = f_input.readline().rstrip()
		initial_point_num = int(f_input.readline().rstrip())
		initial_point_array = []
		for i in range(initial_point_num):
			tmp = f_input.readline().rstrip().split(",")
			tmp_lat = tmp[0]
			tmp_lng = tmp[1]
			tmp_node = node(tmp_lat, tmp_lng)
			initial_point_array.append(tmp_node)

		node_num = 0
		standing_point_array = []

		# deal with the first initial_point_num - 1 points
		for i in range(initial_point_num - 1):
			#head node
			origin = initial_point_array[i]
			#tail node
			destination = initial_point_array[i + 1]

			theta = get_theta(origin, destination) + 90

			tmp_node = node(origin.lat, origin.lng, theta)
			standing_point_array.append(tmp_node)
			node_num += 1
			# f_output.write("%s,%s\n" % (origin.lat, origin.lng))
			# f_output.write("%s\n" % theta)

			distance_in_degree = calculate_distance_in_degree(origin, destination)
			distance_step = int(distance_in_degree * 10000) + 1 # similar to distance_in_degree % 0.0001

			delta_lat = destination.lat - origin.lat
			delta_lng = destination.lng - origin.lng

			for j in range(1, distance_step):
				tmp_lat = origin.lat + j * delta_lat / distance_step
				tmp_lng = origin.lng + j * delta_lng / distance_step

				tmp_node = node(tmp_lat, tmp_lng, theta)
				standing_point_array.append(tmp_node)
				node_num += 1

		# deal with the last point (the last point has no next point...)
		origin = initial_point_array[initial_point_num - 2]
		destination = initial_point_array[initial_point_num - 1]

		theta = get_theta(origin, destination) + 90

		# tmp_node = node(origin.lat, origin.lng, theta)
		tmp_node = node(destination.lat, destination.lng, theta)
		standing_point_array.append(tmp_node)
		node_num += 1

		# print to f_output
		f_output.write("=== play with the %dth way ===\n" % way_index)
		f_output.write("%s\n" % way_id)
		f_output.write("%d\n" % node_num)

		for i in range(node_num):
			tmp_node = standing_point_array[i]
			f_output.write("%s,%s\n" % (tmp_node.lat, tmp_node.lng))
			f_output.write("%s\n" % tmp_node.theta)



		way_index += 1	

