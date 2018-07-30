#!/usr/bin/python3

import os
import re
from sys import argv, stderr

def synchonize_name(path):
	video_formats = ["mkv$", "avi$", "mp4$"]
	video_pattern = re.compile("|".join(video_formats))
	videos = [path + '/' + video for video in os.listdir(path) if  video_pattern.search(video)]

	sub_pattern = re.compile("(smi|srt)$")
	subs = [path + '/' + sub for sub in os.listdir(path) if sub_pattern.search(sub)]
	for video, sub in zip(videos, subs):
		new_sub = video.replace(".mkv", ".smi")
		os.rename(sub, new_sub)
		print(new_sub)


if __name__ == "__main__":
	try:
		synchonize_name(argv[1])
	except IndexError:
		print("Usage: {} <path>".format(argv[0]))
