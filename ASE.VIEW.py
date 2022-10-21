#!/usr/bin/python3
from ase.io import read, write
from ase.io.gaussian import write_gaussian_in, read_gaussian_out,read_gaussian_in
from ase.calculators.gaussian import Gaussian
from ase.visualize import view
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

print(file_path[-3:])
if file_path[-3:]=="log":
	Glog = read_gaussian_out(fd)
elif (file_path[-3:]=="com") or (file_path[-3]=="gjf"):
	Glog=read_gaussian_in(fd)

fd.close()

view(Glog)
