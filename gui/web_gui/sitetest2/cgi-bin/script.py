#!/usr/bin/python
import sys
import time
import cgi, cgitb 
import os

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
#first_name = form.getvalue('first_name')
#last_name  = form.getvalue('last_name')
#button1 = form.getvalue('Submit1')

#time.sleep(1)
#os.system("./test_gui1.py")
time.sleep(1)

print 'Content-type: text/html\n'

if "Submit1" in form:
    	print "button 1 pressed"
elif "Submit2" in form:
    	print "button 2 pressed"
	time.sleep(1)
	os.system("./robomow_logic.py new_image")
else:
    print "Couldn't determine which button was pressed."
#time.sleep(1)

location = 'http://localhost:8004'

page = '''
<html>
<head>
<meta http-equiv="Refresh" content="1; URL='''+location+'''">
</head>
<body></body>
</html>'''

print page

