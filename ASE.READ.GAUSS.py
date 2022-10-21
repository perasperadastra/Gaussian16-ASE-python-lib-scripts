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
#Gcell = Glog.get_cell()
# Test if cell is not defined
# if all index of the three vector of the cell are 0 it not set
#if Gcell == 0:
#	print(" no unit cell defined")
#	print("copuld be defined with set_cell(a,b,c,A,B,C")
# To obtain coordinate from and optimization (out)
#Gfinal_Coord = Glog.get_positions()

# To obtain initial charges
#Gcharge_0 = Glog.get_initial_charges()

# To obtain final charges (if avalible)
#Gcharge_1 = Glog.get_charges()

# In this example we will use the data obtained for the septuplete
# 	To build a scan where N2 dissociates


# se ha de crear un file-like opbject que es unh objieto tipico de python
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
