import socket
import os
import sys
from datetime import datetime
import time

def hour(string):
	hour=float(string)
	minutes=int(hour*100)%100
	realhour=60*int(hour)+minutes
	return realhour

HOST = '127.0.0.1'
PORT = 50007
so = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
so.connect((HOST,PORT))
id = os.fork()
if id == 0:
	pid = os.fork()
	if pid == 0:
		while True:
        		data = so.recv(1024)
			if data and data[0] == 'b' :
        			if (data[1] == '1') or (data[1] == '2'):
                			os.system('run-parts Plugged')
        			elif data[1] == '0':
                			os.system('run-parts Unplugged')
	else:
		pid2 = os.fork()
		if pid2 == 0:
			while True:
				fd = os.open("Unplugged/Plug.log",os.O_RDONLY)
				list = []
				stop = False
				while True:
					buffer = ""
					while True:
						char = os.read(fd,1)
						if char == '\n':
							break
						if char == "":
							stop = True
							break
						buffer += char
					if stop:
						break
					list.append(hour(buffer))
				unplug = sum(list) / len(list)
				os.close(fd)
				now = datetime.now().hour*60 + datetime.now().minute	
				lasts = unplug - now + 1440 % 1440
				if lasts < 10:
					os.system("/opt/slapos/bin/slapgrid-supervisorctl /etc/opt/slapos/slapos.cfg stop all")
					time.sleep(660)
				else:
					time.sleep(300)
		else:
			print "deamon checking plug: "
			print pid
			print "\ndeamon foresighting unplugging"
			print pid2
			print "\n"
			os._exit(0)
else:
	os.wait()
	sys.exit(0)
