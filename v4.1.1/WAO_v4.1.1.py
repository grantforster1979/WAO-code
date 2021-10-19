# WAO_v4.1
# Python 3 code to generate .nc files for instruments based at WAO
# No input arguments required
# System looks to see where it is running from  
# Config.txt file is assumed to be in the root directory along with the source code  
# Data files placed in directory \data - this is platform independent
# Write to a log file as well to screen
# config[0] = vocabulary version
# config[1] = duration of file
# config[2] = start time (epoch)
# config[3] = instrument name
# config[4] = data product
# config[5] = full path to data file
#
# b.brooks 06/2021

import os
from os import path
from datetime import datetime
import WAO_parser as td


# change working directory to the directory where the code is being run from 
try:
    os.chdir(os.path.dirname(__file__))
    print("Current Working directory: ", os.getcwd())
except:
    print("Already in correct directory") 

# create log file new one per day
today = datetime.utcnow().strftime('%Y-%m-%d')
logfile = os.path.join(today + '.log')
g = open(logfile, 'a')
g.close()

# check for Data directory
try:
    dirName = 'Data'
    os.mkdir(dirName)
    print("Directory " , dirName ,  " created ") 
    g = open(logfile, 'a')
    g.write(datetime.utcnow().isoformat() + ' Data directory created.\n')
    g.close()
except FileExistsError:
    print("Directory " , dirName ,  " already exists")
    g = open(logfile, 'a')
    g.write(datetime.utcnow().isoformat() + ' Data directory already exists.\n')
    g.close()
   
# check for config file
try:
    path.exists("config.txt")
    print("Config.txt file detected")
    g = open(logfile, 'a')
    g.write(datetime.utcnow().isoformat() + ' Config.txt file detected.\n')
    g.close()    
except FileExistsError:
    print("Config.txt file missing. Program will terminate.")
    g = open(logfile, 'a')
    g.write(datetime.utcnow().isoformat() + 'Config.txt file missing. Program terminated.\n')
    g.close()
    exit()
    
# check for meta
try:
    path.exists("meta.xlsx")
    print("meta.xlsx file detected")   
    g = open(logfile, 'a')
    g.write(datetime.utcnow().isoformat() + ' meta.xlsx file detected.\n')
    g.close()     
except FileExistsError:
    print("meta.xlsx file missing. Program will terminate.")
    g = open(logfile, 'a')
    g.write(datetime.utcnow().isoformat() + ' meta.xlsx file missing. Program will terminate.\n')
    g.close() 
    exit()
    
td.t_control(logfile)    