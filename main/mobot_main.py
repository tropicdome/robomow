#!/usr/bin/python

from PIL import Image, ImageTk
import time
from datetime import datetime
import socket 
import cv2
from threading import *
import sys
from maxsonar_class import *
import random
from robomow_motor_class_arduino import *
from gps_functions import *
from math import *

hhh = 0
file_lock = False


def snap_shot(filename):
	#capture from camera at location 0
	now = time.time()
	global webcam1
	try:
		#have to capture a few frames as it buffers a few frames..
		for i in range (5):
			ret, img = webcam1.read()		 
		#print "time to capture 5 frames:", (time.time()) - now
		cv2.imwrite(filename, img)
		img1 = Image.open(filename)
		img1.thumbnail((320,240))
		img1.save(filename)
		#print (time.time()) - now
	except:
		print "could not grab webcam"
	return 

def send_file(host, cport, mport, filetosend):
	#global file_lock
	file_lock = True
	#print "file_lock", file_lock
	try:       
		cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cs.connect((host, cport))
		cs.send("SEND " + filetosend)
		print "sending file", filetosend
		cs.close()
	except:
		#print "cs failed"
		pass
	time.sleep(0.1)
	try:
		ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ms.connect((host, mport))
		f = open(filetosend, "rb")
		data = f.read()
		f.close()
		ms.send(data)
		ms.close()
	except:
		#print "ms failed"
		pass
	#file_lock = False
	#print "file_lock", file_lock
		
		
'''
def send_data(host="u1204vm.local", cport=9091, mport=9090, datatosend=""):
	try:       
		cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cs.connect((host, cport))
		cs.send("SEND " + filetosend)
		cs.close()
	except:
		pass
	time.sleep(0.05)
	try:
		ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ms.connect((host, mport))
		f = open(filetosend, "rb")
		data = f.read()
		f.close()
		ms.send(data)
		ms.close()
	except:
		pass
'''	
class send_video(Thread):
	def __init__(self, filetosend):   
		self.filetosend = filetosend     
		Thread.__init__(self)

	def run(self):
			#global file_lock, hhh
			print self.filetosend
			while True:
				snap_shot(self.filetosend)	
				send_file(host="u1204vm.local", cport=9090, mport=9091,filetosend=self.filetosend)
				time.sleep(.01)
							
class send_sonar_data(Thread):
	def __init__(self, filetosend):   
		self.filetosend = filetosend
		self.sonar_data = "" 
		self.max_dist = -1
		self.min_dist = -1   
		self.min_sensor = -1
		self.max_sensor = -1 
		Thread.__init__(self)

	def run(self):
			#global file_lock, hhh
			sonar = MaxSonar()
			
			while True:
				self.sonar_data = ""
				self.max_dist = -1
				self.min_dist = -1 
				self.min_sensor = -1
				self.max_sensor = -1
				#
				#below 2 lines are for test purposes when actual US arent sending data
				#for i in range(1,6):
				#	sonar_data = sonar_data + "s"+str(i)+":"+ str(random.randint(28, 91))

				data = str(sonar.distances_cm())
				self.sonar_data = []
				sonar_data_str1 = ""
				try:
					if len(data) > 1:
						self.sonar_data.append(int(data[(data.find('s1:')+3):(data.find('s2:'))]))
						self.sonar_data.append(int(data[(data.find('s2:')+3):(data.find('s3:'))]))
						self.sonar_data.append(int(data[(data.find('s3:')+3):(data.find('s4:'))]))
						self.sonar_data.append(int(data[(data.find('s4:')+3):(data.find('s5:'))]))
						self.sonar_data.append(int(data[(data.find('s5:')+3):(len(data)-1)]))
						self.max_dist = max(self.sonar_data)
						self.min_dist = min(self.sonar_data)
						self.min_sensor = self.sonar_data.index(self.min_dist)
						self.max_sensor = self.sonar_data.index(self.max_dist)
						#sonar_data_str1 = "".join(str(x) for x in self.sonar_data)
						#print sonar_data_str1
						#print data
						f = open("sonar_data.txt", "w")
						f.write(data)
						f.close()
						send_file(host="u1204vm.local", cport=9092, mport=9093,filetosend=self.filetosend)
				except:
					pass
				time.sleep(.01)
			print "out of while in sonar"


