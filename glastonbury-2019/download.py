import os

PROXY = ""

fo = open("sets.txt", "r")

for line in fo.readlines():
	os.system("youtube-dl -v -f bestvideo+bestaudio --proxy {} {}".format(PROXY, line))