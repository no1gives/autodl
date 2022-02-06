import youtube_dl
from threading import Thread
import requests
import time
import argparse 
import sys
from datetime import datetime

class Logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def hook(d):
    if d['status'] == 'finished':
        print(f'Download finished. {d}')

OPTIONS  = {
    'outtmpl': "videos/%(id)s/%(title)s.%(ext)s",
    'logger': Logger(),
    'progress_hooks': [hook],
    'format': 'bestaudio/best',
    'hls_use_mpegts': True,
    'ignoreerrors': False,
}

class Downloader(object):
    
    def __init__(self, username, options):
        self.username = username
        self.options = options
        self.recording = False
        self.log(f"init(): Starting process to record {username}")

    def log(self, input):
        print(f"{self.username}@{datetime.now().time()}: {input}")

    def alive(self):
        url = "https://chaturbate.com/get_edge_hls_url_ajax/"
        headers = {"X-Requested-With": "XMLHttpRequest"}
        data = {"room_slug": self.username, "bandwidth": "high"}

        time.sleep(3)  # fix issue 30
        r = requests.post(url, headers=headers, data=data)
        result = r.json()
        self.log(f"alive(): request json: {result}")
        if "room_status" in result:
            if result["room_status"] == "public":
                return True

        return False

    def download(self):
        # # check if already downloading
        # if self.recording:
        #     self.log(f"download(): Already downloading {self.username}")
        #     return

        try:
            if self.alive():
                with youtube_dl.YoutubeDL(self.options) as ydl:
                    ydl.download([f"https://chaturbate.com/{self.username}/"])
                    # self.recording = True
                    self.log(f"download(): Starting download for {self.username}")
        except Exception as err:
            self.log(f"download(): I got an error: {err}:{sys.exc_info()[0]}")
            # self.recording = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("streamer", default="yuanlili", help="Streamer you want to watch")

    args = parser.parse_args()
    d = Downloader(args.streamer, OPTIONS)
    while True:
        d.download()
        time.sleep(60)