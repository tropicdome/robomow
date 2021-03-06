import  glob
import  os
import  re

import usb.core


#lsusb to find vendorID and productID:
#Bus 002 Device 005: ID 067b:2303 Prolific Technology, Inc. PL2303 Serial Port
# then call print find_usb_tty("067b","2303")
def find_usb_tty(vendor_id = None, product_id = None) :
    tty_devs    = []
    vendor_id = int(vendor_id, 16)
    product_id = int(product_id , 16)
    #print "vendor_id, product_id", vendor_id, product_id
    for dn in glob.glob('/sys/bus/usb/devices/*') :
        try     :
            vid = int(open(os.path.join(dn, "idVendor" )).read().strip(), 16)
            pid = int(open(os.path.join(dn, "idProduct")).read().strip(), 16)
            #print vid, pid
            if  ((vendor_id is None) or (vid == vendor_id)) and ((product_id is None) or (pid == product_id)) :
                dns = glob.glob(os.path.join(dn, os.path.basename(dn) + "*"))
                for sdn in dns :
                    for fn in glob.glob(os.path.join(sdn, "*")) :
                        print fn
                        if  re.search(r"\/ttyUSB[0-9]+$", fn) :
                            tty_devs.append(os.path.join("/dev", os.path.basename(fn)))
                        if  re.search(r"\/video[0-9]+$", fn) :
                            tty_devs.append(os.path.join("/dev", os.path.basename(fn)))
                        if  re.search(r"\/ttyACM[0-9]+$", fn) :
                            #tty_devs.append("/dev" + os.path.basename(fn))
                            tty_devs.append(os.path.join("/dev", os.path.basename(fn)))
                        pass
                    pass
                pass
            pass
        except ( ValueError, TypeError, AttributeError, OSError, IOError ) :
            pass
        pass

    return tty_devs

'''
import os
from os.path import join

def find_tty_usb(idVendor, idProduct):
    """find_tty_usb('067b', '2302') -> '/dev/ttyUSB0'"""
    # Note: if searching for a lot of pairs, it would be much faster to search
    # for the enitre lot at once instead of going over all the usb devices
    # each time.
    for dnbase in os.listdir('/sys/bus/usb/devices'):
        dn = join('/sys/bus/usb/devices', dnbase)
        if not os.path.exists(join(dn, 'idVendor')):
            continue
        idv = open(join(dn, 'idVendor')).read().strip()
        if idv != idVendor:
            continue
        idp = open(join(dn, 'idProduct')).read().strip()
        if idp != idProduct:
            continue
        #print dnbase, dn #, idv, idp
        for subdir in os.listdir(dn):
            print subdir
            if subdir.startswith(dnbase+':'):
                for subsubdir in os.listdir(join(dn, subdir)):
                    if subsubdir.startswith('video'):
                        
                        return join('/dev', subsubdir)

'''
if __name__== "__main__":
	print find_usb_tty('10c4','ea60' )
	#dev = usb.core.find(idVendor=0x2341, idProduct=0x0043)

	import usb.core
	import usb.util
	import sys

	# find our device
	dev = usb.core.find(idVendor='10c4', idProduct='ea60')

	# was it found?
	if dev is None:
		raise ValueError('Device not found')
	for cfg in dev:
		sys.stdout.write(str(cfg.bConfigurationValue) + '\n')
	for intf in cfg:
		sys.stdout.write('\t' +	str(intf.bInterfaceNumber) +',' + str(intf.bAlternateSetting) + '\n')
	for ep in intf:
		sys.stdout.write('\t\t' + str(ep.bEndpointAddress) +'\n')


	'''
	# set the active configuration. With no arguments, the first
	# configuration will be the active one
	dev.set_configuration()

	# get an endpoint instance
	cfg = dev.get_active_configuration()
	interface_number = cfg[(0,0)].bInterfaceNumber
	alternate_settting = usb.control.get_interface(interface_number)
	intf = usb.util.find_descriptor(
		 cfg, bInterfaceNumber = interface_number,
		 bAlternateSetting = alternate_setting
	)

	ep = usb.util.find_descriptor(
		 intf,
		 # match the first OUT endpoint
		 custom_match = \
		 lambda e: \
		     usb.util.endpoint_direction(e.bEndpointAddress) == \
		     usb.util.ENDPOINT_OUT
	)

	assert ep is not None

	# write the data
	ep.write('test')
	'''
