#!/usr/bin/python
import curses
import subprocess
import re
import time

cell_list = []
cell_history = {}
graph_resolution = 10

w = curses.initscr()

class Cell:
    def __init__(self):
        self.address = ""
        self.frequency = ""
        self.signal_level_dbm = ""
        self.quality = ""
        self.encryption = ""        
        self.essid = ""

def scan_wifi():
    global cell_list, cell_history
    cell_list = []
    scan_output = subprocess.check_output('iwlist wlan0 scan', shell=True)
    cell_strings = scan_output.strip().split("Cell")
    for cell in cell_strings[1:]:
        newCell = Cell()
        newCell.address = re.search('Address:\s*(\S*)', cell).group(1).strip()
        newCell.frequency = re.search('Frequency:\s*(.*)', cell).group(1).strip()
        newCell.signal_level = re.search('Signal level=\s*(\S*)', cell).group(1).strip()
        newCell.quality = re.search('Quality=\s*(\S*)', cell).group(1).strip()
        newCell.encryption = re.search('Encryption key:\s*(\S*)', cell).group(1).strip()
        newCell.essid = re.search('ESSID:\s*(.*)', cell).group(1).strip()
        cell_list += [newCell]
	try:
	    cell_history[newCell.essid + "(" + newCell.address + ")"] += [newCell.signal_level]
	except KeyError:		
	    cell_history[newCell.essid + "(" + newCell.address + ")"] = [newCell.signal_level]

def graph_signal(essid_address):
    for print_signal_level in range(graph_resolution, 0, -1):
        for signal_level in cell_history[essid_address]:
		    signal_level_ratio = ((90.0 - (abs(float(signal_level)) - 10.0))/90.0)		
		    if (int(signal_level_ratio * graph_resolution)) >= print_signal_level:					  
		       w.addstr("X")
		    else:
		       w.addstr("")	
        w.addstr("\n")


try:
    while True:
        scan_wifi()
        w.erase()
        try:	
            for cell in sorted(cell_list, key=lambda cell: cell.signal_level):
                w.addstr("%s(%s): %s\n" % (cell.essid, cell.address, cell.signal_level))
                graph_signal(cell.essid + "(" + cell.address + ")")
        except curses.error:
            pass
        w.refresh()
        time.sleep(3)
finally:
    curses.endwin()

