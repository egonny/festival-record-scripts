import argparse
import requests
from streamlink import Streamlink
import sys
import time
from youtube_dl import YoutubeDL

def get_channels():
	return ["Qo17IbsXXaQ"]

def record_stream(channel, output_dir):
	channels = get_channels()
	channel_url = "http://www.youtube.com/watch?v={}".format(channels[channel - 1])
	print("Downloading from", channel_url)

	ydl = YoutubeDL()
	ydl.add_default_info_extractors()

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

parser = argparse.ArgumentParser(description='Record a EDC Mexico channel')
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
