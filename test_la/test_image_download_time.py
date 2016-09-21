import urllib2
import time
import os

photo_url = "https://maps.googleapis.com/maps/api/streetview?size=900x900&location=37.3995829857,-122.110309914&fov=20&heading=8.091355092&pitch=-5&key=AIzaSyBranwjpavQoj2xAtn6qeRARxURQeTD13M"

start_time = time.time()
# print start_time

read_time = 0

photo_dir = "%s/" % start_time
if not os.path.exists(photo_dir):
	os.makedirs(photo_dir)

for i in range(1):
	fjpg = open("%s/%s.jpg" % (photo_dir, str(i).zfill(4)), "wb")

	tmp = time.time()
	fjpg.write(urllib2.urlopen(photo_url).read())
	read_time += float(time.time()) - float(tmp)
	fjpg.close()

end_time = time.time()
print "time: %s" % (end_time - start_time)