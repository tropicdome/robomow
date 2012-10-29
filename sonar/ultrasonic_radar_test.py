#!/usr/bin/env python
import serial
import sys, time
from threading import Thread
import numpy as np
import matplotlib.cm as cm
from matplotlib.pyplot import figure, show, rc
import matplotlib.pyplot as P
from pylab import *
import Image
import cv

###########################################################

def PILtoCV_4Channel(PIL_img):
	cv_img = cv.CreateImageHeader(PIL_img.size, cv.IPL_DEPTH_8U, 4)
	cv.SetData(cv_img, PIL_img.tostring())
	return cv_img

###########################################################

def fig2img ( fig ):
	# put the figure pixmap into a numpy array
	buf = fig2data ( fig )
	w, h, d = buf.shape
	fig_return = Image.fromstring( "RGBA", ( w ,h ), buf.tostring( ) )
	buf = 0
	return fig_return

###########################################################

def fig2data ( fig ):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw ( )
 
    # Get the RGBA buffer from the figure
    w,h = fig.canvas.get_width_height()
    buf = np.fromstring ( fig.canvas.tostring_argb(), dtype=np.uint8 )
    buf.shape = ( w, h,4 )
 
    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll ( buf, 3, axis = 2 )
    return buf
###########################################################

def sonar_graph(ping_reading):

	# force square figure and square axes looks better for polar, IMO
	fig = figure(figsize=(6,6))
	#ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
	ax = P.subplot(1, 1, 1, projection='polar')
	#ax = fig.add_subplot(2, 2, 2, projection='radar')
	P.rgrids([28, 61, 91])
 	#circle = P.Circle((0, 0), 50)
	#ax.add_artist(circle)	

	ax.set_theta_zero_location('N')
	ax.set_theta_direction(-1)
	x = 1
	theta = 0
	angle = theta * np.pi / 180.0
	radii = [ping_reading]
	width = .15
	bars1 = ax.bar(0, 100, width=0.001, bottom=0.0)
	print "theta, radii, width: ", theta, radii, width
	bars = ax.bar(angle, radii, width=width, bottom=0.0, color='blue')
	
	#for r,bar in zip(radii, bars):
#	bar.set_facecolor( cm.jet(r/10.))
#		bar.set_alpha(1)

	pil_img = fig2img(fig)
	#pil_img.show()

	#print type(pil_img), pil_img
	sonar_image = PILtoCV_4Channel(pil_img)
	#print type(ax)
	#print type(fig)
	#print type(pil_img)
	#print type(sonar_image)

	cv.ShowImage("Sonar", sonar_image )
	#cv.MoveWindow ('Sonar',50 ,50 )
	time.sleep(.01)
	cv.WaitKey(1)
	#print "finished graph"
	
	#garbage cleanup
	fig.clf()
	P.close()
	return sonar_image

def sonar_reading():

	PORT = "/dev/ttyUSB1"
	try:
		ser = serial.Serial(PORT, 9600, timeout=1)
		s = ser.readline()
		print "recieved from arduino: ", s
	except:
		print sys.exc_info()[0]
		s = 0
	#time.sleep(.1)

	#if len(s) < 1: break
	#if ser.isOpen():
	#    print "Connected..."try
	#ser.close()             # close port
	if ser.isOpen():
	#	print "Not Connected..."
		ser.close()             # close port
	try:
		reading_to_return = int(s)
	except:
		reading_to_return = 0
	if reading_to_return > 300: s = 300
	if reading_to_return < 0: s = 0

	return reading_to_return


def sonar_display():
	while 1:
		s1 = sonar_reading()
		sonar_graph(s1)
		time.sleep(.05)

t = Thread(target=sonar_display)
t.start()


#for i in range(10):
#	print i
#	time.sleep(1)
