from libs import alps_lib
import urllib2
import os

query_city = open("./config/query_city.info", "r").readline().rstrip()
query_area = open("./config/query_area.info", "r").readline().rstrip()
work_dir = "./data/%s/%s/" % (query_city, query_area.replace(" ", "").replace(",", "|"))

f_input = open(work_dir + "04.adjust_standing_point_output.txt", "r")
f_output = open(work_dir + "05.download_image_with_zoom_output.txt", "w")

query_fov = "20"
query_key_google = open("./config/query_google_key.info", "r").readline().rstrip()

photo_dir = work_dir + "base_image_database/"
if not os.path.exists(photo_dir):
	os.makedirs(photo_dir)

class node():
	def __init__(self, lat, lng, theta = 0):
		self.lat = float(lat)
		self.lng = float(lng)
		self.theta = float(theta)

def save_photo(photo_url, photo_dir, photo_name):
	print photo_name
	f_output.write("%s\n" % photo_name)
	f_output.write("%s\n" % photo_url)

	fjpg = open(photo_dir + photo_name, "wb")
	fjpg.write(urllib2.urlopen(photo_url).read())
	fjpg.close()


def download_photo(tmp_node, way_index, way_id, node_index):
	query_lat = str(tmp_node.lat)
	query_lng = str(tmp_node.lng)

	heading0 = alps_lib.theta_to_heading(tmp_node.theta)

	for k in range(2):
		heading = heading0 + k * 180

		for i in range(-20, 40, 20): # -20, 0, 20
			for j in range(-15, 15, 10): # -15, -5, 5
				query_heading = str(float(heading) + i)
				query_pitch = str(j)

				query_heading_origin = str(heading)
				query_heading_index = str(i)
				query_pitch_index = str(j)

				photo_url = "https://maps.googleapis.com/maps/api/streetview?size=900x900&location=%s,%s&fov=%s&heading=%s&pitch=%s&key=%s" % (query_lat, query_lng, query_fov, query_heading, query_pitch, query_key_google)
				photo_name = "%s_%s_%s_%s_%s_%s_%s_h%s_p%s.jpg" % (str(way_index).zfill(6), str(way_id).zfill(12), str(node_index).zfill(6), str(k).zfill(2), query_lat, query_lng, query_heading_origin, query_heading_index, query_pitch_index)

				save_photo(photo_url, photo_dir, photo_name)

# ====== main =====
if __name__ == '__main__':

	# in case downloading is forced to stop
	# by some unpredicatable stuff...
	start_way_index = 0
	end_way_index = 99999
	start_node_index = 0

	way_index = 0
	while(f_input.readline()):
		way_id = f_input.readline().rstrip()
		node_num = int(f_input.readline().rstrip())
		for i in range(node_num):
			tmp = f_input.readline().rstrip().split(",")
			tmp_lat = tmp[0]
			tmp_lng = tmp[1]
			tmp_theta = f_input.readline().rstrip()
			tmp_node = node(tmp_lat, tmp_lng, tmp_theta)
				
			# for each node (lat, lng, theta), download several images
			if (way_index < end_way_index):
				if (way_index == start_way_index):
					if (i >= start_node_index):
						download_photo(tmp_node, way_index, way_id, i)
				if (way_index > start_way_index):
					download_photo(tmp_node, way_index, way_id, i)


		way_index += 1


