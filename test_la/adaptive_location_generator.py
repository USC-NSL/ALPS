import math
import utm



class node():
	def __init__(self, lat, lng):
		self.lat = float(lat)
		self.lng = float(lng)
		# self.theta = float(theta)
		# self.meta = str(meta)

def heading_to_theta(heading):
	theta = 90 - heading
	return theta

def theta_to_heading(theta):
	heading = 90 - theta
	return heading

# point in x-y plane
class point():
	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)

def get_heading(origin, destination):
	# convert origin from lat-lng to xy
	xy = utm.from_latlon(origin.lat, origin.lng)
	originXY = point(float(xy[0]), float(xy[1]))
	# convert destination from lat-lng to xy
	xy = utm.from_latlon(destination.lat, destination.lng)
	destinationXY = point(float(xy[0]), float(xy[1]))

	theta = math.atan2(destinationXY.y - originXY.y, destinationXY.x - originXY.x) * 180 / math.pi
	heading = theta_to_heading(theta)

	return heading

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
	f_seed = open(work_dir + "do_triangulation_for_seed_location_output.txt", "r").readlines()
	f_output = open(work_dir + "adaptive_location_generator_output.txt", "w")

	cluster_index = 0

	while (f_input.readline()):
		f_output.write("=== play with the %dth cluster ===\n" % cluster_index)

		image_num = int(f_input.readline().rstrip())
		# f_output.write("%d\n" % (image_num * 3))

		f_input.readline() # no use...

		tmp_seed = f_seed[cluster_index * 3 + 2].rstrip().split(',')
		# print "%s,%s" % (tmp_seed[0], tmp_seed[1])
		seed_node = node(tmp_seed[0], tmp_seed[1])

		image_index = 0
		check_dict = dict()
		printResult = ""

		for i in range(image_num):
			image_path = f_input.readline().rstrip()
			logo_detection_result = f_input.readline().rstrip()

			tmp = image_path.split('_')
			view_lat = float(tmp[4])
			view_lng = float(tmp[5])
			view_heading = float(tmp[6]) # this heading should be perpendicular to the road

			# ***
			check_key = "%s,%s" % (view_lat, view_lng)
			if check_key in check_dict:
				continue
			else:
				image_index += 1
				check_dict[check_key] = 1

			theta_middle = heading_to_theta(view_heading) * math.pi / 180
			theta_left = theta_middle + math.pi / 2
			theta_right = theta_middle - math.pi / 2

			# node in middle
			node_middle = node(view_lat, view_lng)
			# heading_middle = get_heading(node_middle, seed_node)
			theta_to_seed_middle = get_theta(node_middle, seed_node)
			# f_output.write("%s,%s\n" % (str(node_middle.lat), str(node_middle.lng)))
			# f_output.write("%s\n" % str(heading_middle))
			printResult += "%s,%s\n" % (str(node_middle.lat), str(node_middle.lng))
			printResult += "%s\n" % str(theta_to_seed_middle)

			# node on left
			tmp_lat = view_lat + 0.0001 * math.sin(theta_left)
			tmp_lng = view_lng + 0.0001 * math.cos(theta_left)
			node_left = node(tmp_lat, tmp_lng)
			# heading_left = get_heading(node_left, seed_node)
			theta_to_seed_left = get_theta(node_left, seed_node)
			# f_output.write("%s,%s\n" % (str(node_left.lat), str(node_left.lng)))
			# f_output.write("%s\n" % str(heading_left))
			printResult += "%s,%s\n" % (str(node_left.lat), str(node_left.lng))
			printResult += "%s\n" % str(theta_to_seed_left)


			# node on right
			tmp_lat = view_lat + 0.0001 * math.sin(theta_right)
			tmp_lng = view_lng + 0.0001 * math.cos(theta_right)
			node_right = node(tmp_lat, tmp_lng)
			# heading_right = get_heading(node_right, seed_node)
			theta_to_seed_right = get_theta(node_right, seed_node)
			# f_output.write("%s,%s\n" % (str(node_right.lat), str(node_right.lng)))
			# f_output.write("%s\n" % str(heading_right))
			printResult += "%s,%s\n" % (str(node_right.lat), str(node_right.lng))
			printResult += "%s\n" % str(theta_to_seed_right)

		printResult = "%d\n%s" % (image_index * 3, printResult)
		f_output.write(printResult)




		cluster_index += 1