def create_NC_file(config, start_date, opt, logfile):
   from netCDF4 import Dataset
   from datetime import datetime
   import os.path
 
   dout = 'Data' # out put directory
   
   f1 = config[3] # instrument name
   f2 = 'wao' # platform
   if config[1] == 'day':
     f3 = datetime.fromtimestamp(int(start_date)).strftime('%Y%m%d') # date
   if config[1] == 'month':
     f3 = datetime.fromtimestamp(int(start_date)).strftime('%Y%m') # date
   if config[1] == 'year':
     f3 = datetime.fromtimestamp(int(start_date)).strftime('%Y') # date
   f4 = config[4] # data product
   f5 = 'v' + config[0] # file version number
   f6 = '.nc'
   if len(opt) < 1:
      f7 = f1+chr(95)+f2+chr(95)+f3+chr(95)+f4+chr(95)+f5+f6  
   else:         
      f7 = f1+chr(95)+f2+chr(95)+f3+chr(95)+f4+chr(95)+opt+chr(95)+f5+f6
      
   fn = os.path.join(dout, ' '.join(map(str, f7)))
   
   try:   
      nc = Dataset(fn, "w",  format = "NETCDF4_CLASSIC") 
   except:
      # exit if problem encountered
      print('Unable to create: ',fn,'. This program will terminate')
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat()+' Unable to create: '+fn+'. This program will terminate\n')
      g.close()
      exit()
      
      del Dataset, datetime

   return nc

