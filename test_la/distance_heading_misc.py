import time


query_city = open("./config/query_city.info", "r").readline().rstrip()
query_landmark = open("./config/query_landmark.info", "r").readline().rstrip()
work_dir = "./data/%s/%s/" % (query_city, query_landmark)

f_input = open(work_dir + "distance_heading_based_clustering_output.txt", "r")
f_output_cluster = open(work_dir + "distance_based_clustering_output.txt", "w")
f_output_seed = open(work_dir + "do_triangulation_for_seed_location_output.txt", "w")

# ====== main =====
if __name__ == '__main__':
	start_time = time.time()

	cluster_index = 0

	while (f_input.readline()):

		f_output_seed.write("=== play with the %dth cluster ===\n" % cluster_index)
		f_output_cluster.write("=== play with the %dth cluster ===\n" % cluster_index)

		image_num = int(f_input.readline().rstrip())
		f_output_cluster.write("%d\n" % image_num)

		center_info = f_input.readline().rstrip()
		f_output_seed.write("%s\n" % center_info)
		f_output_cluster.write("%s\n" % center_info)

		seed_info = f_input.readline().rstrip().split(": ")[1]
		f_output_seed.write("%s\n" % seed_info)

		for i in range(image_num):
			tmp = f_input.readline().rstrip()
			f_output_cluster.write("%s\n" % tmp)
			tmp = f_input.readline().rstrip()
			f_output_cluster.write("%s\n" % tmp)

		cluster_index += 1
		



	end_time = time.time()
	print "Running time: %s" % (end_time - start_time)


