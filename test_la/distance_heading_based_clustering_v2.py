import math
import utm
import numpy as np

class node():
	def __init__(self, lat, lng, theta = 0):
		self.lat = float(lat)
		self.lng = float(lng)
		self.theta = float(theta)

def heading_to_theta(heading):
	theta = 90 - heading
	return theta

def calculate_distance_in_degree(origin, destination):
	delta_lat = origin.lat - destination.lat
	delta_lng = origin.lng - destination.lng

	result = math.sqrt(delta_lat * delta_lat + delta_lng * delta_lng)

	return result

def easy_triangulation(my_array):

	location_dict = dict()
	heading_dict = dict()
	check_flag = False

	default_lat = ""
	default_lng = ""

	mysin = []
	mycos = []
	x = []
	y = []

	image_num = len(my_array)
	print "len: %d" % image_num

	for image_index in range(image_num):
		view_lat = my_array[image_index].lat
		view_lng = my_array[image_index].lng
		theta = my_array[image_index].theta * math.pi / 180

		mysin.append(math.sin(theta))
		mycos.append(math.cos(theta))

		# x.append(view_lat)
		# y.append(view_lng)

		xy = utm.from_latlon(view_lat, view_lng)

		x.append(xy[0])
		y.append(xy[1])

		check_key = "%s,%s" % (view_lat, view_lng)
		if check_key in location_dict:
			location_dict[check_key] += 1
		else:
			location_dict[check_key] = 1

		if theta in heading_dict:
			heading_dict[theta] += 1
		else:
			heading_dict[theta] = 1

		if (image_index == 0):
			default_lat = view_lat + 0.0001 * math.sin(theta * math.pi / 180)
			default_lng = view_lng + 0.0001 * math.cos(theta * math.pi / 180)

	if (len(location_dict) > 1 and len(heading_dict) > 1):
		check_flag = True

	if (check_flag):
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
		# tmp5 = np.dot(tmp4, h)

		# return node(tmp5[0][0], tmp5[1][0]), True
		theta = np.dot(tmp4, h)

		tmp = utm.from_latlon(view_lat, view_lng)
					
		tmp2 = utm.to_latlon(theta[0][0], theta[1][0], tmp[2], tmp[3])

		return node(tmp2[0], tmp2[1]), True
	else:
		return node(default_lat, default_lng), False

def project_seed_on_theta_line(seed_node, v3):
	new_seed_node = node(seed_node.lat, seed_node.lng, v3.theta + 90)
	return easy_triangulation([new_seed_node, v3])

# instead of convert it into x-y plane, here we calculate theta in lat-lng directly
def get_theta(origin, destination):
	theta = math.atan2(destination.lat - origin.lat, destination.lng - origin.lng) * 180 / math.pi
	return theta

# ====== main =====
if __name__ == '__main__':

	query_city = open("./config/query_city.info", "r").readline().rstrip()
	query_landmark = open("./config/query_landmark.info", "r").readline().rstrip()

	work_dir = "./data/%s/%s/" % (query_city, query_landmark)

	f_input = open(work_dir + "distance_based_clustering_output.txt", "r")
	# f_input = open(work_dir + "fake_input.txt", "r")
	f_output = open(work_dir + "distance_based_clustering_v2_output.txt", "w")

	query_fov = float(20.0)

	cluster_index = 0

	round_index = 0

	while (f_input.readline()):
		# print round_index
		# f_output.write("*** round: %d ***\n" % round_index)
		# f_output.write("=== play with the %dth cluster ===\n" % cluster_index)

		node_dict = dict()

		image_num = int(f_input.readline().rstrip())
		center_info = f_input.readline().rstrip()

		location_dict = dict()
		heading_dict = dict()
		check_flag = False
		default_lat = ""
		default_lng = ""

		for i in range(image_num):
			image_path = f_input.readline().rstrip()
			logo_detection_result = f_input.readline().rstrip()

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
			# tmp = f_input.readline().rstrip().split(',')
			# view_lat = float(tmp[0])
			# view_lng = float(tmp[1])
			# theta = float(f_input.readline().rstrip())

			node_dict[i] = node(view_lat, view_lng, theta)

			check_key = "%s,%s" % (view_lat, view_lng)
			if check_key in location_dict:
				location_dict[check_key] += 1
			else:
				location_dict[check_key] = 1

			if theta in heading_dict:
				heading_dict[theta] += 1
			else:
				heading_dict[theta] = 1

			if (i == 0):
				default_lat = view_lat + 0.0001 * math.sin(theta * math.pi / 180)
				default_lng = view_lng + 0.0001 * math.cos(theta * math.pi / 180)


		# for key, value in node_dict.items():
		if (len(location_dict) > 1 and len(heading_dict) > 1):
			check_flag = True

		if (not check_flag):
			f_output.write("=== play with the %dth cluster ===\n" % cluster_index)
			f_output.write("score: -1\n")
			f_output.write("%s,%s\n" % (default_lat, default_lng))
			cluster_index += 1

		else:
			while (len(node_dict) != 0):
				if (len(node_dict) == 1):
					# print "only one node left"
					break
				else:
					highest_score = 0
					highest_array = []
					for k1, v1 in node_dict.items():
						for k2, v2 in node_dict.items():
							if (k1 == k2):
								# print "*1"
								continue
							else:
								# print "v1: %s,%s" % (v1.lat, v1.lng)
								# print "v2: %s,%s" % (v2.lat, v2.lng)

								score = 2
								in_cluster_key = [k1, k2]
								seed_node, flag = easy_triangulation([v1, v2])
								if (not flag):
									# print "*2"
									continue
								else:
									# print "seed-node: %s,%s" % (seed_node.lat, seed_node.lng)
									for k3, v3 in node_dict.items():
										if (k3 == k1 or k3 == k2):
											# print "*3"
											continue
										else:
											projected_node, flag = project_seed_on_theta_line(seed_node, v3)
											if (not flag):
												# print "*4"
												continue
											else:
												# print "projected-node: %s,%s" % (projected_node.lat, projected_node.lng)
												projected_theta = get_theta(v3, projected_node)
												tmp_theta = abs(v3.theta - projected_theta) % 360
												if (tmp_theta < 45 or tmp_theta > 315):
													projected_distance = calculate_distance_in_degree(seed_node, projected_node)
													if (projected_distance < 0.0002):
														in_cluster_key.append(k3)
														# print "yes!"
												# else:
													# print "no!"
													# print v3.theta
													# print projected_theta

									score = len(in_cluster_key)
									if (score > highest_score):
										highest_score = score
										for i in range(score):
											highest_array = in_cluster_key[:]

					in_cluster_array = []
					for i in range(highest_score):
						tmp_node = node_dict[highest_array[i]]
						in_cluster_array.append(node(tmp_node.lat, tmp_node.lng, tmp_node.theta))
						del node_dict[highest_array[i]]

					final_seed_node, final_flag = easy_triangulation(in_cluster_array)

					f_output.write("=== play with the %dth cluster ===\n" % cluster_index)
					f_output.write("score: %d\n" % highest_score)
					# f_output.write("%d\n" % highest_score)
					if (not final_flag):
						# f_output.write("oops...\n")
						f_output.write("%s,%s\n" % (final_seed_node.lat, final_seed_node.lng))
					else:
						f_output.write("%s,%s\n" % (final_seed_node.lat, final_seed_node.lng))


					cluster_index += 1

		round_index += 1




