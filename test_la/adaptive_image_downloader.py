import urllib2
import os

query_city = open("./config/query_city.info", "r").readline().rstrip()
query_landmark = open("./config/query_landmark.info", "r").readline().rstrip()

work_dir = "./data/%s/%s/" % (query_city, query_landmark)

f_input = open(work_dir + "adaptive_location_generator_output.txt", "r")
f_output = open(work_dir + "adaptive_image_downloader_output.txt", "w")

query_fov = "20"

query_key_google = open("./config/query_google_key.info", "r").readline().rstrip()

photo_dir = work_dir + "adaptive_image_database/"
if not os.path.exists(photo_dir):
	os.makedirs(photo_dir)

class node():
	def __init__(self, lat, lng, theta = 0):
		self.lat = float(lat)
		self.lng = float(lng)
		self.theta = float(theta)

def theta_to_heading(theta):
	heading = 90 - theta
	return heading

def save_photo(photo_url, photo_dir, photo_name):
	print photo_name
	f_output.write("%s\n" % photo_name)
	f_output.write("%s\n" % photo_url)

	fjpg = open(photo_dir + photo_name, "wb")
	fjpg.write(urllib2.urlopen(photo_url).read())
	fjpg.close()

def download_photo(tmp_node, seed_index, image_index):
	query_lat = str(tmp_node.lat)
	query_lng = str(tmp_node.lng)

	bearing = theta_to_heading(tmp_node.theta)

	for i in range(-20, 40, 20):
		for j in range(-15, 15, 10):
			query_heading = str(float(bearing) + i)
			query_pitch = str(j)

			query_heading_origin = str(bearing)
			query_heading_index = str(i)
			query_pitch_index = str(j)		

			photo_url = "https://maps.googleapis.com/maps/api/streetview?size=900x900&location=%s,%s&fov=%s&heading=%s&pitch=%s&key=%s" % (query_lat, query_lng, query_fov, query_heading, query_pitch, query_key_google)
			photo_name = "%s_%s_%s_%s_%s_h%s_p%s.jpg" % (str(seed_index).zfill(6), str(image_index).zfill(6), query_lat, query_lng, query_heading_origin, query_heading_index, query_pitch_index)

			save_photo(photo_url, photo_dir, photo_name)


# ====== main =====
if __name__ == '__main__':

	start_seed_index = 0
	end_seed_index = 99999
	start_image_index = 0


	seed_index = 0
	while (f_input.readline()):
		image_num = int(f_input.readline().rstrip())

		for image_index in range(image_num):
			tmp = f_input.readline().rstrip().split(',')
			tmp_lat = tmp[0]
			tmp_lng = tmp[1]
			tmp_theta = f_input.readline().rstrip()

			tmp_node = node(tmp_lat, tmp_lng, tmp_theta)

			if (seed_index < end_seed_index):
				if (seed_index == start_seed_index):
					if (image_index >= start_image_index):
						download_photo(tmp_node, seed_index, image_index)
				if (seed_index > start_seed_index):
					download_photo(tmp_node, seed_index, image_index)


		seed_index += 1

