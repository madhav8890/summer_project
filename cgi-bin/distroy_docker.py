#!/usr/bin/python3

print("content-type: text/html\n")

import subprocess as sp
a=sp.getoutput("sudo Docker rm -f $(docker PS -q -a)")
print(a)
