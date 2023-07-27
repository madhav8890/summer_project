#!/usr/bin/python3


print("content-type: text/html")
print()
import cgi
import subprocess



form = cgi.FieldStorage()
osname = form.getvalue("b")
osimage = form.getvalue("a")
cmd = "docker run -dit --name {0} {1}".format(osname, osimage)
a = subprocess.getoutput("sudo\t"  +  cmd)
print(a)












