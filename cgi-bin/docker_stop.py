#!/usr/bin/python3

print("content-type: text/html")
print()

import subprocess as sp
import cgi

form = cgi.getvalue()
cmd = form.FieldStorage("stop")

a=sp.getoutput("sudo docker stop \t " + cmd)
print(a)
