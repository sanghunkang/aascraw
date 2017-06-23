#!/usr/bin/python


def fetch_seq_from_file(fpath):
	with open(fpath, "r") as fr:
		seq_url = []

		line_read = "TRUE"
		while line_read.strip() != "":
			line_read = fr.readline()
			seq_url.append(line_read)	
		
	return seq_url

