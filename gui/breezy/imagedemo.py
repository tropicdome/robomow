"""
File: imagedemo.py
Author: Kenneth A. Lambert
"""
#!/usr/bin/env python
import sys
sys.path.append( "../../lib/" )
import time
import mobot_video_consume
from img_processing_tools import *
import Image, ImageTk

from breezypythongui import EasyFrame
from Tkinter import PhotoImage
#from tkFont.Font import Font

class ImageDemo(EasyFrame):
	"""Displays an image and a caption."""

	def __init__(self):
		"""Sets up the window and widgets."""
		EasyFrame.__init__(self, title = "Image Demo")
		self.setResizable(False)
		self.imageLabel = self.addLabel(text = "",
					               row = 0, column = 0,
					               sticky = "NSEW")
		textLabel = self.addLabel(text = "Smokey the cat",
					              row = 1, column = 0,
					              sticky = "NSEW")
		

		#self.update_display()
		# Set the font and color of the caption.
		#font = Font(family = "Verdana", size = 20, slant = "italic")
		#textLabel["font"] = font
		textLabel["foreground"] = "blue"
		
	def update_display(self):
		# Load the image and associate it with the image label.
		# Load the image and associate it with the image label.
		self.image = PhotoImage(file = "smokey.gif")
		imageLabel["image"] = self.image
		#self.image = PhotoImage(self.frame)
		#camera = mobot_video_consume.consume_video('video.0', 'localhost')
		#while True:
		#time.sleep(0.01)
		#print camera.frame
		#cv2.imshow('Video', camera.frame)
		#cv.WaitKey(10)
		#self.frame = ImageTk.PhotoImage(array2image(camera.frame))
		#img = Image.open(camera.frame)	
		#self.imageLabel["image"] = self.frame
		print "hi", self.frame
		#self.imageLabel.pack()
		#self.imageLabel.config(image=self.frame)
		#self.main_gui.after(100, update_display)
		self.after(5, self.update_display)

if __name__ == "__main__":

	ImageDemo().mainloop()
