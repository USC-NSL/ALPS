import time



# ====== main =====
if __name__ == '__main__':
	start_time = time.time()

	query_city = open("./config/query_city.info", "r").readline().rstrip()
	query_landmark = open("./config/query_landmark.info", "r").readline().rstrip()

	work_dir = "./data/%s/%s/" % (query_city, query_landmark)

	f_input = open(work_dir + "adaptive_fov_analysis_output_formal.txt", "r").readlines()
	f_output = open(work_dir + "adaptive_fov_pretty_output.txt", "w")

	printResult = ""
	printTmp = ""

	seed_previous = 0
	image_count = 0

	for i in range(len(f_input) / 2):
		seed_current = int(f_input[i * 2][0:6])
		# print seed_current

		if (seed_current != seed_previous):
			# seed_previous = seed_current
			# image_count = 0
			# f_output.write("=== play with the %dth seed ===\n" % seed_current)

			printResult += "=== play with the %dth seed ===\n" % seed_previous
			printResult += "%d\n" % image_count
			printResult += printTmp

			seed_previous = seed_current
			image_count = 0
			printTmp = ""

		image_count += 1
		printTmp += "%s\n" % f_input[i * 2].rstrip()
		printTmp += "%s\n" % f_input[i * 2 + 1].rstrip()

	printResult += "=== play with the %dth seed ===\n" % seed_previous
	printResult += "%d\n" % image_count
	printResult += printTmp

	f_output.write(printResult)


	end_time = time.time()
	print "Running time: %s" % (end_time - start_time)
