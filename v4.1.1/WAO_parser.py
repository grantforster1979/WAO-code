# WAO_parser_v4.1
# python 3
# suit of functions to read in config, and meta files and to control the work flow
#
# b.brooks 06/2021

def read_meta(logfile, name):
   import pandas as pd
   import numpy as np
   from datetime import datetime
   import WAO_common as com
   
   # read in meta
   try:
      df = pd.read_excel("meta.xlsx")
   except:
      # exit if problem encountered
      print("Unable to open meta.xlsx. This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open meta.xlsx. Program will terminate.\n')
      g.close()
      exit()     
      
   # find the approprate line
   inst = df.loc[:, 'instrument\n':'instrument\n':1].values
   tp = df.columns
   header = np.array(tp[1:len(tp)])      
   for x in range (0, len(inst)):
      if (name in inst[x]):
         tp = df.loc[x,:].values  
         dd = np.array(tp[1:len(tp)])
         break
            
   meta = np.empty([len(header), 2], dtype=object)       
   if 'dd' not in locals():
      print("Can't find meta data about named instrument. This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Can\'t find meta data about named instrument. Program will terminate.\n')
      g.close()
      exit()
   else:
      for x in range (0, len(header)):
         meta[x, 0] = header[x]
         meta[x, 1] = dd[x]
   
   del pd, datetime, np    
   
   return meta

def read_config(logfile):
   from datetime import datetime
   import time
   import calendar   
   import numpy as np
   
   # read in Config file
   try:
      f = open("Config.txt", "r")
      if f.mode == 'r':
         lines = f.readlines()
         f.close()
   except:
      # exit if problem encountered
      print("Unable to open Config.txt file. This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open Config.txt. Program will terminate.\n')
      g.close()
      exit()
      
   config = np.empty([7, 1], dtype=object)
   # process information in config file
   ss1 = "##### Start - do not remove #####"
   for x in range (0, len(lines)):
      if (ss1 in lines[x]):
         try:
            config[0] = str(lines[x+1].strip('\n')).strip('[]') #file version
            config[1] = str(lines[x+2].strip('\n')) # desired duration in file
            config[2] = str(lines[x+3].strip('\n')) # start date all or d, m, y
            config[3] = str(lines[x+4].strip('\n')) # instrument name
            config[4] = str(lines[x+5].strip('\n')) # data product
            config[5] = str(lines[x+6].strip('\n')) # path to data  
            config[6] = str(lines[x+7].strip('\n')) # standard version          
            break  
         except:   
            print("Error in. This program will terminate.")
            g = open(logfile, 'a')
            g.write(datetime.utcnow().isoformat() + ' Error in config file. Program will terminate.\n')
            g.close()
            exit()
      
   del lines, datetime, np, time, calendar
   
   return config

def do_run(config, meta, data, logfile):
   import WAO_data as dat
   import WAO_products as prod
   
   data.lat = 52.9506
   data.lon = 1.1219
   opt = ''
   
   if (config[3] == 'ncas-ceilometer-2') and (config[4] == 'aerosol-backscatter'):
      opt = 'standard'
      data = dat.ncas_ceilometer_2(config, data, logfile) # this gets all the data in the file   
      data = dat.data_chunker(config, data, logfile) # this returns a data structure split into appropraite chuncks 
      try:
         for n in range(len(data.st)):
            data.counter = n # keeps track of where you are in the list (-1) 
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.aerosol_backscatter(meta, data, nc)
            nc.close() 
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.aerosol_backscatter(meta, data, nc) # counter will be -1
         nc.close()
   
   if (config[3] == 'ncas-ceilometer-2') and (config[4] == 'cloud-base'):
      opt = 'standard'
      data = dat.ncas_ceilometer_2(config, data, logfile) # this gets all the data in the file   
      data = dat.data_chunker(config, data, logfile) # this returns a data structure split into appropraite chuncks 
      try:
         for n in range(len(data.st)):
            data.counter = n # keeps track of where you are in the list (-1) 
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.cloud_base(meta, data, nc)
            nc.close() 
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.cloud_base(meta, data, nc) # counter will be -1
         nc.close()
         
   if (config[3] == 'ncas-co2-1') and (config[4] == 'co2-concentration'):
      data = dat.ncas_co2_1(config, data, logfile) # this gets all the data in the file   
      data = dat.data_chunker(config, data, logfile) # this returns a data structure split into appropraite chuncks 
      try:
         for n in range(len(data.st)):
            data.counter = n # keeps track of where you are in the list (-1) 
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.co2_concentration(meta, data, nc)
            nc.close() 
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.co2_concentration(meta, data, nc) # counter will be -1
         nc.close()

   if (config[3] == 'ncas-ftir-1') and (config[4] == 'ch4-n2o-co2-co-concentration'):
      data = dat.ncas_ftir_1(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try: 
         for n in range (len(data.st)):
            data.counter = n # keeps track of where you are in the list (-1)
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)  
            prod.ch4_n2o_co2_co_concentration(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)  
         prod.ch4_n2o_co2_co_concentration(meta, data, nc)
         nc.close()

   if (config[3] == 'ncas-ghg-gc-fid-1') and (config[4] == 'ch4-concentration'):
      data = dat.ncas_ghg_gc_fid_1(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.ch4_concentration(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile) 
         prod.ch4_concentration(meta, data, nc)
         nc.close()

   if (config[3] == 'ncas-ghg-gc-ecd-1') and (config[4] == 'n2o-sf6-concentration'):
      data = dat.ncas_ghg_gc_ecd_1(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.n2o_sf6_concentration(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile) 
         prod.n2o_sf6_concentration(meta, data, nc)
         nc.close()
            
   if (config[3] == 'ncas-ghg-gc-ecd-1') and (config[4] == 'sf6-concentration'):
      data = dat.ncas_ghg_gc_ecd_1(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.sf6_concentration(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile) 
         prod.sf6_concentration(meta, data, nc)
         nc.close()
      
   if (config[3] == 'ncas-o2-1') and (config[4] == 'o2n2-concentration-ratio'):
      data = dat.ncas_o2_1(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.o2n2_concentration_ratio(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.o2n2_concentration_ratio(meta, data, nc)
         nc.close()
      
   if (config[3] == 'ncas-rga3-1') and (config[4] == 'co-h2-concentration'):
      data = dat.ncas_rga3_1(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.co_h2_concentration(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.co_h2_concentration(meta, data, nc)
         nc.close()
         
   if (config[3] == 'ncas-rga3-1') and (config[4] == 'h2-concentration'):
      data = dat.ncas_rga3_1(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.h2_concentration(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.h2_concentration(meta, data, nc)
         nc.close()
      
   if (config[3] == 'uea-42i-nox-1') and (config[4] == 'nox-noxy-concentration'):
      data = dat.uea_42i_nox_1(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.nox_noxy_concentration(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.nox_noxy_concentration(meta, data, nc)
         nc.close()
   
   if (config[3] == 'uea-43i-so2-1') and (config[4] == 'so2-concentration'):
      data = dat.uea_43i_so2_1(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.so2_concentration(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.so2_concentration(meta, data, nc)
         nc.close()     
    
   if (config[3] == 'uea-49i-o3-1') and (config[4] == 'o3-concentration'):
      data = dat.uea_49i_o3_1(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.o3_concentration(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.o3_concentration(meta, data, nc)
         nc.close()    
         
   if (config[3] == 'uea-t200up-1') and (config[4] == 'nox-noxy-concentration'):
      data = dat.uea_t200up_1(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.nox_noxy_concentration(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.nox_noxy_concentration(meta, data, nc)
         nc.close()
         
   if (config[3] == 'uea-t200up-2') and (config[4] == 'nox-noxy-concentration'):
      data = dat.uea_t200up_2(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.nox_noxy_concentration(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.nox_noxy_concentration(meta, data, nc)
         nc.close()
      
   if (config[3] == 'uea-aws-1') and (config[4] == 'surface-met'):
      #campbell radiation only
      opt = '10m'
      data = dat.uea_aws_1and2(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.surface_met1(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.surface_met1(meta, data, nc)
         nc.close()
   
   if (config[3] == 'uea-aws-2') and (config[4] == 'surface-met'):
      # Gill no radiation
      opt = '10m'
      data = dat.uea_aws_1and2(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.surface_met2(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.surface_met2(meta, data, nc)
         nc.close()   
      
   if (config[3] == 'uea-caps-1') and (config[4] == 'no2-concentration'):
      data = dat.uea_caps_1(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.no2_concentration(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.no2_concentration(meta, data, nc)
         nc.close()  
      
   if (config[3] == 'uea-fidas200E-1') and (config[4] == 'pm-concentration'):
      data = dat.uea_fidas200E_1(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.pm_concentration(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.pm_concentration(meta, data, nc)
         nc.close()
      
   if (config[3] == 'uea-radon-1') and (config[4] == 'radon-concentration'):
      data = dat.uea_radon_1(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.radon_concentration(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.radon_concentration(meta, data, nc)
         nc.close()
   
   if (config[3] == 'uea-sodar-rass-1') and (config[4] == 'acoustic-backscatter-winds'):
      data = dat.uea_sodar_rass_1(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.acoustic_backscatter_winds(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.acoustic_backscatter_winds(meta, data, nc)
         nc.close()
         
   if (config[3] == 'uea-sodar-rass-1') and (config[4] == 'boundary-layer-temperature-profiles'):
      data = dat.uea_sodar_rass_1(config, data, logfile) 
      data = dat.data_chunker(config, data, logfile)
      try:
         for n in range (len(data.st)):
            data.counter = n
            nc = prod.create_NC_file(config, data.ET[data.st[n]], opt, logfile)
            prod.boundary_layer_temperature_profiles(meta, data, nc)
            nc.close()
      except:
         nc = prod.create_NC_file(config, data.ET[data.st], opt, logfile)
         prod.boundary_layer_temperature_profiles(meta, data, nc)
         nc.close()      
         
   del dat, prod

def t_control(logfile): 
   from collections import namedtuple  
   
   # read in and process config file 
   config = read_config(logfile)
   
   # read in meta file
   meta = read_meta(logfile, config[3])
  
   #set up data tuple
   data = namedtuple("data", "") 
   
   # do the run
   do_run(config, meta, data, logfile)
   