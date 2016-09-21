import math
import utm

class node():
	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)

def calculate_distance(n1, n2):
	dx = n1.x - n2.x
	dy = n1.y - n2.y

	result = math.sqrt(dx * dx + dy * dy)

	return result


# ====== main =====
if __name__ == '__main__':

	f1 = open("ground_truth.txt", "r").readlines()
	f2 = open("l2m_output.txt", "r").readlines()

	f1_array = []
	f2_array = []

	for i in range(len(f1)):
		tmp = f1[i].rstrip().split(',')
		xy = utm.from_latlon(float(tmp[0]), float(tmp[1]))

		f1_array.append(node(xy[0], xy[1]))

	for i in range(len(f2)):
		tmp = f2[i].rstrip().split(',')
		xy = utm.from_latlon(float(tmp[0]), float(tmp[1]))

		f2_array.append(node(xy[0], xy[1]))

	for i in range(len(f1)):
		min_dis = 100
		for j in range(len(f2)):
			distance = calculate_distance(f1_array[i],f2_array[j])
			if (distance < min_dis):
				min_dis = distance

		if (min_dis < 20):
			# print "%s,%s" % (f1_array[i].lat, f1_array[i].lng)
			# print "%s" % f1[i].rstrip()
			print "%f" % min_dis
		# else:
		# 	# print "%s,%s" % (f1_array[i].lat, f1_array[i].lng)
		# 	print "%s" % f1[i].rstrip()
		# 	print "too large: %f" % min_dis