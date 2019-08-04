import requests
import json
import os
import time
import sys
import datetime
import subprocess
from bs4 import BeautifulSoup
from subprocess import call

DEST_DIR = "."
SOURCE = "http://live.rockwerchter.be/nl/channel"
FILE = "artists-playing.txt"

while True:
	with open(FILE, 'a', encoding="utf-8") as infile:
		for num in range(1, 3):
			doc = requests.get(SOURCE + str(num))
			soup = BeautifulSoup(doc.text, 'html.parser')
			infile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
			infile.write("\n")
			elems = soup.select(".main > p")
			for elem in elems:
				if ("Nu op kanaal" in elem.string):
					print(elem.string)
					infile.write(elem.string + "\n")
	time.sleep(60 * 30)