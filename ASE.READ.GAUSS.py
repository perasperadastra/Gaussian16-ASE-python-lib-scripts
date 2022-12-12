#!/usr/bin/python3
from ase.io import read, write
from ase.io.gaussian import write_gaussian_in, read_gaussian_out
import sys
import os

actual_path=os.getcwd()
file = sys.argv[1]
if file.startswith("./"):
	file = file[1:]
elif not file.startswith("/"):
	file="/"+file

file_path=actual_path+file
fd = open(file_path,"r")
# For the  L3MoN2MoL3_TZVP.log file 
Glog = read_gaussian_out(fd)
fd.close()




fd=open("./gaussian.com","w")

write_gaussian_in(fd, #input file name to write
				atoms=Glog, #atoms object
				chk='MoN2MO7Dscan.chk',
				mem='1Gb',
				method="PBE1PBE", #
				basis="Def2SVP",
				output_type='P',
				mult=1,
				charge=0,
				nrpocshared=8)
