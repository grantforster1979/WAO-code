def global_attributes(nc, meta, ET):
   from datetime import datetime
  
   for x in range(0,len(meta[:,0])):
      nc.setncattr(meta[x,0], meta[x,1])
   
   # write specific global attribute
   nc.last_revised_date = datetime.utcnow().isoformat()  
   nc.time_coverage_start = datetime.utcfromtimestamp(ET[0]).isoformat()
   nc.time_coverage_end = datetime.utcfromtimestamp(ET[len(ET)-1]).isoformat()
   del datetime
      
def dimensions(nc, ET):
   time = nc.createDimension('time', len(ET))
   latitude = nc.createDimension('latitude', 1)
   longitude = nc.createDimension('longitude', 1)
   
def variables(nc, data):
   import numpy as np
   
   # ET
   if data.counter == -1: #single day month or year
      ET = data.ET[data.st:data.ed]
   else: # part of a multi file loop
      ET = data.ET[data.st[data.counter]:data.ed[data.counter]]
   # DoY
   if data.counter == -1: #single day month or year
      DoY = data.DoY[data.st:data.ed]
   else: # part of a multi file loop
      DoY = data.DoY[data.st[data.counter]:data.ed[data.counter]]
   # DT
   if data.counter == -1: #single day month or year
      DT = data.DT[data.st:data.ed,:]
   else: # part of a multi file loop
      DT = data.DT[data.st[data.counter]:data.ed[data.counter],:]
       
   #time
   v = nc.createVariable('time', np.float64, ('time',))
   #variable attributes
   v.units = 'seconds since 1970-01-01 00:00:00'
   v.standard_name = 'time'
   v.long_name = 'Time (seconds since 1970-01-01 00:00:00)'
   v.axis = 'T'
   v.valid_min = np.float64(min(ET))
   v.valid_max = np.float64(max(ET))
   v.calendar = 'standard'
   #write data
   v[:] = np.float64(ET)

   #lat
   v = nc.createVariable('latitude', np.float32, ('latitude',))
   #variable attributes
   v.units = 'degrees_north'
   v.standard_name = 'latitude'
   v.long_name = 'Latitude'
   #write data
   v[:] = np.float32(data.lat)
   
   #lon
   v = nc.createVariable('longitude', np.float32, ('longitude',))
   #variable attributes
   v.units = 'degrees_east'
   v.standard_name = 'longitude'
   v.long_name = 'Longitude'
   #write data
   v[:] = np.float32(data.lon)
   
   #doy
   v = nc.createVariable('day_of_year', np.float32, ('time',))
   #variable attributes
   v.units = '1'
   v.long_name = 'Day of Year'
   v.valid_min = np.float32(min(DoY))
   v.valid_max = np.float32(max(DoY))
   #write data
   v[:] = np.float32(DoY)
   
   #year
   v = nc.createVariable('year', np.int32, ('time',))
   #variable attributes
   v.units = '1'
   v.long_name = 'Year'
   v.valid_min = np.int32(min(DT[:,0]))
   v.valid_max = np.int32(max(DT[:,0])) 
   #write data
   v[:] = np.int32(DT[:,0])
   
   #month
   v = nc.createVariable('month', np.int32, ('time',))
   #variable attributes
   v.units = '1'
   v.long_name = 'Month'
   v.valid_min = np.int32(min(DT[:,1]))
   v.valid_max = np.int32(max(DT[:,1])) 
   #write data
   v[:] = np.int32(DT[:,1])
   
   #day
   v = nc.createVariable('day', np.int32, ('time',))
   #variable attributes
   v.units = '1'
   v.long_name = 'Day'
   v.valid_min = np.int32(min(DT[:,2]))
   v.valid_max = np.int32(max(DT[:,2]))
   #write data
   v[:] = np.int32(DT[:,2])
   
   #hour
   v = nc.createVariable('hour', np.int32, ('time',))
   #variable attributes
   v.units = '1'
   v.long_name = 'Hour'
   v.valid_min = np.int32(min(DT[:,3]))
   v.valid_max = np.int32(max(DT[:,3])) 
   #write data
   v[:] = np.int32(DT[:,3])
   
   #minute
   v = nc.createVariable('minute', np.int32, ('time',))
   #variable attributes
   v.units = '1'
   v.long_name = 'Minute'
   v.valid_min = np.int32(min(DT[:,4]))
   v.valid_max = np.int32(max(DT[:,4]))  
   #write data
   v[:] = np.int32(DT[:,4])
   
   #second
   v = nc.createVariable('second', np.float32, ('time',))
   #variable attributes
   v.units = '1'
   v.long_name = 'Second'
   v.valid_min = np.float32(min(DT[:,5]))
   v.valid_max = np.float32(max(DT[:,5])) 
   #write data
   v[:] = np.float32(DT[:,5])
   
   del np