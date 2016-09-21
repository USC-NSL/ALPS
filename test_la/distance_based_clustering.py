import math



query_city = open("./config/query_city.info", "r").readline().rstrip()
query_landmark = open("./config/query_landmark.info", "r").readline().rstrip()
work_dir = "./data/%s/%s/" % (query_city, query_landmark)

f_input = open(work_dir + "fov_analysis_output_formal.txt", "r").readlines()
f_output = open(work_dir + "distance_based_clustering_output.txt", "w")


class node():
	def __init__(self, lat, lng, meta = ""):
		self.lat = float(lat)
		self.lng = float(lng)
		# self.theta = float(theta)
		self.meta = str(meta)

def calculate_distance_in_degree(origin, destination):
	delta_lat = origin.lat - destination.lat
	delta_lng = origin.lng - destination.lng

	result = math.sqrt(delta_lat * delta_lat + delta_lng * delta_lng)

	return result

# ====== main =====
if __name__ == '__main__':

	# image_number = 48
	min_radius = 0.0005

	basic_db_map = dict()
	tmp = open(work_dir + "basic_image_database_yolo_result.txt", "r").readlines()
	for i in range(len(tmp) / 2):
		basic_db_map[tmp[i * 2].rstrip()[:-4]] = tmp[i * 2 + 1].rstrip()

	node_dict = dict()

	for i in range(len(f_input)):
		# tmp = f_input.readline().rstrip().split(',')
		tmp = f_input[i].rstrip().split('_')
		view_lat = tmp[4]
		view_lng = tmp[5]
		node_dict[i] = node(view_lat, view_lng, f_input[i].rstrip())

	# printResult = ""
	cluster_index = 0

	print "cluster center (lat, lng):"

	while (len(node_dict) != 0):

		center_node = node(node_dict[node_dict.keys()[0]].lat, node_dict[node_dict.keys()[0]].lng)

		is_stable = False
		in_cluster_array = []
		old_cluster_len = 0

		while (not is_stable):
			for key, value in node_dict.items():
				distance = calculate_distance_in_degree(center_node, value)
				if (distance <= min_radius):
					in_cluster_array.append(node(value.lat, value.lng, value.meta))
					del node_dict[key]

			new_cluster_len = len(in_cluster_array)

			sum_lat = 0
			sum_lng = 0
			for i in range(new_cluster_len):
				sum_lat += in_cluster_array[i].lat
				sum_lng += in_cluster_array[i].lng

			center_node = node(sum_lat/new_cluster_len, sum_lng/new_cluster_len)

			if (new_cluster_len == old_cluster_len):
				is_stable = True

			old_cluster_len = new_cluster_len

		# print "=== result ==="
		# print new_cluster_len
		print "%s,%s" % (center_node.lat, center_node.lng)
		# f_output.write("%s,%s\n" % (center_node.lat, center_node.lng))

		f_output.write("=== play with the %dth cluster ===\n" % cluster_index)
		f_output.write("%d\n" % new_cluster_len)
		f_output.write("center: %s,%s\n" % (center_node.lat, center_node.lng))
		for i in range(new_cluster_len):
			f_output.write("%s\n" % in_cluster_array[i].meta)
			f_output.write("%s\n" % basic_db_map[in_cluster_array[i].meta])

		cluster_index += 1

	# printResult = "%d\n%s" % (cluster_index, printResult)
	# f_output.write(printResult)