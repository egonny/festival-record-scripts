import requests
from streamlink import Streamlink
import sys
import time
from youtube_dl import YoutubeDL

# window._CONFIG_ = {"subscribe":"/subscribe","unsubscribe":"/unsubscribe","url":"https://coachella.withyoutube.com/","env":"youtube","ga":"UA-94059745-1","sch":"sch_EPRFW82HxP.json"};

# https://storage.googleapis.com/coachella-2019/schedules/sch_EPRFW82HxP.json?1555025819579

BASE_URL = "https://storage.googleapis.com/coachella-2019/"
DATA_URL = BASE_URL + "publish/data.json"
CHANNEL_URL = BASE_URL + "channels/{}-phase-{}-channels.json"

def get_general_data():
	resp = requests.get(url=DATA_URL)
	data = resp.json()
	
	return data

def get_schedule():
	pass

def get_channels(region, phase):
	resp = requests.get(url=CHANNEL_URL.format(region, phase))
	data = resp.json()
	
	return data["channels"]

if len(sys.argv) < 2:
	print("Supply a channel")
	exit()
channel = int(sys.argv[1])

if channel < 1 or channel > 3:
	print("Channel must be one of 1, 2 and 3")
	exit()

channels = get_channels("world", 2)
channel_url = "http://www.youtube.com/watch?v={}".format(channels[channel - 1])
print("Downloading from", channel_url)

ydl = YoutubeDL()
ydl.add_default_info_extractors()
info = ydl.extract_info(channel_url, download=False)
if info["uploader_id"] != "coachella":
	print("Uploader is not coachella, stopping")
	exit()

streamlink = Streamlink()
streamlink.set_loglevel("debug")
streamlink.set_logoutput(sys.stdout)
streamlink.set_option("hls-live-edge", 9999999)
streamlink.set_option("hls-segment-attempts", 99)
streamlink.set_option("hls-segment-threads", 5)
streamlink.set_option("hls-segment-timeout", 9999)

filename = "channel{}-{}.ts".format(channel, int(time.time()))
streams = streamlink.streams(channel_url)
stream = streams["best"]

print("Writing stream {} to {}".format(stream.url, filename))
with open("streams/" + filename, 'wb') as out_file, stream.open() as in_stream:
	while True:
		data = in_stream.read(1024)
		if not data:
			exit()
		out_file.write(data)