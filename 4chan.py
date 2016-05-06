import urllib2
import urllib
import re
import os.path
import threading
import time

keywords = []

max_thread_count = 5
thread_join_timeout = 3.0

file_types = ["webm", "jpg", "gif", "png"]

def fetch_thread_list(board_name):
	thread_list = []
	page_count = range(2, 10)
	for page in page_count:
		url = "http://boards.4chan.org/%s" % board_name
		if page != 0:	
			url += "/%d" % page
		board_source = urllib2.urlopen(url).read()
		for x in re.findall(r"href=\"(.*?)\"", board_source):
			search_thread_start_string = "thread/"
			thread_start = x.find(search_thread_start_string)
			if (thread_start != -1):
				canidate_thread = x[thread_start+len(search_thread_start_string):]
				hash_index = canidate_thread.rfind("#")
				slash_index = canidate_thread.rfind("/")
				if(hash_index == -1 and slash_index == -1):
					thread_list += [canidate_thread]
	return set(thread_list)

def keyword_search(source):
	keyword_found = False
	if(len(keywords) <= 0):
		keyword_found = True
	else:	
		for x in re.findall(r">(.*?)<", source):
			for keyword in keywords:
				if (re.search(r"\b%s\b" % keyword, x) != None):
					print ("Keyword found: %s" % x)
					keyword_found = True
					break
	return keyword_found

def fetch_thread(board_name, thread_id):
	thread_source = urllib2.urlopen("http://boards.4chan.org/%s/thread/%s" % (board_name, thread_id)).read()
	if(keyword_search(thread_source)):
		directory = os.path.join(board_name, thread_id)
		if not os.path.exists(directory):
			os.makedirs(directory)
		for x in re.findall(r"href=\"(.*?)\"", thread_source):
			url = "http:"+x
			file_name = os.path.join(directory, x.split("/")[-1])
			for file_type in file_types:
				if (x.find("."+file_type) != -1):
					if(os.path.isfile(file_name) == False):
						print "%s:%s:%s" % (board_name, thread_id, file_name)
						urllib.urlretrieve(url, file_name)

def main(board):
	while True:
		running_thread_count = 0
		thread_list = fetch_thread_list(board)
		thread_count = 0
		running_threads = []
		for thread_id in thread_list:
			thread_count+=1
			print "Fetching %d of %d" %(thread_count, len(thread_list))
			thread = threading.Thread(target=fetch_thread, args=(board, thread_id))
			thread.start()
			running_threads += [thread]
			if(len(running_threads) >= max_thread_count):
				print "Max threads running"
				while len(running_threads) >= max_thread_count:
					for current_running_thread in running_threads:
						current_running_thread.join(thread_join_timeout)
						if(not current_running_thread.is_alive()):
							print "Thread finished"
							running_threads.remove(current_running_thread)
				print "Spawning More threads"
				

main("s")
