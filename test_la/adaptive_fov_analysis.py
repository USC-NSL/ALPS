import time





# ====== main =====
if __name__ == '__main__':
	start_time = time.time()

	query_city = open("./config/query_city.info", "r").readline().rstrip()
	query_landmark = open("./config/query_landmark.info", "r").readline().rstrip()

	work_dir = "./data/%s/%s/" % (query_city, query_landmark)


	f1 = open(work_dir + "adaptive_fov_downloader_output.txt", "r").readlines()
	f2 = open(work_dir + "adaptive_fov_downloader_yolo_result.txt", "r").readlines()

	f3 = open(work_dir + "adaptive_fov_analysis_output.txt", "w")
	f4 = open(work_dir + "adaptive_fov_analysis_output_formal.txt", "w")

	adaptive_db_map = dict()
	f5 = open(work_dir + "adaptive_image_downloader_yolo_result.txt", "r").readlines()
	for i in range(len(f5) / 2):
		adaptive_db_map[f5[i * 2].rstrip()[:-4]] = f5[i * 2 + 1].rstrip()

	d = dict()

	f1_len = len(f1)
	# print f1_len
	f2_len = len(f2)
	# print f2_len

	for i in range(f1_len / 2):
		tmp = f1[i * 2].rstrip()
		# print tmp
		d[tmp] = 0
		# f1.readline()

	for i in range(f2_len / 2):
		tmp = f2[i * 2].rstrip()
		# print tmp
		d[tmp] += 1
		# f2.readline()

	# f1.close()

	f1 = open(work_dir + "adaptive_fov_downloader_output.txt", "r").readlines()
	for i in range(f1_len/12):
		tmp1 = f1[i * 12].rstrip()
		# f1.readline()
		tmp2 = f1[i * 12 + 2].rstrip()
		# f1.readline()
		tmp3 = f1[i * 12 + 4].rstrip()
		# f1.readline()
		tmp4 = f1[i * 12 + 6].rstrip()
		# f1.readline()
		tmp5 = f1[i * 12 + 8].rstrip()
		# f1.readline()
		tmp6 = f1[i * 12 + 10].rstrip()
		# f1.readline()

		f3.write("%s %d %d %d %d %d %d\n" % (tmp1[:-10].ljust(100), d[tmp1], d[tmp2], d[tmp3], d[tmp4], d[tmp5], d[tmp6]))

		tmp7 = int(d[tmp1]) + int(d[tmp2]) + int(d[tmp3]) + int(d[tmp4]) + int(d[tmp5]) + int(d[tmp6])
		if (tmp7 >= 4):
			f4.write("%s\n" % tmp1[:-10])
			f4.write("%s\n" % adaptive_db_map[tmp1[:-10]])

	end_time = time.time()
	print "Running time: %s" % (end_time - start_time)