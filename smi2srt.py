#!/usr/bin/python3
from sys import argv, stderr
import re
import argparse
import os

_debug=False


def isUTF8(filename: str):
	with open(argv[1], "rb") as f:
		data = f.read()
	try:
		data.decode('UTF-8')
	except UnicodeDecodeError:
		return False
	else:
		return True

class SMI:
	def __init__(self, filename):
		self.filename = filename
		with open(filename, encoding="utf-8" if isUTF8(filename) else "euc-kr", errors="ignore") as f:
			self.lines = f.readlines()
		return

	def parse(self):
		'''
		return a list of (begin_frame, end_frame, speech)
		frame unit: ms
		'''

		ret = []
		idx = 0
		while True:
			try:
				begin_idx, begin_frame = self.find_sync(idx)
				end_idx, end_frame = self.find_sync(begin_idx + 1)
			except EOFError:
				break
			speech = [line for line in (
				self.get_pure_speech(line) for line in self.lines[begin_idx:end_idx]) if line]

			if speech:
				data = (begin_frame, end_frame, '\n'.join(speech))
				ret.append(data)
				if _debug:
					print(data)

			idx = end_idx

		return ret



	def get_pure_speech(self, line: str):
		useless_pattern = re.compile(r"(<.*?>)|(&nbsp;)|(\n)")
		return useless_pattern.sub("", line)

	def find_sync(self, start_from):
		''' return (index, frame)'''
		start_pattern = re.compile(r"(?<=<SYNC Start=)\d+(?=>)")
		size = len(self.lines)
		for i in range(start_from, size):
			result = start_pattern.search(self.lines[i])
			if result:
				if _debug:
					print(i, result.group())
				return i, int(result.group())
		raise EOFError
	#end of SMI

class SRT:
	def __init__(self, data_from_SMI, delay=0):
		self.data = data_from_SMI
		self.delay=delay
		return

	def write(self, filename: str):
		if filename.find("smi") != -1:
			filename = filename.replace(".smi", ".srt")
		elif filename.find(".srt") != -1:
			pass
		else:
			filename += ".srt"


		with open(filename, "w+", encoding="utf-8") as f:
			for cnt, b_frame, e_frame, speech in ((i, *tpl) for i, tpl in enumerate(self.data, 1)):
				payload = "".join([str(cnt), '\n', 
				self.frame_to_time(b_frame) , " --> " , self.frame_to_time(e_frame), '\n',  
				speech, '\n\n'])
				f.write(payload)

		return

	def frame_to_time(self, frame: int):
		def to_formatted(t: float):
			hour = int(t // 3600)
			t %= 3600

			minute = int(t // 60)
			t %= 60

			sec = int(t)
			milisec = round(1000 * (t - sec))
			ret = "{:02d}:{:02d}:{:02d},{:03d}".format(hour, minute, sec, milisec)
			if _debug:
				print(ret)
			return ret

		time_in_sec = (frame / 1000) + self.delay
		return to_formatted(time_in_sec)


if __name__ == "__main__":
	if len(argv) == 1:
		print("Usage: {} [-delay <sec> -clean] smi_files...".format(argv[0]), file=stderr)

	if argv.count("-delay"):
		i = argv.index("-delay") + 1
		delay = float(argv[i])
		argv.pop(i)
		argv.remove("-delay")
	else:
		delay = 0

	if argv.count("-clean"):
		erase_original = True 
		argv.remove("-clean")
	else:
		erase_original = False

	for subtitle in argv[1:]:
		ret = SMI(subtitle).parse()
		SRT(ret, delay).write(subtitle)
		print(subtitle)

	for subtitle in argv[1:]:
		os.remove(subtitle)