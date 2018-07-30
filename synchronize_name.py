#!/usr/bin/python3

import os
from sys import argv

def synchonize_name(path):
	videos = [path + '/' + video for video in os.listdir(path) if video.find(".mkv") != -1]
	subs = [path + '/' + sub for sub in os.listdir(path) if sub.find(".smi") != -1]

	for video, sub in zip(videos, subs):
		new_sub = video.replace(".mkv", ".smi")
		os.rename(sub, new_sub)
		print(new_sub)
