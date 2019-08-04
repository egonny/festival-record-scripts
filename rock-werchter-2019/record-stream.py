import requests
import json
import os
import time
import sys
import threading
from bs4 import BeautifulSoup
from streamlink import Streamlink

class PeriodicThread(object):
    """
    Python periodic Thread using Timer with instant cancellation
    """

    def __init__(self, callback=None, period=1, name=None, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.callback = callback
        self.period = period
        self.stop = False
        self.current_timer = None
        self.schedule_lock = threading.Lock()

    def start(self):
        """
        Mimics Thread standard start method
        """
        self.schedule_timer()

    def run(self):
        """
        By default run callback. Override it if you want to use inheritance
        """
        if self.callback is not None:
            self.callback()

    def _run(self):
        """
        Run desired callback and then reschedule Timer (if thread is not stopped)
        """
        try:
            self.run()
        except Exception:
            logging.exception("Exception in running periodic thread")
        finally:
            with self.schedule_lock:
                if not self.stop:
                    self.schedule_timer()

    def schedule_timer(self):
        """
        Schedules next Timer run
        """
        self.current_timer = threading.Timer(self.period, self._run, *self.args, **self.kwargs)
        if self.name:
            self.current_timer.name = self.name
        self.current_timer.start()

    def cancel(self):
        """
        Mimics Timer standard cancel method
        """
        with self.schedule_lock:
            self.stop = True
            if self.current_timer is not None:
                self.current_timer.cancel()

    def join(self):
        """
        Mimics Thread standard join method
        """
        self.current_timer.join()

DEST_DIR = "werchter"
SOURCE = "https://videocenter.proximusmwc.be/event/stage"

def download_stream(channel_url, output_dir, filename):
	streamlink = Streamlink()
	streamlink.set_loglevel("debug")
	streamlink.set_logoutput(output_dir + "/" + filename + ".log")
	streamlink.set_option("hls-live-edge", 9999999)
	streamlink.set_option("hls-segment-attempts", 99)
	streamlink.set_option("hls-segment-threads", 5)
	streamlink.set_option("hls-segment-timeout", 9999)

	streams = streamlink.streams(channel_url.replace("https", "http"))
	stream = streams["best"]
	print("Found stream {}".format(stream.url))
	print("Writing stream to {}".format(output_dir + "/" + filename))
	with open(output_dir + "/" + filename, 'wb') as out_file, stream.open() as in_stream:
		while True:
			try:
				data = in_stream.read(1024)
				if not data:
					return
				out_file.write(data)
			except IOError:
				return

def download_stream_thread(channel_url, output_dir, filename, timer):
	download_stream(channel_url, output_dir, filename)
	timer.cancel()

def periodic_stream_loop(channel = "1"):
	url = ""
	if (channel == "1"):
		url = SOURCE + "1"
	else:
		url = SOURCE + "2"

	print(url)
	while True:
		timer = PeriodicThread(period=60 * 90)
		r = requests.get(url + "/getStreamUrl", headers={"referer": url})
		stream = r.json()['hls']
		print(stream)
		file = "channel-" + channel + "-" + str(int(time.time())) + ".ts"
		download_thread = threading.Thread(target=download_stream_thread, args=(stream, DEST_DIR, file, timer))
		download_thread.daemon = True
		timer.daemon = True
		timer.start()
		download_thread.start()
		try:
			timer.join()
		except KeyboardInterrupt:
			sys.exit()

periodic_stream_loop(sys.argv[1])