import math
import utm
import numpy as np
import time

query_city = open("./config/query_city.info", "r").readline().rstrip()
query_landmark = open("./config/query_landmark.info", "r").readline().rstrip()
work_dir = "./data/%s/%s/" % (query_city, query_landmark)

query_fov = float(20.0)

# f_input = open(work_dir + "fov_analysis_output_formal_test_dh_clustering.txt", "r").readlines()
f_input = open(work_dir + "fov_analysis_output_formal.txt", "r").readlines()
f_output = open(work_dir + "distance_heading_based_clustering_output.txt", "w")

class node():
	def __init__(self, lat, lng, theta = 0, meta = "", misc = ""):
		self.lat = float(lat)
		self.lng = float(lng)
		self.theta = float(theta)
		self.meta = str(meta)
		self.misc = str(misc)

# instead of convert it into x-y plane, here we calculate theta in lat-lng directly
def get_theta(origin, destination):

	# print "origin: %f,%f" % (origin.lat, origin.lng)
	# print "destination: %f,%f" % (destination.lat, destination.lng)

	theta = math.atan2(destination.lat - origin.lat, destination.lng - origin.lng) * 180 / math.pi
	return theta

def calculate_distance_in_degree(origin, destination):
	delta_lat = origin.lat - destination.lat
	delta_lng = origin.lng - destination.lng

	result = math.sqrt(delta_lat * delta_lat + delta_lng * delta_lng)

	return result

def heading_to_theta(heading):
	theta = 90 - heading
	return theta

def do_triangulation(my_array):

	# print "new_triangulation"
	# print "len = %d" % len(my_array)

	check_we_have_image_from_more_than_one_point = dict()
	check_we_have_image_from_more_than_one_heading = dict()
	check_result_flag = False
	default_lat = "" # ****************
	default_lng = ""

	mysin = []
	mycos = []
	x = []
	y = []

	image_num = len(my_array)

	for image_index in range(image_num):
		view_lat = my_array[image_index].lat
		view_lng = my_array[image_index].lng
		theta = my_array[image_index].theta * math.pi / 180
		meta = my_array[image_index].meta
		misc = my_array[image_index].misc

		# print "%f,%f,%f" % (view_lat, view_lng, theta)
		# print "%s" % meta
		# print "%s" % misc

		mysin.append(math.sin(theta))
		mycos.append(math.cos(theta))

		xy = utm.from_latlon(view_lat, view_lng)

		x.append(xy[0])
		y.append(xy[1])

		# new stuff to deal with the case
		# when all images come from the same standing point
		check_key = "%s,%s" % (view_lat, view_lng)
		if check_key in check_we_have_image_from_more_than_one_point:
			check_we_have_image_from_more_than_one_point[check_key] += 1
		else:
			check_we_have_image_from_more_than_one_point[check_key] = 1

		if theta in check_we_have_image_from_more_than_one_heading:
			check_we_have_image_from_more_than_one_heading[theta] += 1
		else:
			check_we_have_image_from_more_than_one_heading[theta] = 1

		if (image_index == 0):
			default_lat = view_lat + 0.0001 * math.sin(theta)
			default_lng = view_lng + 0.0001 * math.cos(theta)
	
	if (len(check_we_have_image_from_more_than_one_point) > 1 and len(check_we_have_image_from_more_than_one_heading) > 1):
		check_result_flag = True

	if (check_result_flag):

		G = []

		for i in range(image_num):
			G.append(mysin[i])
			G.append(-mycos[i])

		G = np.reshape(G, (image_num, 2))

		h = []

		for i in range(image_num):
			h.append(x[i] * mysin[i] - y[i] * mycos[i])

		h = np.reshape(h, (image_num, 1))

		tmp1 = G.transpose()
		tmp2 = np.dot(tmp1, G)
		tmp3 = np.linalg.inv(tmp2)
		tmp4 = np.dot(tmp3, tmp1)
		theta = np.dot(tmp4, h)

		tmp = utm.from_latlon(view_lat, view_lng)
					
		tmp2 = utm.to_latlon(theta[0][0], theta[1][0], tmp[2], tmp[3])

		return node(tmp2[0], tmp2[1])
	else:
		return node(default_lat, default_lng)





