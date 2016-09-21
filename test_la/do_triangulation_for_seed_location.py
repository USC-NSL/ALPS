import math
import utm
import numpy as np



def heading_to_theta(heading):
	theta = 90 - heading
	return theta


# ====== main =====
if __name__ == '__main__':

	query_city = open("./config/query_city.info", "r").readline().rstrip()
	query_landmark = open("./config/query_landmark.info", "r").readline().rstrip()

	work_dir = "./data/%s/%s/" % (query_city, query_landmark)

	f_input = open(work_dir + "distance_based_clustering_output.txt", "r")
	f_output = open(work_dir + "do_triangulation_for_seed_location_output.txt", "w")

	query_fov = float(20.0)

	# cluster_num = f_input.readline().rstrip()
	cluster_index = 0

	while (f_input.readline()):
		f_output.write("=== play with the %dth cluster ===\n" % cluster_index)
		print "=== play with the %dth cluster ===" % cluster_index

		image_num = int(f_input.readline().rstrip())

		center_info = f_input.readline().rstrip()
		f_output.write("%s\n" % center_info)

		check_we_have_image_from_more_than_one_point = dict()
		check_result_flag = False
		default_lat = "" # ****************
		default_lng = ""

		mysin = []
		mycos = []
		x = []
		y = []

		check_two_image_are_actually_from_same_location_even_though_their_meta_is_different = dict()
		image_num_real = 0

		for image_index in range(image_num):
			image_path = f_input.readline().rstrip()
			logo_detection_result = f_input.readline().rstrip()

			if logo_detection_result in check_two_image_are_actually_from_same_location_even_though_their_meta_is_different:
				continue
			else:
				check_two_image_are_actually_from_same_location_even_though_their_meta_is_different[logo_detection_result] = 1
				image_num_real += 1

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

			theta = heading_to_theta(view_heading_new) * math.pi / 180

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

			if (image_index == 0):
				default_lat = view_lat + 0.0001 * math.sin(theta)
				default_lng = view_lng + 0.0001 * math.cos(theta)
				# default_lat_lng = "%s,%s" % (tmp_lat, tmp_lng)

		if (len(check_we_have_image_from_more_than_one_point) > 1):
			check_result_flag = True

			G = []

			for i in range(image_num_real):
				G.append(mysin[i])
				G.append(-mycos[i])

			G = np.reshape(G, (image_num_real, 2))

			h = []

			for i in range(image_num_real):
				h.append(x[i] * mysin[i] - y[i] * mycos[i])

			h = np.reshape(h, (image_num_real, 1))

			tmp1 = G.transpose()
			tmp2 = np.dot(tmp1, G)
			tmp3 = np.linalg.inv(tmp2)
			tmp4 = np.dot(tmp3, tmp1)
			theta = np.dot(tmp4, h)

			tmp = utm.from_latlon(view_lat, view_lng)
					
			tmp2 = utm.to_latlon(theta[0][0], theta[1][0], tmp[2], tmp[3])

		# if (check_result_flag):
			f_output.write("%s,%s\n" % (str(tmp2[0]), str(tmp2[1])))
			print "%s,%s" % (str(tmp2[0]), str(tmp2[1]))
		else:
			# f_output.write("there isn't enough image from different view point...\n")
			# print "there isn't enough image from different view point..."
			f_output.write("%s,%s\n" % (default_lat, default_lng))
			print "%s,%s" % (default_lat, default_lng)


		cluster_index += 1


