import argparse
import base64
import json
import requests
from streamlink import Streamlink
import sys
import time
from youtube_dl import YoutubeDL

TOKEN = 'vNVdglQOjFJJGG2U'
COUNTRY = 'BE'

def get_channel(channel):
	channel = channel - 1
	CHANNELS = [115942331, 115942449, 115942395]
	r = requests.get("https://api.tidal.com/v1/videos/{}/playbackinfoprepaywall?videoquality=HIGH&assetpresentation=FULL&countryCode={}&token={}".format(CHANNELS[channel], COUNTRY, TOKEN))
	resp = r.json()
	manifest = resp['manifest']
	decoded_manifest = json.loads(base64.b64decode(manifest))
	return decoded_manifest['urls'][0]

def record_stream(channel, output_dir):
	channel_url = get_channel(channel)
	print("Downloading from", channel_url)
	filename = "channel{}-{}.ts".format(channel, int(time.time()))

	streamlink = Streamlink()
	streamlink.set_loglevel("debug")
	streamlink.set_logoutput(output_dir + "/" + filename + ".log")
	streamlink.set_option("hls-live-edge", 9999999)
	streamlink.set_option("hls-segment-attempts", 99)
	streamlink.set_option("hls-segment-threads", 5)
	streamlink.set_option("hls-segment-timeout", 9999)

	streams = streamlink.streams(channel_url)
	stream = streams["best"]
	print("Found stream {}".format(stream.url))
	print("Writing stream to {}".format(output_dir + "/" + filename))
	with open(output_dir + "/" + filename, 'wb') as out_file, stream.open() as in_stream:
		while True:
			data = in_stream.read(1024)
			if not data:
				return
			out_file.write(data)

parser = argparse.ArgumentParser(description='Record a MIA channel')
parser.add_argument('channel')
parser.add_argument('-o', '--output-dir', default="./streams")

args = parser.parse_args()

if not args.channel:
	print("Supply a channel")
	exit()
channel = int(args.channel)

if channel < 1 or channel > 3:
	print("Channel must be one of 1, 2 and 3")
	exit()

while True:
	record_stream(channel, args.output_dir)
