import glob

# ====== main =====
if __name__ == '__main__':

	query_city = open("./config/query_city.info", "r").readline().rstrip()
	# query_landmark = open("./config/query_landmark.info", "r").readline().rstrip()
	query_landmark = "subway"

	work_dir = "./data/%s/%s/" % (query_city, query_landmark)


	# ===============================================================================
	file_name = "fov_analysis_output_formal.txt"
	# ===============================================================================

	f_input = open(work_dir + file_name, "r").readlines()

	# for i in range(len(f_input) / 2):
	# 	tmp = f_input[i * 2].rstrip()[:-4].split('_')
	# 	print "%s,%s" % (tmp[4], tmp[5])

	for i in range(len(f_input)):
		tmp = f_input[i].rstrip().split('_')
		print "%s,%s" % (tmp[4], tmp[5])