import argparse
import requests
from streamlink import Streamlink
import sys
import time

def get_channel_url(channel):
	return "twitch.tv/" + ["twitchmusic", "telnach_bcgbciecjbih", "telnach_bcgbdbjcjeah"][channel - 1]

def record_stream(channel, output_dir):
	filename = f"channel{channel}-{int(time.time())}.ts"

	streamlink = Streamlink()
	streamlink.set_loglevel("debug")
	streamlink.set_logoutput(output_dir + "/" + filename + ".log")
	streamlink.set_option("hls-live-edge", 9999999)
	streamlink.set_option("hls-segment-attempts", 99)
	streamlink.set_option("hls-segment-threads", 5)
	streamlink.set_option("hls-segment-timeout", 9999)

	streams = streamlink.streams(get_channel_url(channel))
	if not "best" in streams: 
		print("No stream found")
		return
	stream = streams["best"]
	print(f"Found stream {stream.url}")
	print("Writing stream to {}".format(output_dir + "/" + filename))
	with open(output_dir + "/" + filename, 'wb') as out_file, stream.open() as in_stream:
		while True:
			try:
				data = in_stream.read(1024)
			except:
				print("Got error while writing")
				return
			if not data:
				return
			out_file.write(data)

parser = argparse.ArgumentParser(description='Record Camp Flog Gnaw channel')
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