#!/usr/bin/python3
import ase, ase.neb, ase.io
import ase.build
from ase.calculators.gaussian import Gaussian
from ase.io.gaussian import write_gaussian_in
from ase.io.gaussian import read_gaussian_in
from ase.io.trajectory import Trajectory
from ase.optimize import FIRE
from copy import deepcopy
from ase.visualize import view
from ase.io.animation import write_gif
import os
from os import path
import sys
import glob

# Colors, for fancy user's
class bcolors():
    Black= "\u001b[30;1m"
    Red= "\u001b[31;1m"
    Green= "\u001b[32;1m"
    Yellow= "\u001b[33;1m"
    Blue= "\u001b[34;1m"
    Magenta= "\u001b[35;1m"
    Cyan= "\u001b[36;1m"
    White= "\u001b[37;1m"
    END="\u001b[0m"

# Obtain path and file in the format:
#       name.initial
#       name.final

dir_path = os.getcwd()

# If there are more than one file in the files[list] of files it read and makes you choose which of them you want
def choose(files,string_name):
    if len(files)<1:
        sys.exit(bcolors.Red+ "There no "+string_name+" file in the "+dir_path+ bcolors.END)
    elif(len(files)>1):
        print(bcolors.Yellow+"There are many "+string_name+" files in this directory")
        print("     Chosse one of the by index"+bcolors.END)
        count = 0
        for i in files:
            print(i+"       "+bcolors.Yellow+str(count)+bcolors.END)
            count+=1
        count = input("Now choose your file : "+bcolors.Yellow)
        print(bcolors.END)
        files=files[int(count)]
    else:
        files=files[0]
    return files

# Function decined to correct glob library list
def correct_argv(file,dir_path):
    if file.startswith("./"):
        file = file[1:]
    elif not file.startswith("/"):
        file="/"+file
    return dir_path+file

# Check initial and final files 
#   First check if the files are given as arguments to the scripts
#       True: use .initial and .final to identify the files
if (len(sys.argv) < 3):
    dir_path = os.getcwd()
    initial_file = glob.glob(dir_path+"/*.initial")
    final_file = glob.glob(dir_path+"/*.final")
    initial_file = choose(initial_file,"initial")
    final_file = choose(final_file,"final")
else:    
    initial_file =str(sys.argv[1])
    final_file =str(sys.argv[2])
    initial_file = correct_argv(initial_file,dir_path)
    final_file = correct_argv(final_file,dir_path)
if not (path.exists(initial_file) and path.exists(final_file)):
    print(bcolors.Red +"The file "+ log_path + " does not exist"+bcolors.END)
    quit()

# Obtaining the name of the initial file, this will be used to give name to the other files
initial_name = (initial_file.split("/")[-1]).split(".")[0]

initial = open(initial_file)
final = open(final_file)
initial = read_gaussian_in(initial,True)
final = read_gaussian_in(final,True)

# Copy parameters line
tem=open(initial_file)
for line in tem:
    if line.startswith("#"):
        PARAMETER_INITIAL=line
tem.close()
print(PARAMETER_INITIAL)

def Gcheck_parameters(atom_obj1,atom_obj2):
    if not (atom_obj1.calc.parameters==atom_obj2.calc.parameters):
        print(bcolors.Red+"    WARNING:"+bcolors.END)
        print(" Parameters do not coincide between initial and final files")
        print("   Value              Initial              Final")
        print("--------------------------------------------------")
        keys = list(atom_obj2.calc.parameters.keys())
        val1 = list((atom_obj1.calc.parameters).values())
        val2 = list((atom_obj2.calc.parameters).values())
        keys[3]="method"
        keys[4]="basis"
        for i in range(len(val1)):
            if not (val1[i]==None and
                val2[i]==None):
                if not (val1[i]==val2[i]):
                    print("  "+ str(keys[i])+
                        "       "+bcolors.Red+str(val1[i])
                        +"       " + str(val2[i])+bcolors.END)
                else:
                    print("  "+ str(keys[i])+
                        "       "+str(val1[i])
                        +"       " + str(val2[i]))


Gcheck_parameters(initial,final)

# we copy the initial and final into a save object
write_initial = initial 
write_final = final

#           Interpolate process

Nimages = int(input(bcolors.Green+"Choose the number of images: \n  "+bcolors.END))


# function to copy intial parameters 
def WGwrite(fd,atom_obj, atom_obj_params):
    keys = list(atom_obj_params.calc.parameters.keys())
    val = list((atom_obj_params.calc.parameters).values())
    if not( "method" in keys):
        _method=keys[5]
    else:
        _method=atom_obj_params.calc.parameters["method"]
    if not("basis" in keys):
        _basis=keys[6]
    else:
        _basis=atom_obj_params.calc.parameters["basis"]
    params={'nprocshared':8}
    write_gaussian_in(fd, #input file name to write
                    atoms=atom_obj, #atoms object
                    chk=atom_obj_params.calc.parameters["chk"],
                    mem=atom_obj_params.calc.parameters["mem"],
                    method=_method,
                    basis=_basis,
                    output_type=atom_obj_params.calc.parameters["output_type"],
                    mult=atom_obj_params.calc.parameters["mult"],
                    charge=atom_obj_params.calc.parameters["charge"],
                    nprocshared=8
                    )


################ NEB process
try:
    #  copy initial to the list of images
    images = []
    images = [initial]
    for i in range(Nimages):
        image = initial.copy()
        images.append(image)
    images.append(final)

    neb = ase.neb.NEB(images, climb=False, k=0.5)
except ValueError as err:
    print(bcolors.Red)
    print(err)
    print(bcolors.END)
    quit()

    neb = ase.neb.NEB(images, climb=False, k=0.4)
#    print(images)


neb.interpolate('idpp',apply_constraint=True)
print("NEB done")

os.system('mkdir 00')
fd = open(dir_path+"/00/"+initial_name+"0.com","+w")
WGwrite(fd,initial,write_initial)



for i in range(1,Nimages+2):
    os.system("mkdir 0"+str(i))
    fd = open("./0"+str(i)+"/"+initial_name+str(i)+".com","+w")
    WGwrite(fd,images[i],write_initial)

# Editing files to give the same parameters as the initial file
for i in range(0,Nimages+2):
    file = open("./0"+str(i)+"/"+initial_name+str(i)+".com","r")
    text=""
    for line in file:
        if line.startswith("#"):
            text=text + PARAMETER_INITIAL
        else:
            text=text + line
    file.close()
    file = open("./0"+str(i)+"/"+initial_name+str(i)+".com","w")
    file.write(text)
    file.close()


write_gif(initial_name+".gif", images, interval=100, save_count=200)
view(images)