# ====== main =====
if __name__ == '__main__':
	start_time = time.time()

	min_radius = 0.0005

	basic_db_map = dict()
	tmp = open(work_dir + "basic_image_database_yolo_result.txt", "r").readlines()
	for i in range(len(tmp) / 2):
		basic_db_map[tmp[i * 2].rstrip()[:-4]] = tmp[i * 2 + 1].rstrip()

	node_dict = dict()

	for i in range(len(f_input)):
		# tmp = f_input[i].rstrip().split('_')
		# view_lat = tmp[4]
		# view_lng = tmp[5]
		# node_dict[i] = node(view_lat, view_lng, f_input[i].rstrip())

		image_path = f_input[i].rstrip()
		logo_detection_result = basic_db_map[image_path]

		# print image_path
		# print logo_detection_result

		tmp = image_path.split('_')
		view_lat = float(tmp[4])
		view_lng = float(tmp[5])
		view_heading = float(tmp[6]) + float(tmp[7][1:])
		view_pitch = float(tmp[8][1:])

		tmp = logo_detection_result.split('/')
		photo_pixel_width = float(tmp[0])
		photo_pixel_height = float(tmp[1])
		logo_pixel_left = float(tmp[2])
		logo_pixel_right = float(tmp[3])
		logo_pixel_top = float(tmp[4])
		logo_pixel_down = float(tmp[5])

		logo_pixel_horizontal = (logo_pixel_left + logo_pixel_right) / 2

		distance_pixel = photo_pixel_width / (2 * math.tan(0.5 * query_fov * math.pi / 180))

		relative_heading = math.atan2(logo_pixel_horizontal - photo_pixel_width / 2, distance_pixel) * 180 / math.pi
		view_heading_new = view_heading + relative_heading

		theta = heading_to_theta(view_heading_new)

		node_dict[i] = node(view_lat, view_lng, theta, image_path, logo_detection_result)


	cluster_index = 0

	while (len(node_dict) != 0):

		center_node = node(node_dict[node_dict.keys()[0]].lat, node_dict[node_dict.keys()[0]].lng, node_dict[node_dict.keys()[0]].theta, node_dict[node_dict.keys()[0]].meta, node_dict[node_dict.keys()[0]].misc)

		is_stable = False
		in_cluster_array = []
		old_cluster_len = 0

		tmp_count = 0

		while (not is_stable):
			
			for key, value in node_dict.items():

				# print "=== round %d ===" % tmp_count

				if (tmp_count == 0):
					in_cluster_array.append(node(value.lat, value.lng, value.theta, value.meta, value.misc))
					# print "1"
					# print "%f,%f" % (value.lat, value.lng)
					# print "%f" % value.theta
					del node_dict[key]

				else:
					distance = calculate_distance_in_degree(center_node, value)
					if (distance <= min_radius):
						in_cluster_array.append(node(value.lat, value.lng, value.theta, value.meta, value.misc))
						seed_node = do_triangulation(in_cluster_array)
						seed_theta = get_theta(node(value.lat, value.lng), seed_node)

						tmp_value = abs(seed_theta - value.theta) % 360

						if (tmp_value > 45 and tmp_value < 315):
							# print "2"
							# print "%f,%f" % (value.lat, value.lng)
							# print "%f" % value.theta
							# print "%f,%f" % (seed_node.lat, seed_node.lng)
							# print "%f" % seed_theta
							del in_cluster_array[-1]
						else:
							del node_dict[key]
							# print "3"
					# else:
						# print "4"

				tmp_count += 1

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

		# print "=== play with the %dth cluster ===" % cluster_index
		# print "center: %s,%s" % (center_node.lat, center_node.lng)

		f_output.write("=== play with the %dth cluster ===\n" % cluster_index)
		f_output.write("%d\n" % new_cluster_len)
		f_output.write("center: %s,%s\n" % (center_node.lat, center_node.lng))

		seed_node = do_triangulation(in_cluster_array)
		f_output.write("seed: %s,%s\n" % (seed_node.lat, seed_node.lng))
		print "%s,%s" % (seed_node.lat, seed_node.lng)

		for i in range(new_cluster_len):
			f_output.write("%s\n" % in_cluster_array[i].meta)
			f_output.write("%s\n" % basic_db_map[in_cluster_array[i].meta])
			# f_output.write("%s,%s\n" % (str(in_cluster_array[i].lat), str(in_cluster_array[i].lng)))
			# f_output.write("%s\n" % str(in_cluster_array[i].theta))

		cluster_index += 1


	end_time = time.time()
	print "Running time: %s" % (end_time - start_time)