# A
def acoustic_backscatter_winds(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data & flag
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD11 = data.H[data.st:data.ed,:] # Height H
      DD2 = data.R[data.st:data.ed,:] # Sound intensity R
      DD3 = data.V[data.st:data.ed,:] # windspeed V
      DD4 = data.D[data.st:data.ed,:] # wind direction D
      DD5 = data.VVU[data.st:data.ed,:] # Eastward wind VVU
      DD6 = data.VVV[data.st:data.ed,:] # Northward wind VVV
      DD7 = data.VVW[data.st:data.ed,:] # Upward wind VVW
      FL1 = data.qc_backscatter[data.st:data.ed,:]
      FL2 = data.qc_mean_winds[data.st:data.ed,:]
      FL3 = data.qc_wind_component_eastward[data.st:data.ed,:]
      FL4 = data.qc_wind_component_northward[data.st:data.ed,:]
      FL5 = data.qc_wind_component_upward_air_velocity[data.st:data.ed,:]
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter],:]
      DD11 = data.H[data.st[data.counter]:data.ed[data.counter],:] # Height H
      DD2 = data.R[data.st[data.counter]:data.ed[data.counter],:]# Sound intensity R
      DD3 = data.V[data.st[data.counter]:data.ed[data.counter],:]# windspeed V
      DD4 = data.D[data.st[data.counter]:data.ed[data.counter],:] # wind direction D
      DD5 = data.VVU[data.st[data.counter]:data.ed[data.counter],:] # Eastward wind VVU
      DD6 = data.VVV[data.st[data.counter]:data.ed[data.counter],:] # Northward wind VVV
      DD7 = data.VVW[data.st[data.counter]:data.ed[data.counter],:]# Upward wind VVW
      FL1 = data.qc_backscatter[data.st[data.counter]:data.ed[data.counter],:]
      FL2 = data.qc_mean_winds[data.st[data.counter]:data.ed[data.counter],:]
      FL3 = data.qc_wind_component_eastward[data.st[data.counter]:data.ed[data.counter],:]
      FL4 = data.qc_wind_component_northward[data.st[data.counter]:data.ed[data.counter],:]
      FL5 = data.qc_wind_component_upward_air_velocity[data.st[data.counter]:data.ed[data.counter],:]
      
   # valid max and min values
   DD1 = np.array(DD11[1,:])
   XX1 = np.array(DD1) # height
   min_dat1 = np.float32(np.min(XX1))
   max_dat1 = np.float32(np.max(XX1)) 

   XX2 = np.array(DD2) # backscatter
   np.putmask(XX2, FL1 != 1, np.nan)
   min_dat2 = np.float32(np.nanmin(XX2))
   max_dat2 = np.float32(np.nanmax(XX2)) 
  
   XX3 = np.array(DD3) # wind speeds
   np.putmask(XX3, FL2 != 1, np.nan)
   min_dat3 = np.float32(np.nanmin(XX3))
   max_dat3 = np.float32(np.nanmax(XX3)) 

   XX4 = np.array(DD4) # wind direction
   np.putmask(XX4, FL2 != 1, np.nan)
   min_dat4 = np.float32(np.nanmin(XX4))
   max_dat4 = np.float32(np.nanmax(XX4)) 

   XX5 = np.array(DD5) # eastward
   np.putmask(XX5, FL3 != 1, np.nan)
   min_dat5 = np.float32(np.nanmin(XX5))
   max_dat5 = np.float32(np.nanmax(XX5))
   
   XX6 = np.array(DD6) # northward
   np.putmask(XX6, FL4 != 1, np.nan)
   min_dat6 = np.float32(np.nanmin(XX6))
   max_dat6 = np.float32(np.nanmax(XX6)) 

   XX7 = np.array(DD7) 
   np.putmask(XX7, FL5 != 1, np.nan)
   min_dat7 = np.float32(np.nanmin(XX7))
   max_dat7 = np.float32(np.nanmax(XX7)) 
   
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write specific dimensions
   altitude = nc.createDimension('altitude', len(DD1))
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('altitude', np.float32, ('altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm'
   v.standard_name = 'altitude'
   v.long_name = 'Geometric height above geoid (WGS84).'
   v.axis = 'Z'
   v.valid_min = np.float32(min_dat1 + 10)
   v.valid_max = np.float32(max_dat1 + 10)
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(DD1 + 10)
   
   v = nc.createVariable('sound_intensity_level_in_air', np.float32, ('time', 'altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'dB'
   v.standard_name = 'sound_intensity_level_in_air'
   v.long_name = 'Sound Intensity Level in Air'
   v.valid_min = np.float32(min_dat2)
   v.valid_max = np.float32(max_dat2)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(DD2)
   
   v = nc.createVariable('wind_speed', np.float32, ('time', 'altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.standard_name = 'wind_speed'
   v.long_name = 'Wind Speed'
   v.valid_min = np.float32(min_dat3)
   v.valid_max = np.float32(max_dat3)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(DD3)
   
   v = nc.createVariable('wind_from_direction', np.float32, ('time', 'altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'degree'
   v.standard_name = 'wind_from_direction'
   v.long_name = 'Wind From Direction'
   v.valid_min = np.float32(min_dat4)
   v.valid_max = np.float32(max_dat4)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(DD4)
  
   v = nc.createVariable('eastward_wind', np.float32, ('time', 'altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.standard_name = 'eastward_wind'
   v.long_name = 'Eastward Wind Component (U)'
   v.valid_min = np.float32(min_dat5)
   v.valid_max = np.float32(max_dat5)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(DD5)
   
   v = nc.createVariable('northward_wind', np.float32, ('time', 'altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.standard_name = 'northward_wind'
   v.long_name = 'Northward Wind Component (V)'
   v.valid_min = np.float32(min_dat6)
   v.valid_max = np.float32(max_dat6)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(DD6)
   
   v = nc.createVariable('upward_air_velocity', np.float32, ('time', 'altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.standard_name = 'upward_air_velocity'
   v.long_name = 'Upward Air Velocity (W)'
   v.valid_min = np.float32(min_dat7)
   v.valid_max = np.float32(max_dat7)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(DD7)
   
   v = nc.createVariable('qc_flag_mean_winds', np.int8, ('time', 'altitude',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Mean Winds'
   v.flag_values = '0b,1b,2b,3b,4b,5b,6b,7b,8b,9b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise<0' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise>50' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:mean_wind_speed<0ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:mean_wind_speed>35ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:mean_wind_direction<0degrees' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:mean_wind_direction>=360degrees' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:mean_wind_speed==0ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:time_stamp_error' 
   #write data
   v[:,:] = np.int8(FL2)
   
   v = nc.createVariable('qc_flag_wind_component_eastward', np.int8, ('time', 'altitude',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Eastward Wind Component (U)'
   v.flag_values = '0b,1b,2b,3b,4b,5b,6b,7b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise<0' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise>50' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:U_component<-10ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:U_component>10ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:U_component==0ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:time_stamp_error' 
   #write data
   v[:,:] = np.int8(FL3)
   
   v = nc.createVariable('qc_flag_wind_component_northward', np.int8, ('time', 'altitude',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Northward Wind Component (V)'
   v.flag_values = '0b,1b,2b,3b,4b,5b,6b,7b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise<0' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise>50' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:U_component<-10ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:U_component>10ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:U_component==0ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:time_stamp_error' 
   #write data
   v[:,:] = np.int8(FL4)
   
   v = nc.createVariable('qc_flag_wind_component_upward_air_velocity', np.int8, ('time', 'altitude',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Upward Air Velocity (W)'
   v.flag_values = '0b,1b,2b,3b,4b,5b,6b,7b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise<0' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise>50' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:U_component<-10ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:U_component>10ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:U_component==0ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:time_stamp_error' 
   #write data
   v[:,:] = np.int8(FL5)
   
   v = nc.createVariable('qc_flag_backscatter', np.int8, ('time', 'altitude',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Backscatter'
   v.flag_values = '0b,1b,2b,3b,4b,5b,6b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise<0' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise>50' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:backscatter<1dB' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:backscatter>90db' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:time_stamp_error' 
   #write data
   v[:,:] = np.int8(FL1)
   
def aerosol_backscatter(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data & flag
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.ZZ[data.st:data.ed] # altitude
      DD2 = data.BB[data.st:data.ed,:] # backscatter
      HK = data.HK2[data.st:data.ed,:] # house keeping
      FL1 = data.BB_flag[data.st:data.ed,:]
      
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter],:]
      DD1 = data.ZZ[data.st[data.counter]:data.ed[data.counter]] # altitude
      DD2 = data.BB[data.st[data.counter]:data.ed[data.counter],:] # backscatter
      HK = data.HK2[data.st[data.counter]:data.ed[data.counter],:] # house keeping
      FL1 = data.BB_flag[data.st[data.counter]:data.ed[data.counter],:]
   
   # valid max and min values
   XX1 = np.array(DD1) # height
   min_dat1 = np.float32(np.min(XX1))
   max_dat1 = np.float32(np.max(XX1)) 

   XX2 = np.array(DD2) # backscatter
   np.putmask(XX2, FL1 != 1, np.nan)
   min_dat2 = np.float32(np.nanmin(XX2))
   max_dat2 = np.float32(np.nanmax(XX2)) 
  
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
   nc.setncattr('laser_wavelength', '905 nm')
   nc.setncattr('nominal_laser_pulse_energy', '1.6e-06 J')
   nc.setncattr('pulse_repetition_frequency', '5570 s-1')
   nc.setncattr('lens_diameter', '0.145 m')
   nc.setncattr('beam_divergence', '0.53 mrad')
   nc.setncattr('pulse_length', 'Not Known')
   nc.setncattr('sampling_frequency', 'Not Known')
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write specific dimensions
   altitude = nc.createDimension('altitude', 256)
   
   # write common variables
   com.variables(nc, data)    

   # write specific variables
   v = nc.createVariable('altitude', np.float32, ('altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm'
   v.standard_name = 'altitude'
   v.long_name = 'Geometric height above geoid (WGS84).'
   v.axis = 'Z'
   v.valid_min = np.float32(min_dat1 + 10)
   v.valid_max = np.float32(max_dat1 + 10)
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(DD1 + 10)
      
   v = nc.createVariable('attenuated_aerosol_backscatter_coefficient', np.float32, ('time', 'altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm-1 sr-1'
   v.long_name = 'Attenuated Aerosol Backscatter Coefficient'
   v.valid_min = np.float32(min_dat2)
   v.valid_max = np.float32(max_dat2)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(DD2)    
   
   v = nc.createVariable('laser_pulse_energy', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = '%'
   v.long_name = 'Laser Pulse Energy (% of maximum)'
   v.valid_min = np.float32(min(HK[:,2]))
   v.valid_max = np.float32(max(HK[:,2]))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(HK[:,2])
   
   v = nc.createVariable('laser_temperature', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'K'
   v.long_name = 'Laser Temperature'
   v.valid_min = np.float32(min(HK[:,3]))
   v.valid_max = np.float32(max(HK[:,3]))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(HK[:,3])
   
   v = nc.createVariable('sensor_zenith_angle', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'degree'
   v.standard_name = 'sensor_zenith_angle'
   v.long_name = 'Sensor Zenith Angle (from vertical)'
   v.valid_min = np.float32(min(HK[:,6]))
   v.valid_max = np.float32(max(HK[:,6]))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(HK[:,6])
   
   v = nc.createVariable('profile_scaling', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = '%'
   v.long_name = 'Scaling of range profile (default = 100%)'
   v.valid_min = np.float32(min(HK[:,0]))
   v.valid_max = np.float32(max(HK[:,0]))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(HK[:,0])
   
   v = nc.createVariable('window_contamination', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'mV'
   v.long_name = 'Window Contamination (mV as measured by ADC: 0 - 2500)'
   v.valid_min = np.float32(min(HK[:,5]))
   v.valid_max = np.float32(max(HK[:,5]))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(HK[:,5])
   
   v = nc.createVariable('background_light', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'mV'
   v.long_name = 'Background Light (mV as measured by ADC: 0 - 2500)'
   v.valid_min = np.float32(min(HK[:,7]))
   v.valid_max = np.float32(max(HK[:,7]))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(HK[:,7])
   
   v = nc.createVariable('backscatter_sum', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'sr-1'
   v.long_name = 'Sum of detected and normalized backscatter'
   v.valid_min = np.float32(min(HK[:,9]))
   v.valid_max = np.float32(max(HK[:,9]))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(HK[:,9])
   
   v = nc.createVariable('qc_flag', np.float32, ('time', 'altitude',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_attenuated_aerosol_backscatter_coefficient_outside_instrument_operational_range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'    
   #write data
   v[:,:] = np.int8(FL1)
      
#B
def boundary_layer_temperature_profiles(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data & flag
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD11 = data.H[data.st:data.ed,:] # Height H
      DD2 = data.RTP[data.st:data.ed,:] # temperature
      FL1 = data.qc_temperature[data.st:data.ed,:]
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter],:]
      DD11 = data.H[data.st[data.counter]:data.ed[data.counter],:] # Height H
      DD2 = data.RTP[data.st[data.counter]:data.ed[data.counter],:]# Sound intensity R
      FL1 = data.qc_temperature[data.st[data.counter]:data.ed[data.counter],:]
      
   # valid max and min values
   DD1 = np.array(DD11[1,:])
   XX1 = np.array(DD1) # height
   min_dat1 = np.float32(np.min(XX1))
   max_dat1 = np.float32(np.max(XX1)) 

   XX2 = np.array(DD2) # temperature
   np.putmask(XX2, FL1 != 1, np.nan)
   min_dat2 = np.float32(np.nanmin(XX2))
   max_dat2 = np.float32(np.nanmax(XX2)) 
  
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write specific dimensions
   altitude = nc.createDimension('altitude', len(DD1))
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('altitude', np.float32, ('altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm'
   v.standard_name = 'altitude'
   v.long_name = 'Geometric height above geoid (WGS84).'
   v.axis = 'Z'
   v.valid_min = np.float32(min_dat1 + 10)
   v.valid_max = np.float32(max_dat1 + 10)
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(DD1 + 10)
   
   v = nc.createVariable('air_temperature', np.float32, ('time', 'altitude',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'K'
   v.standard_name = 'air_temperature'
   v.long_name = 'SODAR RASS Air Temperatrue'
   v.valid_min = np.float32(min_dat2 + 273.15)
   v.valid_max = np.float32(max_dat2 + 273.15)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(DD2 + 273.15)
   
   v = nc.createVariable('qc_flag', np.int8, ('time', 'altitude',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b,4b,5b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise<0' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:signal_to_noise>50' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:Air Temperature<-50C' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data:Air temperature>50C' + '\n' 
   #write data
   v[:,:] = np.int8(FL1)
   
#C   
def ch4_concentration(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data & flag - two species
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.species1[data.st:data.ed]
      FL1 = data.flag1[data.st:data.ed]
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
      DD1 = data.species1[data.st[data.counter]:data.ed[data.counter]]
      FL1 = data.flag1[data.st[data.counter]:data.ed[data.counter]]
      
   # valid max and min values
   XX1 = np.array(DD1)
   np.putmask(XX1, FL1 != 1, np.nan)
   min_dat1 = np.float32(np.nanmin(XX1))
   max_dat1 = np.float32(np.nanmax(XX1))  

   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables  
   v = nc.createVariable('mole_fraction_of_methane_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit1
   v.practical_units = data.practical_units1
   v.standard_name = 'mole_fraction_of_methane_in_air'
   v.long_name = 'Mole Fraction of Methane in air'
   v.valid_min = np.float32(min_dat1)
   v.valid_max = np.float32(max_dat1)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'CH4'
   # write data
   v[:] = np.float32(DD1)
   
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:_data=0' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'    
   # write data
   v[:] = np.int8(FL1)
      
         
def ch4_n2o_co2_co_concentration(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data & flag
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.species1[data.st:data.ed]
      DD2 = data.species2[data.st:data.ed]
      DD3 = data.species3[data.st:data.ed]
      DD4 = data.species4[data.st:data.ed]
      FL1 = data.flag1[data.st:data.ed]
      FL2 = data.flag2[data.st:data.ed]  
      FL3 = data.flag3[data.st:data.ed]
      FL4 = data.flag4[data.st:data.ed]  
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
      DD1 = data.species1[data.st[data.counter]:data.ed[data.counter]]
      DD2 = data.species2[data.st[data.counter]:data.ed[data.counter]]
      DD3 = data.species3[data.st[data.counter]:data.ed[data.counter]]
      DD4 = data.species4[data.st[data.counter]:data.ed[data.counter]]
      FL1 = data.flag1[data.st[data.counter]:data.ed[data.counter]]
      FL2 = data.flag2[data.st[data.counter]:data.ed[data.counter]]
      FL3 = data.flag3[data.st[data.counter]:data.ed[data.counter]]
      FL4 = data.flag4[data.st[data.counter]:data.ed[data.counter]]
   
   # valid max and min values
   XX1 = np.array(DD1)
   np.putmask(XX1, FL1 != 1, np.nan)
   min_dat1 = np.float32(np.nanmin(XX1))
   max_dat1 = np.float32(np.nanmax(XX1))  
   
   XX2 = np.array(DD2)
   np.putmask(XX2, FL2 != 1, np.nan)
   min_dat2 = np.float32(np.nanmin(XX2))
   max_dat2 = np.float32(np.nanmax(XX2)) 

   XX3 = np.array(DD3)
   np.putmask(XX3, FL3 != 1, np.nan)
   min_dat3 = np.float32(np.nanmin(XX3))
   max_dat3 = np.float32(np.nanmax(XX3))
   
   XX4 = np.array(DD4)
   np.putmask(XX4, FL4 != 1, np.nan)
   min_dat4 = np.float32(np.nanmin(XX4))
   max_dat4 = np.float32(np.nanmax(XX4))   
      
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('mole_fraction_of_methane_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit1
   v.practical_units = data.practical_units1
   v.standard_name = 'mole_fraction_of_methane_in_air'
   v.long_name = 'Mole Fraction of Methane in air'
   v.valid_min = np.float32(min_dat1)
   v.valid_max = np.float32(max_dat1)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'CH4'
   # write data
   v[:] = np.float32(DD1)
   
   v = nc.createVariable('mole_fraction_of_nitrous_oxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit2
   v.practical_units = data.practical_units2
   v.standard_name = 'mole_fraction_of_nitrous_oxide_in_air'
   v.long_name = 'Mole Fraction of Nitrous Oxide in air'
   v.valid_min = np.float32(min_dat2)
   v.valid_max = np.float32(max_dat2)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'N2O'
   # write data
   v[:] = np.float32(DD2)
  
   v = nc.createVariable('mole_fraction_of_carbon_monoxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit3
   v.practical_units = data.practical_units3
   v.standard_name = 'mole_fraction_of_carbon_monoxide_in_air'
   v.long_name = 'Mole Fraction of Carbon Monoxide in air'
   v.valid_min = np.float32(min_dat3)
   v.valid_max = np.float32(max_dat3)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'CO'
   # write data
   v[:] = np.float32(DD3)  
   
   v = nc.createVariable('mole_fraction_of_carbon_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = data.unit4
   v.practical_units = data.practical_units4
   v.standard_name = 'mole_fraction_of_carbon_dioxide_in_air'
   v.long_name = 'Mole Fraction of Carbon Dioxide in air'
   v.valid_min = np.float32(min_dat4)
   v.valid_max = np.float32(max_dat4)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'CO2'
   # write data
   v[:] = np.float32(DD4)
  
   v = nc.createVariable('qc_flag_ch4', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: CH4'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:_data=0' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'    
   # write data
   v[:] = np.int8(FL1)
   
   v = nc.createVariable('qc_flag_n2o', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: N2O'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:_data=0' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'    
   # write data
   v[:] = np.int8(FL2)
   
   v = nc.createVariable('qc_flag_co', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: CO'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:_data=0' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'    
   # write data
   v[:] = np.int8(FL3)
   
   v = nc.createVariable('qc_flag_co2', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: CO2'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:_data=0' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'    
   # write data
   v[:] = np.int8(FL4)

def cloud_base(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data & flag
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.CBH[data.st:data.ed,:] # cloud base altitude
      FL1 = data.CBH_flag[data.st:data.ed,:]
      HK = data.HK2[data.st:data.ed]
      
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter],:]
      DD1 = data.CBH[data.st[data.counter]:data.ed[data.counter],:] # cloud base altitude
      FL1 = data.CBH_flag[data.st[data.counter]:data.ed[data.counter],:]
      HK = data.HK2[data.st[data.counter]:data.ed[data.counter]]
   
   # valid max and min values
   XX1 = np.array(DD1[:,0]) 
   XX2 = np.array(DD1[:,1]) 
   XX3 = np.array(DD1[:,2]) 
   np.putmask(XX1, FL1[:,0] != 1, np.nan)
   np.putmask(XX2, FL1[:,1] != 1, np.nan)
   np.putmask(XX3, FL1[:,2] != 1, np.nan)
   np.putmask(XX1, XX1 < 0, np.nan)
   np.putmask(XX2, XX2 < 0, np.nan)
   np.putmask(XX3, XX3 < 0, np.nan)
   XX4 = np.array([XX1, XX2, XX3])   
   min_dat1 = np.float32(np.nanmin(XX4))
   max_dat1 = np.float32(np.nanmax(XX4)) 
  
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
   nc.setncattr('laser_wavelength', '905 nm')
   nc.setncattr('nominal_laser_pulse_energy', '1.6e-06 J')
   nc.setncattr('pulse_repetition_frequency', '5570 s-1')
   nc.setncattr('lens_diameter', '0.145 m')
   nc.setncattr('beam_divergence', '0.53 mrad')
   nc.setncattr('pulse_length', 'Not Known')
   nc.setncattr('sampling_frequency', 'Not Known')
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write specific dimensions
   layer_index = nc.createDimension('layer_index', 3)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('cloud_base_altitude', np.float32, ('time','layer_index',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm'
   v.standard_name = 'cloud_base_altitude'
   v.long_name = 'Cloud Base Altitude (Geometric height above geoid WGS84)'
   v.valid_min = np.float32(min_dat1)
   v.valid_max = np.float32(max_dat1)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:,:] = np.float32(DD1)
   
   v = nc.createVariable('laser_pulse_energy', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = '%'
   v.long_name = 'Laser Pulse Energy (% of maximum)'
   v.valid_min = np.float32(min(HK[:,2]))
   v.valid_max = np.float32(max(HK[:,2]))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(HK[:,2])
   
   v = nc.createVariable('laser_temperature', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'K'
   v.long_name = 'Laser Temperature'
   v.valid_min = np.float32(min(HK[:,3]))
   v.valid_max = np.float32(max(HK[:,3]))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(HK[:,3])
   
   v = nc.createVariable('sensor_zenith_angle', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'degree'
   v.standard_name = 'sensor_zenith_angle'
   v.long_name = 'Sensor Zenith Angle (from vertical)'
   v.valid_min = np.float32(min(HK[:,6]))
   v.valid_max = np.float32(max(HK[:,6]))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(HK[:,6])
   
   v = nc.createVariable('profile_scaling', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = '%'
   v.long_name = 'Scaling of range profile (default = 100%)'
   v.valid_min = np.float32(min(HK[:,0]))
   v.valid_max = np.float32(max(HK[:,0]))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(HK[:,0])
   
   v = nc.createVariable('window_contamination', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'mV'
   v.long_name = 'Window Contamination (mV as measured by ADC: 0 - 2500)'
   v.valid_min = np.float32(min(HK[:,5]))
   v.valid_max = np.float32(max(HK[:,5]))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(HK[:,5])
   
   v = nc.createVariable('background_light', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'mV'
   v.long_name = 'Background Light (mV as measured by ADC: 0 - 2500)'
   v.valid_min = np.float32(min(HK[:,7]))
   v.valid_max = np.float32(max(HK[:,7]))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(HK[:,7])
   
   v = nc.createVariable('backscatter_sum', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'sr-1'
   v.long_name = 'Sum of detected and normalized backscatter'
   v.valid_min = np.float32(min(HK[:,9]))
   v.valid_max = np.float32(max(HK[:,9]))
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(HK[:,9])
   
   v = nc.createVariable('qc_flag', np.int8, ('time','layer_index',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b,4b,5b,6b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_no_signifcant_backscatter' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_full_obscuration_determined_but_no_cloud_base_detected' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_some_obscuration_detected_but_determined_to_be_transparent' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_raw_data_missing' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'    
   #write data
   v[:,:] = np.int8(FL1)
            
def co_h2_concentration(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data & flag
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.species1[data.st:data.ed]
      DD2 = data.species2[data.st:data.ed]
      FL1 = data.flag1[data.st:data.ed]
      FL2 = data.flag2[data.st:data.ed]  
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
      DD1 = data.species1[data.st[data.counter]:data.ed[data.counter]]
      DD2 = data.species2[data.st[data.counter]:data.ed[data.counter]]
      FL1 = data.flag1[data.st[data.counter]:data.ed[data.counter]]
      FL2 = data.flag2[data.st[data.counter]:data.ed[data.counter]]
      
   # valid max and min values
   XX1 = np.array(DD1)
   np.putmask(XX1, FL1 != 1, np.nan)
   min_dat1 = np.float32(np.nanmin(XX1))
   max_dat1 = np.float32(np.nanmax(XX1))  
   
   XX2 = np.array(DD2)
   np.putmask(XX2, FL2 != 1, np.nan)
   min_dat2 = np.float32(np.nanmin(XX2))
   max_dat2 = np.float32(np.nanmax(XX2))    
      
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('mole_fraction_of_carbon_monoxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit1
   v.practical_units = data.practical_units1
   v.standard_name = 'mole_fraction_of_carbon_monoxide_in_air'
   v.long_name = 'Mole Fraction of Carbon Monoxide in air'
   v.valid_min = np.float32(min_dat1)
   v.valid_max = np.float32(max_dat1)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'CO'
   # write data
   v[:] = np.float32(DD1)
   
   v = nc.createVariable('mole_fraction_of_molecular_hydrogen_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit2
   v.practical_units = data.practical_units2
   v.standard_name = 'mole_fraction_of_molecular_hydrogen_in_air'
   v.long_name = 'Mole Fraction of Molecular Hydrogen in air'
   v.valid_min = np.float32(min_dat2)
   v.valid_max = np.float32(max_dat2)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'H2'
   # write data
   v[:] = np.float32(DD2)
      
   v = nc.createVariable('qc_flag_co', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: CO'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:_data=0' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'    
   # write data
   v[:] = np.int8(FL1)
   
   v = nc.createVariable('qc_flag_h2', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: H2'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:_data=0' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   # write data
   v[:] = np.int8(FL2)
                  
def co2_concentration(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data & flag
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.species1[data.st:data.ed]
      FL1 = data.flag1[data.st:data.ed]
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
      DD1 = data.species1[data.st[data.counter]:data.ed[data.counter]]
      FL1 = data.flag1[data.st[data.counter]:data.ed[data.counter]]
      
   # valid max and min values
   XX1 = np.array(DD1)
   np.putmask(XX1, FL1 != 1, np.nan)
   min_dat1 = np.float32(np.nanmin(XX1))
   max_dat1 = np.float32(np.nanmax(XX1))   
      
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('mole_fraction_of_carbon_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit1
   v.practical_units = data.practical_units1
   v.standard_name = 'mole_fraction_of_carbon_dioxide_in_air'
   v.long_name = 'Mole Fraction of Carbon Dioxide in air'
   v.valid_min = np.float32(min_dat1)
   v.valid_max = np.float32(max_dat1)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'CO2'
   # write data
   v[:] = np.float32(DD1)
     
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   # write data
   v[:] = np.int8(FL1)
   
# D   
# E
# F
# G
# H
def h2_concentration(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data, flag, time
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.species1[data.st:data.ed]
      FL1 = data.flag1[data.st:data.ed]
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
      DD1 = data.species1[data.st[data.counter]:data.ed[data.counter]]
      FL1 = data.flag1[data.st[data.counter]:data.ed[data.counter]]
      
   # valid max and min values
   XX1 = np.array(DD1)
   np.putmask(XX1, FL1 != 1, np.nan)
   min_dat1 = np.float32(np.nanmin(XX1))
   max_dat1 = np.float32(np.nanmax(XX1))   
      
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('mole_fraction_of_molecular_hydrogen_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit1
   v.practical_units = data.practical_units1
   v.standard_name = 'mole_fraction_of_molecular_hydrogen_in_air'
   v.long_name = 'Mole Fraction of Molecular Hydrogen in air'
   v.valid_min = np.float32(min_dat1)
   v.valid_max = np.float32(max_dat1)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'H2'
   # write data
   v[:] = np.float32(DD1)
   
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_data_not_quality_controlled' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:_data=0' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   # write data
   v[:] = np.int8(FL1)
   
 # I
 # J
 # K
 # L
 # M
 # N
def n2o_sf6_concentration(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data, flag, time
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.species1[data.st:data.ed]
      DD2 = data.species2[data.st:data.ed]
      FL1 = data.flag1[data.st:data.ed]
      FL2 = data.flag2[data.st:data.ed]
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
      DD1 = data.species1[data.st[data.counter]:data.ed[data.counter]]
      DD2 = data.species2[data.st[data.counter]:data.ed[data.counter]]
      FL1 = data.flag1[data.st[data.counter]:data.ed[data.counter]]
      FL2 = data.flag2[data.st[data.counter]:data.ed[data.counter]]
      
   # valid max and min values
   XX1 = np.array(DD1)
   np.putmask(XX1, FL1 != 1, np.nan)
   min_dat1 = np.float32(np.nanmin(XX1))
   max_dat1 = np.float32(np.nanmax(XX1)) 

   XX2 = np.array(DD2)
   np.putmask(XX2, FL2 != 1, np.nan)
   min_dat2 = np.float32(np.nanmin(XX2))
   max_dat2 = np.float32(np.nanmax(XX2))   
      
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('mole_fraction_of_nitrous_oxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit1
   v.practical_units = data.practical_units1
   v.standard_name = 'mole_fraction_of_nitrous_oxide_in_air'
   v.long_name = 'Mole Fraction of Nitrous Oxide in air'
   v.valid_min = np.float32(min_dat1)
   v.valid_max = np.float32(max_dat1)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'N2O'
   # write data
   v[:] = np.float32(DD1)
  
   v = nc.createVariable('mole_fraction_of_sulfur_hexafluoride_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit2
   v.practical_units = data.practical_units2
   v.long_name = 'Mole Fraction of Sulphur Hexafluoride in air'
   v.valid_min = np.float32(min_dat2)
   v.valid_max = np.float32(max_dat2)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'SF6'
   # write data
   v[:] = np.float32(DD2)
   
   v = nc.createVariable('qc_flag_n2o', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: N2O'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_unspecified_instrument_performance_issues_contact_data_originator_for_more_information' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   # write data
   v[:] = np.int8(FL1)
   
   v = nc.createVariable('qc_flag_sf6', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: SF6'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_unspecified_instrument_performance_issues_contact_data_originator_for_more_information' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   # write data
   v[:] = np.int8(FL2)
   
def no2_concentration(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data, flag, time
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.species1[data.st:data.ed]
      FL1 = data.flag1[data.st:data.ed]
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
      DD1 = data.species1[data.st[data.counter]:data.ed[data.counter]]
      FL1 = data.flag1[data.st[data.counter]:data.ed[data.counter]]
      
   # valid max and min values
   XX1 = np.array(DD1)
   np.putmask(XX1, FL1 != 1, np.nan)
   min_dat1 = np.float32(np.nanmin(XX1))
   max_dat1 = np.float32(np.nanmax(XX1))  
      
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('mole_fraction_of_nitrogen_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit1
   v.practical_units = data.practical_units1
   v.standard_name = 'mole_fraction_of_nitrogen_dioxide_in_air'
   v.long_name = 'Mole Fraction of Nitrogen Dioxide in air'
   v.valid_min = np.float32(min_dat1)
   v.valid_max = np.float32(max_dat1)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'NO2'
   # write data
   v[:] = np.float32(DD1)
   
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_gas_concentration_outside_instrument_operational _range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp _error' 
   # write data
   v[:] = np.int8(FL1)
         
def nox_noxy_concentration(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data, flag, time
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.species1[data.st:data.ed]
      DD2 = data.species2[data.st:data.ed]
      DD3 = data.species3[data.st:data.ed]
      FL1 = data.flag1[data.st:data.ed]
      FL2 = data.flag2[data.st:data.ed]
      FL3 = data.flag3[data.st:data.ed]
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
      DD1 = data.species1[data.st[data.counter]:data.ed[data.counter]]
      DD2 = data.species2[data.st[data.counter]:data.ed[data.counter]]
      DD3 = data.species3[data.st[data.counter]:data.ed[data.counter]]
      FL1 = data.flag1[data.st[data.counter]:data.ed[data.counter]]
      FL2 = data.flag2[data.st[data.counter]:data.ed[data.counter]]
      FL3 = data.flag3[data.st[data.counter]:data.ed[data.counter]]
      
   # valid max and min values
   XX1 = np.array(DD1)
   np.putmask(XX1, FL1 != 1, np.nan)
   min_dat1 = np.float32(np.nanmin(XX1))
   max_dat1 = np.float32(np.nanmax(XX1)) 

   XX2 = np.array(DD2)
   np.putmask(XX2, FL2 != 1, np.nan)
   min_dat2 = np.float32(np.nanmin(XX2))
   max_dat2 = np.float32(np.nanmax(XX2))   

   XX3 = np.array(DD3)
   np.putmask(XX3, FL3 != 1, np.nan)
   min_dat3 = np.float32(np.nanmin(XX3))
   max_dat3 = np.float32(np.nanmax(XX3))    
      
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('mole_fraction_of_nitric_oxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit1
   v.practical_units = data.practical_units1
   v.long_name = 'Mole Fraction of Nitric Oxide in air'
   v.valid_min = np.float32(min_dat1)
   v.valid_max = np.float32(max_dat1)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'NO'
   # write data
   v[:] = np.float32(DD1)  
 
   v = nc.createVariable('mole_fraction_of_nitrogen_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit2
   v.practical_units = data.practical_units2
   v.standard_name = 'mole_fraction_of_nitrogen_dioxide_in_air'
   v.long_name = 'Mole Fraction of Nitrogen Dioxide in air'
   v.valid_min = np.float32(min_dat2)
   v.valid_max = np.float32(max_dat2)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'NO2'
   # write data
   v[:] = np.float32(DD2)
   
   v = nc.createVariable('mole_fraction_of_nox_expressed_as_nitrogen_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit3
   v.practical_units = data.practical_units3
   v.standard_name = 'mole_fraction_of_nox_expressed_as_nitrogen_in_air'
   v.long_name = 'Mole Fraction of NOx in air'
   v.valid_min = np.float32(min_dat3)
   v.valid_max = np.float32(max_dat3)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'NOx'
   # write data
   v[:] = np.float32(DD3)
   
   v = nc.createVariable('qc_flag_no', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: NO'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   # write data
   v[:] = np.int8(FL1)
   
   v = nc.createVariable('qc_flag_no2', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: NO2'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   # write data
   v[:] = np.int8(FL2)
   
   v = nc.createVariable('qc_flag_nox', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: NOx'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   # write data
   v[:] = np.int8(FL3)
   
# O   
def o2n2_concentration_ratio(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data, flag, time
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.species1[data.st:data.ed]
      FL1 = data.flag1[data.st:data.ed]
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
      DD1 = data.species1[data.st[data.counter]:data.ed[data.counter]]
      FL1 = data.flag1[data.st[data.counter]:data.ed[data.counter]]
      
   # valid max and min values
   XX1 = np.array(DD1)
   np.putmask(XX1, FL1 != 1, np.nan)
   min_dat1 = np.float32(np.nanmin(XX1))
   max_dat1 = np.float32(np.nanmax(XX1))    
      
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('molecular_oxygen_molecular_nitrogen_ratio_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = 'per meg'
   v.long_name = 'O2/N2 ratio in air'
   v.valid_min = np.float32(min_dat1)
   v.valid_max = np.float32(max_dat1)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   # write data
   v[:] = np.float32(DD1)

   v = nc.createVariable('qc_flag', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_gas_concentration_outside_instrument_operational_range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   # write data
   v[:] = np.int8(FL1) 
         
def o3_concentration(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data, flag, time
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.species1[data.st:data.ed]
      FL1 = data.flag1[data.st:data.ed]
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
      DD1 = data.species1[data.st[data.counter]:data.ed[data.counter]]
      FL1 = data.flag1[data.st[data.counter]:data.ed[data.counter]]
      
   # valid max and min values
   XX1 = np.array(DD1)
   np.putmask(XX1, FL1 != 1, np.nan)
   min_dat1 = np.float32(np.nanmin(XX1))
   max_dat1 = np.float32(np.nanmax(XX1))    
      
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('mole_fraction_of_ozone_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit1
   v.practical_units = data.practical_units1
   v.standard_name = 'mole_fraction_of_ozone_in_air'
   v.long_name = 'Mole Fraction of Ozone in air'
   v.valid_min = np.float32(min_dat1)
   v.valid_max = np.float32(max_dat1)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'O3'
   # write data
   v[:] = np.float32(DD1)
   
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_unspecified_instrument_performance_issues_contact_data_originator_for_more_information' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   # write data
   v[:] = np.int8(FL1) 
   
# P
def pm_concentration(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data, flag, time
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.species1[data.st:data.ed]
      DD2 = data.species2[data.st:data.ed]
      DD3 = data.species3[data.st:data.ed]
      DD4 = data.species4[data.st:data.ed]
      DD5 = data.species5[data.st:data.ed]
      DD6 = data.species6[data.st:data.ed]
      FL1 = data.flag1[data.st:data.ed]
      FL2 = data.flag2[data.st:data.ed]
      FL3 = data.flag3[data.st:data.ed]
      FL4 = data.flag4[data.st:data.ed]
      FL5 = data.flag5[data.st:data.ed]
      FL6 = data.flag6[data.st:data.ed]      
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
      DD1 = data.species1[data.st[data.counter]:data.ed[data.counter]]
      DD2 = data.species2[data.st[data.counter]:data.ed[data.counter]]
      DD3 = data.species3[data.st[data.counter]:data.ed[data.counter]]
      DD4 = data.species4[data.st[data.counter]:data.ed[data.counter]]
      DD5 = data.species5[data.st[data.counter]:data.ed[data.counter]]
      DD6 = data.species6[data.st[data.counter]:data.ed[data.counter]]
      FL1 = data.flag1[data.st[data.counter]:data.ed[data.counter]]
      FL2 = data.flag2[data.st[data.counter]:data.ed[data.counter]]
      FL3 = data.flag3[data.st[data.counter]:data.ed[data.counter]]
      FL4 = data.flag4[data.st[data.counter]:data.ed[data.counter]]
      FL5 = data.flag5[data.st[data.counter]:data.ed[data.counter]]
      FL6 = data.flag6[data.st[data.counter]:data.ed[data.counter]]
   
   # valid max and min values
   XX1 = np.array(DD1)
   np.putmask(XX1, FL1 != 1, np.nan)
   min_dat1 = np.float32(np.nanmin(XX1))
   max_dat1 = np.float32(np.nanmax(XX1))
 
   XX2 = np.array(DD2)
   np.putmask(XX2, FL2 != 1, np.nan)
   min_dat2 = np.float32(np.nanmin(XX2))
   max_dat2 = np.float32(np.nanmax(XX2))

   XX3 = np.array(DD3)
   np.putmask(XX3, FL3 != 1, np.nan)
   min_dat3 = np.float32(np.nanmin(XX3))
   max_dat3 = np.float32(np.nanmax(XX3))

   XX4 = np.array(DD4)
   np.putmask(XX4, FL4 != 1, np.nan)
   min_dat4 = np.float32(np.nanmin(XX4))
   max_dat4 = np.float32(np.nanmax(XX4))
   
   XX5 = np.array(DD5)
   np.putmask(XX5, FL5 != 1, np.nan)
   min_dat5 = np.float32(np.nanmin(XX5))
   max_dat5 = np.float32(np.nanmax(XX5))

   XX6 = np.array(DD6)
   np.putmask(XX6, FL6 != 1, np.nan)
   min_dat6 = np.float32(np.nanmin(XX6))
   max_dat6 = np.float32(np.nanmax(XX6))
      
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('mass_concentration_of_pm1_ambient_aerosol_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'ug m-3'
   v.standard_name = 'mass_concentration_of_pm1_ambient_aerosol_in_air'
   v.long_name = 'Mass Concentration of PM1 Ambient Aerosol in Air'
   v.valid_min = np.float32(min_dat1)
   v.valid_max = np.float32(max_dat1)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(DD1)  
   
   v = nc.createVariable('mass_concentration_of_pm2p5_ambient_aerosol_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'ug m-3'
   v.standard_name = 'mass_concentration_of_pm2p5_ambient_aerosol_in_air'
   v.long_name = 'Mass Concentration of PM2.5 Ambient Aerosol in Air'
   v.valid_min = np.float32(min_dat2)
   v.valid_max = np.float32(max_dat2)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(DD2) 
   
   v = nc.createVariable('mass_concentration_of_pm4_ambient_aerosol_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'ug m-3'
   v.long_name = 'Mass Concentration of PM4 Ambient Aerosol in Air'
   v.valid_min = np.float32(min_dat3)
   v.valid_max = np.float32(max_dat3)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(DD3)
   
   v = nc.createVariable('mass_concentration_of_pm10_ambient_aerosol_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'ug m-3'
   v.standard_name = 'mass_concentration_of_pm10_ambient_aerosol_in_air'
   v.long_name = 'Mass Concentration of PM10 Ambient Aerosol in Air'
   v.valid_min = np.float32(min_dat4)
   v.valid_max = np.float32(max_dat4)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(DD4) 
   
   v = nc.createVariable('mass_concentration_of_total_pm_ambient_aerosol_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'ug m-3'
   v.long_name = 'Mass Concentration of Total PM Ambient Aerosol Particles in air'
   v.valid_min = np.float32(min_dat5)
   v.valid_max = np.float32(max_dat5)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(DD5)
   
   v = nc.createVariable('number_concentration_of_ambient_aerosol_particles_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'cm-3'
   v.standard_name = 'number_concentration_of_ambient_aerosol_particles_in_air'
   v.long_name = 'Number Concentration of Ambient Aerosol Particles in air'
   v.valid_min = np.float32(min_dat6)
   v.valid_max = np.float32(max_dat6)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(DD6) 

   v = nc.createVariable('qc_flag_pm1', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: PM1'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_pm1_outside_sensor_operational_range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(FL1)
   
   v = nc.createVariable('qc_flag_pm2p5', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: PM2.5'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_pm2.5_outside_sensor_operational_range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(FL2)
   
   v = nc.createVariable('qc_flag_pm4', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: PM4'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_pm4_outside_sensor_operational_range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(FL3)
   
   v = nc.createVariable('qc_flag_pm10', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: PM10'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_pm10_outside_sensor_operational_range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(FL4)
   
   v = nc.createVariable('qc_flag_total_pm', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Total PM'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_total_pm_outside_sensor_operational_range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(FL5)
   
   v = nc.createVariable('qc_flag_total_number', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Total Number'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_total_number_outside_sensor_operational_range' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(FL6)
   
# Q
# R
def radon_concentration(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data, flag, time
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.species1[data.st:data.ed]
      FL1 = data.flag1[data.st:data.ed]
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
      DD1 = data.species1[data.st[data.counter]:data.ed[data.counter]]
      FL1 = data.flag1[data.st[data.counter]:data.ed[data.counter]]
      
   # valid max and min values
   XX1 = np.array(DD1)
   np.putmask(XX1, FL1 != 1, np.nan)
   min_dat1 = np.float32(np.nanmin(XX1))
   max_dat1 = np.float32(np.nanmax(XX1))    
      
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('mole_fraction_of_radon_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit1
   v.practical_units = data.practical_units1
   v.standard_name = 'mole_fraction_of_radon_in_air'
   v.long_name = 'Mole Fraction of Radon in air'
   v.valid_min = np.float32(min_dat1)
   v.valid_max = np.float32(max_dat1)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'Rn'
   # write data
   v[:] = np.float32(DD1)
   
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_unspecified_instrument_performance_issues_contact_data_originator_for_more_information' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   # write data
   v[:] = np.int8(FL1)
   
# S
def sf6_concentration(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data, flag, time
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.species1[data.st:data.ed]
      FL1 = data.flag1[data.st:data.ed]
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
      DD1 = data.species1[data.st[data.counter]:data.ed[data.counter]]
      FL1 = data.flag1[data.st[data.counter]:data.ed[data.counter]]
      
   # valid max and min values
   XX1 = np.array(DD1)
   np.putmask(XX1, FL1 != 1, np.nan)
   min_dat1 = np.float32(np.nanmin(XX1))
   max_dat1 = np.float32(np.nanmax(XX1))    
      
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('mole_fraction_of_sulfur_hexafluoride_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit1
   v.practical_units = data.practical_units1
   v.long_name = 'Mole Fraction of Sulphur Hexafluoride in air'
   v.valid_min = np.float32(min_dat1)
   v.valid_max = np.float32(max_dat1)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'SF6'
   # write data
   v[:] = np.float32(DD1)
   
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_unspecified_instrument_performance_issues_contact_data_originator_for_more_information' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(FL1)
   
def so2_concentration(meta, data, nc):
   import WAO_common as com
   import numpy as np
   
   # data, flag, time
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.species1[data.st:data.ed]
      FL1 = data.flag1[data.st:data.ed]
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
      DD1 = data.species1[data.st[data.counter]:data.ed[data.counter]]
      FL1 = data.flag1[data.st[data.counter]:data.ed[data.counter]]
      
   # valid max and min values
   XX1 = np.array(DD1)
   np.putmask(XX1, FL1 != 1, np.nan)
   min_dat1 = np.float32(np.nanmin(XX1))
   max_dat1 = np.float32(np.nanmax(XX1))    
      
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('mole_fraction_of_sulfur_dioxide_in_air', np.float32, ('time',), fill_value=-1.00e+20)
   # variable attributes
   v.units = data.unit1
   v.practical_units = data.practical_units1
   v.standard_name = 'mole_fraction_of_sulfur_dioxide_in_air'
   v.long_name = 'Mole Fraction of Sulphur Dioxide in air'
   v.valid_min = np.float32(min_dat1)
   v.valid_max = np.float32(max_dat1)
   v.cell_methods = 'time: point'
   v.coordinates = 'latitude longitude'
   v.chemical_species = 'SO2'
   # write data
   v[:] = np.float32(DD1)
   
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   # variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_unspecified_instrument_performance_issues_contact_data_originator_for_more_information' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'  
   # write data
   v[:] = np.int8(FL1)

def surface_met1(meta, data, nc):
   #campbell radiation only
   import WAO_common as com
   import numpy as np
   
   # data, flag, time
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD3 = data.species3[data.st:data.ed] # species 3 IR
      DD4 = data.species4[data.st:data.ed] # species 4 Net IR
      FL3 = data.flag3[data.st:data.ed]
      FL4 = data.flag4[data.st:data.ed]
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
      DD3 = data.species3[data.st[data.counter]:data.ed[data.counter]] # species 3 IR
      DD4 = data.species4[data.st[data.counter]:data.ed[data.counter]] # species 4 Net IR
      FL3 = data.flag3[data.st[data.counter]:data.ed[data.counter]]
      FL4 = data.flag4[data.st[data.counter]:data.ed[data.counter]]
   
   # valid max and min values
   XX3 = np.array(DD3)
   np.putmask(XX3, FL3 != 1, np.nan)
   min_dat3 = np.float32(np.nanmin(XX3))
   max_dat3 = np.float32(np.nanmax(XX3))    
   
   XX4 = np.array(DD4)
   np.putmask(XX4, FL4 != 1, np.nan)
   min_dat4 = np.float32(np.nanmin(XX4))
   max_dat4 = np.float32(np.nanmax(XX4))  
      
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('downwelling_total_irradiance', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'W m-2'
   v.long_name = 'Downwelling Total Irradiance'
   v.valid_min = np.float32(min_dat3)
   v.valid_max = np.float32(max_dat3)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(DD3)
   
   v = nc.createVariable('net_total_irradiance', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'W m-2'
   v.long_name = 'Net Total Irradiance'
   v.valid_min = np.float32(min_dat4)
   v.valid_max = np.float32(max_dat4)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(DD4)
   
   v = nc.createVariable('qc_flag_downwelling_total_irradiance', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Downwelling Total Irradiance'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data<0Wm-2' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_exceeds_instrument_measurment_range_of_2000Wm-2'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'
   #write data
   v[:] = np.int8(FL3)
   
   v = nc.createVariable('qc_flag_net_total_irradiance', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Net Total Irradiance'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data<0Wm-2' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_exceeds_instrument_measurment_range_of_2000Wm-2'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error'
   #write data
   v[:] = np.int8(FL4)
   
def surface_met2(meta, data, nc):
   #metpak
   import WAO_common as com
   import numpy as np
   
   # data, flag, time
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
      DD1 = data.species1[data.st:data.ed] # species 1 RH
      DD2 = data.species2[data.st:data.ed] # species 2 TT
      DD5 = data.species5[data.st:data.ed] # species 5 WS
      DD6 = data.species6[data.st:data.ed] # species 6 WD
      DD7 = data.species7[data.st:data.ed] # species 7 PP
      FL1 = data.flag1[data.st:data.ed]
      FL2 = data.flag2[data.st:data.ed]
      FL5 = data.flag5[data.st:data.ed]
      FL6 = data.flag6[data.st:data.ed]
      FL7 = data.flag7[data.st:data.ed]
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
      DD1 = data.species1[data.st[data.counter]:data.ed[data.counter]] # species 1 RH
      DD2 = data.species2[data.st[data.counter]:data.ed[data.counter]] # species 2 TT
      DD5 = data.species5[data.st[data.counter]:data.ed[data.counter]] # species 5 WS
      DD6 = data.species6[data.st[data.counter]:data.ed[data.counter]] # species 6 WD
      DD7 = data.species7[data.st[data.counter]:data.ed[data.counter]] # species 7 PP
      FL1 = data.flag1[data.st[data.counter]:data.ed[data.counter]]
      FL2 = data.flag2[data.st[data.counter]:data.ed[data.counter]]
      FL5 = data.flag5[data.st[data.counter]:data.ed[data.counter]]
      FL6 = data.flag6[data.st[data.counter]:data.ed[data.counter]]
      FL7 = data.flag7[data.st[data.counter]:data.ed[data.counter]]
     
   # valid max and min values
   XX1 = np.array(DD1)
   np.putmask(XX1, FL1 != 1, np.nan)
   min_dat1 = np.float32(np.nanmin(XX1))
   max_dat1 = np.float32(np.nanmax(XX1))    
   
   XX2 = np.array(DD2)
   np.putmask(XX2, FL2 != 1, np.nan)
   min_dat2 = np.float32(np.nanmin(XX2))
   max_dat2 = np.float32(np.nanmax(XX2)) 

   XX5 = np.array(DD5)
   np.putmask(XX5, FL5 != 1, np.nan)
   min_dat5 = np.float32(np.nanmin(XX5))
   max_dat5 = np.float32(np.nanmax(XX5))    
   
   XX6 = np.array(DD6)
   np.putmask(XX6, FL6 != 1, np.nan)
   min_dat6 = np.float32(np.nanmin(XX6))
   max_dat6 = np.float32(np.nanmax(XX6)) 

   XX7 = np.array(DD7)
   np.putmask(XX7, FL7 != 1, np.nan)
   min_dat7 = np.float32(np.nanmin(XX7))
   max_dat7 = np.float32(np.nanmax(XX7))   
      
   # write common global attrib 
   com.global_attributes(nc, meta, ET)
   
   # write specific global attrib
   nc.product_version = ' '.join(map(str, data.ver))
      
   # write common dimensions
   com.dimensions(nc, ET)
   
   # write common variables
   com.variables(nc, data)
 
   # write specific variables
   v = nc.createVariable('air_pressure', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'hPa'
   v.standard_name = 'air_pressure'
   v.long_name = 'Air Pressure'
   v.valid_min = np.float32(min_dat7)
   v.valid_max = np.float32(max_dat7)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(DD7) 
   
   v = nc.createVariable('air_temperature', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'K'
   v.standard_name = 'air_temperature'
   v.long_name = 'Air Temperature'
   v.valid_min = np.float32(min_dat2)
   v.valid_max = np.float32(max_dat2)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(DD2)
   
   v = nc.createVariable('relative_humidity', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = '%'
   v.standard_name = 'relative_humidity'
   v.long_name = 'Relative Humidity'
   v.valid_min = np.float32(min_dat1)
   v.valid_max = np.float32(max_dat1)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(DD1)
   
   v = nc.createVariable('wind_speed', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.standard_name = 'wind_speed'
   v.long_name = 'Wind Speed'
   v.valid_min = np.float32(min_dat5)
   v.valid_max = np.float32(max_dat5)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(DD5)
   
   v = nc.createVariable('wind_from_direction', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'degree'
   v.standard_name = 'wind_from_direction'
   v.long_name = 'Wind From Direction'
   v.valid_min = np.float32(min_dat6)
   v.valid_max = np.float32(max_dat6)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(DD6)
   
   v = nc.createVariable('qc_flag_temperature', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Temperature'
   v.flag_values = '0b,1b,2b,3b,4b,5b,6b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_below_measurement_threshold_of_50C' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_above_measurement_threshold_of_100C' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:T<_-20C_and_T>-50C' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:T>_40C_and_T<100C' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(FL2)  
   
   v = nc.createVariable('qc_flag_relative_humidity', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Relative Humidity'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_below_measurement_threshold_of_0%' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_above_measurement_threshold_of_100%' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(FL1)
   
   v = nc.createVariable('qc_flag_pressure', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Pressure'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_below_measurement_threshold_of_600hPa' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_above_measurement_threshold_of_11000hPa' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(FL7)
   
   v = nc.createVariable('qc_flag_wind_speed', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Wind Speed'
   v.flag_values = '0b,1b,2b,3b,4b,5b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_below_measurement_threshold_of_0ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_above_measurement_threshold_of_60ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:data=0ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(FL5)
   
   v = nc.createVariable('qc_flag_wind_from_direction', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Wind From Direction'
   v.flag_values = '0b,1b,2b,3b,4b,5b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_below_measurement_threshold_of_0degrees' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_above_measurement_threshold_of_359degrees' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:windspeed=0ms-1_so_direction_cannot_be_determined' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(FL6)  