def move_mobot(themove, speed):
	global motor
	if (themove == "f"):
		motor.forward(speed)
		#time.sleep(.01)
		#print motor.motor1_speed, motor.motor2_speed
	if (themove == "b"):
		motor.reverse(speed)
		#time.sleep(.01)
		#print motor.motor1_speed, motor.motor2_speed
	if (themove == "l"):
		motor.left(speed)
		#time.sleep(.01)
		#print motor.motor1_speed, motor.motor2_speed
	if (themove == "r"):
		motor.right(speed)
		#time.sleep(.01)
		#print motor.motor1_speed, motor.motor2_speed
	if (themove == "s"):
		motor.stop()
		#time.sleep(.01)
		#print motor.motor1_speed, motor.motor2_speed


def enable_video():
	video1 = send_video("snap_shot.jpg")
	video1.daemon=True
	video1.start()
	#video1.join()
	
def enable_sonar():
	sonar = send_sonar_data("sonar_data.txt")
	sonar.daemon=True
	sonar.start()
	#sonar.join()


def test_gps():
	#print "startup all gps"
	#start_all_gps()
	gpslist = gps_list()
	#print gpslist
	gps2 = mobot_gps()
	gps2.daemon=True
	gps2.start()
	#gps2.join()
	while 1:
		print "# of GPS Units:", len(gpslist)
		if (gps2.satellites > 0):
			print 'Satellites (total of', len(gps2.satellites) , ' in view)'
			print "Active satellites used:", gps2.active_satellites
			for i in gps2.satellites:
				print '\t', i
		print "lat: ", gps2.latitude
		print "long:", gps2.longitude
		time.sleep(random.randint(1, 3))	
		#os.system("clear")




if __name__== "__main__":
	testmode = False
	if len(sys.argv) > 1:
		if sys.argv[1] == 'testmode':
				print 'starting in testing mode'
				testmode= True
		
	#webcam1 = cv2.VideoCapture(0)
	#enable_video()
	#while 1:
	#	time.sleep(1)

	#test_gps()

	#move_mobot('f', 15)
	#time.sleep(5)
	#move_mobot('s', 0)
	sonar = None
	motor = None

	while True:
		current_move = ""
		now =  datetime.now()
		if sonar == None: # or len(sonar.sonar_data) < 1:
			sonar = send_sonar_data("sonar_data.txt")
			sonar.daemon=True
			sonar.start()
		if motor == None:
			motor = robomow_motor()
			print "motor.isConnected:", motor.isConnected
			time.sleep(2)

		if (sonar.max_dist > 0):
			move = ""
			print "......................"
			print "sonar_data: ", sonar.sonar_data
			print "max dist: ", sonar.max_dist, sonar.max_sensor
			print "min_dist: ", sonar.min_dist, sonar.min_sensor
			#if sonar.max_sensor == 0: move = "foward"
			#if sonar.max_sensor == 1: move = "right"
			#if sonar.max_sensor == 2: move = "reverse"
			#if sonar.max_sensor == 3: move = "left"
			
			threshold = 75
			#go foward until < 40 cm turn right
			if (sonar.sonar_data[0] > threshold): move = "f"
			if (sonar.sonar_data[1] > threshold): move = "f"
			if (sonar.sonar_data[0] < threshold) or (sonar.sonar_data[1] < threshold):
				if sonar.sonar_data[2] > sonar.sonar_data[3]: move = "r"
				else:
					move = "l"
			if (current_move != move) and (sonar.min_dist > 40):	
				print "moving mobot: ", move
				current_move = move
				#print "moving robot"
				if move == "f":
					move_mobot(move, 20)
					time.sleep(random.randint(50, 200)/100)
				else:
					move_mobot(move, 25)
					time.sleep(random.randint(50, 200)/100)
			if (sonar.min_dist < 40):
				move_mobot('b', 28)
				time.sleep(.4)
				move_mobot('r', 25)
				time.sleep(.65)
				
		#move_mobot('s', 0)
		#time.sleep(.2)
		print "sonar_data: ", sonar.sonar_data
		print "loop time:",  datetime.now() - now
	print "stopped"



'''
#############################################################
#start gps
#get current gps postiion
#get bearing to target position 
# turn toward target bearing
######################################################
gps1 = gps.gps(host="localhost", port="2947")
gps2 = gps.gps(host="localhost", port="2948")
gps3 = gps.gps(host="localhost", port="2949")
gps4 = gps.gps(host="localhost", port="2950")

'''

