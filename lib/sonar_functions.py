#!/usr/bin/env python
import serial
import sys, time
from threading import Thread
import numpy as np
import matplotlib
matplotlib.use('agg')
from matplotlib.pyplot import figure, show, rc
import matplotlib.pyplot as P
from pylab import *
import Image
import cv
from maxsonar_class import *
import gc

###########################################################

def CVtoPIL_4Channel(CV_img):
	"""converts CV image to PIL image"""
	cv_img = cv.CreateMatHeader(cv.GetSize(img)[1], cv.GetSize(img)[0], cv.CV_8UC1)
	#cv.SetData(cv_img, pil_img.tostring())
	pil_img = Image.fromstring("L", cv.GetSize(img), img.tostring())
	return pil_img
###########################################################



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



def fig2img ( fig ):
    """
    @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
    @param fig a matplotlib figure
    @return a Python Imaging Library ( PIL ) image
    """
    # put the figure pixmap into a numpy array
    buf = fig2data ( fig )
    w, h, d = buf.shape
    return Image.fromstring( "RGBA", ( w ,h ), buf.tostring( ) )

###########################################################
def sonar_graph(ping_readings):
	#print "ping reading:", ping_readings
	#print type(ping_readings[1])
	# force square figure and square axes looks better for polar, IMO
	fig = figure(figsize=(3.8,3.8))
	ax = P.subplot(1, 1, 1, projection='polar')
	P.rgrids([28, 61, 91])
	ax.set_theta_zero_location('N')
	ax.set_theta_direction(-1)

	try:
		theta = 346
		angle = theta * np.pi / 180.0
		radii = [ping_readings[0]]
		width = .15
		bars1 = ax.bar(0, 100, width=0.001, bottom=0.0)
		#print "theta, radii, width: ", theta, radii, width
		bars = ax.bar(angle, radii, width=width, bottom=0.0, color='blue')
		theta = 6
		angle = theta * np.pi / 180.0
		radii = [ping_readings[1]]
		width = .15
		bars = ax.bar(angle, radii, width=width, bottom=0.0, color='blue')	
		theta = 86
		angle = theta * np.pi / 180.0
		radii = [ping_readings[2]]
		width = .15
		bars = ax.bar(angle, radii, width=width, bottom=0.0, color='blue')
		theta = 266
		angle = theta * np.pi / 180.0
		radii = [ping_readings[3]]
		width = .15
		bars = ax.bar(angle, radii, width=width, bottom=0.0, color='blue')
		img_to_return = fig2img(fig)
		P.close(fig)
		return img_to_return 
	except:
		print "Sonar data error... can't graph"
		pass
	#print "finshed graph"
	#pil_img = fig2img(fig)
	#sonar_image = pil_img
	#print type(pil_img), pil_img
	#sonar_image = PILtoCV_4Channel(pil_img)
	#cv.ShowImage("Sonar", sonar_image )
	#cv.MoveWindow ('Sonar',50 ,50 )
	#time.sleep(.01)
	#cv.WaitKey(10)
	#enable line below to make basestation work 12/13/2012
	#fig.savefig('sonar_image.png')

	#Image.open('sonar_image.png').save('sonar_image.jpg','JPEG')
	#print "finished saving"
	#stop
	#garbage cleanup
	#fig.clf()
	
	#gc.collect()
	#del fig
	P.close(fig)

def process_sonar_data(sonar_data):
	#global sensor1
	#data  = str(sensor1.distances_cm())
	data = sonar_data
	print "sonar data from inside sonar_functions", sonar_data
	if len(data) > 1:
		#print "data=", data
		#s1_data = re.search('s1', data)
		#print s1_data.span()
		s1_data = int(data[(data.find('s1:')+3):(data.find('s2:'))])
		s2_data = int(data[(data.find('s2:')+3):(data.find('s3:'))])
		s3_data = int(data[(data.find('s3:')+3):(data.find('s4:'))])
		s4_data = int(data[(data.find('s4:')+3):(data.find('s5:'))])
		s5_data = int(data[(data.find('s5:')+3):(len(data))])
		print s1_data, s2_data, s3_data, s4_data, s5_data 
		data2 = []
		data2.append(s1_data)
		data2.append(s2_data)
		data2.append(s3_data)
		data2.append(s4_data)
		data2.append(s5_data)
		#s1_data = int(s1_data)
		#if s1_data > 91: s1_data = 91
		#if s1_data < 0: s1_data = 0
		#print "s1:", s1_data
		#sonar_img = sonar_graph(data2)
		return data2
		#time.sleep(.01)



if __name__== "__main__":

	#t = Thread(target=sonar_display)
	#t.start()

	sensor1 = MaxSonar()
	time.sleep(1)
	sonar_display(sensor1)
	time.sleep(1)

	for i in range(1000):
		sonar_display(sensor1)
		time.sleep(0.01)

