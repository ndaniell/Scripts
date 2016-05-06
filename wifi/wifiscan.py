#!/usr/bin/python
import curses
import subprocess
import re
import time

cell_list = []

class Cell:
    def __init__(self):
        self.address = ""
        self.frequency = ""
        self.signal_level_dbm = ""
        self.quality = ""
        self.encryption = ""        
        self.essid = ""

def scan_wifi():
    global cell_list
    cell_list = []
    scan_output = subprocess.check_output('iwlist wlan0 scan', shell=True)
    cell_strings = scan_output.strip().split("Cell")
    for cell in cell_strings[1:]:
        newCell = Cell()
        newCell.address = re.search('Address:\s*(\S*)', cell).group(0).strip()
        newCell.frequency = re.search('Frequency:\s*(.*)', cell).group(0).strip()
        newCell.signal_level = re.search('Signal level=\s*(\S*)', cell).group(0).strip()
        newCell.quality = re.search('Quality=\s*(\S*)', cell).group(0).strip()
        newCell.address = re.search('Encryption key:\s*(\S*)', cell).group(0).strip()
        newCell.essid = re.search('ESSID:\s*(.*)', cell).group(0).strip()
        cell_list += [newCell]
                

w = curses.initscr()
try:
    while True:
        scan_wifi()
        w.erase()
        for cell in sorted(cell_list, key=lambda cell: cell.signal_level):
            w.addstr("%s: %s\n" % (cell.essid, cell.signal_level))
        w.refresh()
        time.sleep(3)
finally:
    curses.endwin()

