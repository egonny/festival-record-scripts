import argparse
import requests
from streamlink import Streamlink
import sys
import time

def record_stream(output_dir):
	filename = "channel1-{}.ts".format(int(time.time()))

	streamlink = Streamlink()
	streamlink.set_loglevel("debug")
	streamlink.set_logoutput(output_dir + "/" + filename + ".log")
	streamlink.set_option("hls-live-edge", 9999999)
	streamlink.set_option("hls-segment-attempts", 99)
	streamlink.set_option("hls-segment-threads", 5)
	streamlink.set_option("hls-segment-timeout", 9999)

	streams = streamlink.streams("twitch.tv/twitchmusic")
	if not "best" in streams: 
		print("No stream found")
		return
	stream = streams["best"]
	print("Found stream {}".format(stream.url))
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

parser = argparse.ArgumentParser(description='Record Camp Flog Gnaw stream')
parser.add_argument('-o', '--output-dir', default="./streams")

args = parser.parse_args()

while True:
	record_stream(args.output_dir)