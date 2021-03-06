#!/usr/bin/python
#JoshAshby 2011
#joshuaashby@joshashby.com
#http://joshashby.com

"""
Import all of the libraries we need.
sys is needed for the system arguments
bluetooth is for communicating with the phone which acts as a barcode scanner
virtkey is for emulating keyboard key presses to type the barcode data
"""
import bluetooth
import sys
import virtkey

"""
sock is the socket for the bluetooth connection, all bluetooth functions happen through sock
v is the object for virtual keys (the keyboard emulation)
"""
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
v = virtkey.virtkey()

"""
returns: host in the format of xx:xx:xx:xx:xx:xx
takes: nothing
"""
def find_host():
	for host, name in bluetooth.discover_devices(lookup_names=True):
		print host, name
		#if (name == 'Nexus 10' or host == 'BC:20:A4:74:7E:43'):
		if (host == "04:E4:51:11:19:09"):
			print "name: ", name
			return host

"""
returns: port number of SL4A, needed for connecting with the phone's python script inorder to get and pass data between the phone and computer
takes: host number in the format of xx:xx:xx:xx:xx:xx
finds which port everything, including the needed SL4A port, is running on. Needed in order to connect to device
"""
def find_port(host):
	services = bluetooth.find_service(address=host)
	for service in services:
		print service
		if service['name'] == 'SL4A':
			print service
			port = service['port']
			print port
			return port

"""
returns: nothing
takes: nothing
connect to the bluetooth device
"""
def connect(host, port):
	sock.connect((host, port))
	print sock

"""
returns: 100bytes from bluetooth everytime it's called
takes: nothing
receive data from the bluetooth device
"""
def receive():
	return sock.recv(100)

"""
returns: nothing
takes: product_name, name of the product
send data to the bluetooth device
"""
def send(product_name):
	sock.send(product_name)

"""
returns: nothing
takes: nothing
take input from the bluetooth device
"""
def scan():
	while True:
		query = receive()
		print "received from client:", query
		for x in query:
			v.press_unicode(ord(x))
			v.release_unicode(ord(x))

host = find_host()
print host
if (host == 'None'):
	host = find_host()
print host
port = find_port(host)
print port
connect(host,port)
scan()
