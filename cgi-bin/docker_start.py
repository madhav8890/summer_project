#!/usr/bin/python3

print("content-type: text/html")
print()

import subprocess as sp
import cgi

form = cgi.FieldStorage()
cmd = form.getvalue("start")

a=sp.getstatusoutput("sudo docker start {}".format(cmd))
print(a)

