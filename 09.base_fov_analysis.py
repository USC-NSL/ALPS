# ====== main =====
if __name__ == '__main__':

	query_city = open("./config/query_city.info", "r").readline().rstrip()
	query_area = open("./config/query_area.info", "r").readline().rstrip()
	query_landmark = open("./config/query_landmark.info", "r").readline().rstrip()
	work_dir = "./data/%s/%s/%s/" % (query_city, query_area.replace(" ", "").replace(",", "|"), query_landmark)

	f1 = open(work_dir + "07.base_fov_check_output.txt", "r").readlines()
	f2 = open(work_dir + "08.base_fov_database_detection_res_output.txt", "r").readlines()

	f3 = open(work_dir + "09b.base_fov_analysis_tmp.txt", "w")
	f4 = open(work_dir + "09.base_fov_analysis_output.txt", "w")

	d = dict()

	f1_len = len(f1)
	f2_len = len(f2)

	for i in range(f1_len / 2):
		tmp = f1[i * 2].rstrip()
		d[tmp] = 0

	for i in range(f2_len / 2):
		tmp = f2[i * 2].rstrip()
		d[tmp] += 1

	f1 = open(work_dir + "07.base_fov_check_output.txt", "r").readlines()

	for i in range(f1_len / 12):
		tmp1 = f1[i * 12].rstrip()
		tmp2 = f1[i * 12 + 2].rstrip()
		tmp3 = f1[i * 12 + 4].rstrip()
		tmp4 = f1[i * 12 + 6].rstrip()
		tmp5 = f1[i * 12 + 8].rstrip()
		tmp6 = f1[i * 12 + 10].rstrip()

		f3.write("%s %d %d %d %d %d %d\n" % (tmp1[:-10].ljust(100), d[tmp1], d[tmp2], d[tmp3], d[tmp4], d[tmp5], d[tmp6]))

		tmp7 = int(d[tmp1]) + int(d[tmp2]) + int(d[tmp3]) + int(d[tmp4]) + int(d[tmp5]) + int(d[tmp6])
		if (tmp7 >= 4):
			f4.write("%s\n" % tmp1[:-10])