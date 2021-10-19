def ncas_ceilometer_2(config, data, logfile):
   import numpy as np
   import WAO_ceilometer as WAOC

   #parse the data  
   data = WAOC.ceil_parse(config, data)      
   
   return data
         
def ncas_co2_1(config, data, logfile): 
   import pandas as pd
   import numpy as np
   import time
   import os
   from datetime import datetime
   import calendar   
   
   fn = os.path.normpath(str(config[5]).strip('[]'))
   fn = fn[1:len(fn)-1] 
   try:
      df = pd.read_csv(fn)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn , ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   #remove any nans from data
   
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
 
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   data.species1 = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X1 <= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   data.species1 = X1
   
   if 'ppm' in header[1]:
      data.unit1 = '1e-6'
      data.practical_units1 = 'ppm'
   if 'ppb' in header[1]:
      data.unit1 = '1e-9'
      data.practical_units1 = 'ppb'
   if 'ppt' in header[1]:
      data.unit1 = '1e-12'
      data.practical_units1 = 'ppt'
   
   data.ET = np.array(ET)
   data.DT = np.array(DT)
   data.DoY = np.array(DoY)
   
   return data    
         
def ncas_ftir_1(config, data, logfile): 
   import pandas as pd
   import numpy as np
   import time
   import os
   from datetime import datetime
   import calendar   
   
   fn = os.path.normpath(str(config[5]).strip('[]'))
   fn = fn[1:len(fn)-1] 
   
   try:
      df = pd.read_csv(fn)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn , ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
     
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   df[header[3]].fillna(-1.00e+20, inplace = True) 
   df[header[5]].fillna(-1.00e+20, inplace = True) 
   df[header[7]].fillna(-1.00e+20, inplace = True) 
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   X2 = np.array(df.loc[:, header[3]:header[3]:1].values)
   data.flag2 = np.array(df.loc[:, header[4]:header[4]:1].values)
   X3 = np.array(df.loc[:, header[5]:header[5]:1].values)
   data.flag3 = np.array(df.loc[:, header[6]:header[6]:1].values)
   X4 = np.array(df.loc[:, header[7]:header[7]:1].values)
   data.flag4 = np.array(df.loc[:, header[8]:header[8]:1].values)
   
   data.species1 = np.array([])
   data.species2 = np.array([])
   data.species3 = np.array([])
   data.species4 = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X1 <= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   
   ii = np.where(X2 <= 0)
   data.flag2[ii] = 2
   ii = np.where(X2 > 9000)
   data.flag2[ii] = 3
   
   ii = np.where(X3 <= 0)
   data.flag3[ii] = 2
   ii = np.where(X3 > 9000)
   data.flag3[ii] = 3
   
   ii = np.where(X4 <= 0)
   data.flag4[ii] = 2
   ii = np.where(X4 > 9000)
   data.flag4[ii] = 3
          
   data.species1 = X1
   if 'pp' in header[1]:
      if 'ppm' in header[1]:
         data.unit1 = '1e-6'
         data.practical_units1 = 'ppm'
      if 'ppb' in header[1]:
         data.unit1 = '1e-9'
         data.practical_units1 = 'ppb'
      if 'ppt' in header[1]:
         data.unit1 = '1e-12'
         data.practical_units1 = 'ppt'
   
   data.species2 = X2      
   if 'pp' in header[3]:
      if 'ppm' in header[3]:
         data.unit2 = '1e-6'
         data.practical_units2 = 'ppm'
      if 'ppb' in header[3]:
         data.unit2 = '1e-9'
         data.practical_units2 = 'ppb'
      if 'ppt' in header[3]:
         data.unit2 = '1e-12'
         data.practical_units2 = 'ppt'
  
   data.species3 = X3        
   if 'pp' in header[5]:
      if 'ppm' in header[5]:
         data.unit3 = '1e-6'
         data.practical_units3 = 'ppm'
      if 'ppb' in header[5]:
         data.unit3 = '1e-9'
         data.practical_units3 = 'ppb'
      if 'ppt' in header[5]:
         data.unit3 = '1e-12'
         data.practical_units3 = 'ppt'
         
   data.species4 = X4     
   if 'pp' in header[7]:
      if 'ppm' in header[7]:
         data.unit4 = '1e-6'
         data.practical_units4 = 'ppm'
      if 'ppb' in header[7]:
         data.unit4 = '1e-9'
         data.practical_units4 = 'ppb'
      if 'ppt' in header[7]:
         data.unit4 = '1e-12'
         data.practical_units4 = 'ppt'
 
   return data 
         
def ncas_ghg_gc_fid_1(config, data, logfile): 
   import pandas as pd
   import numpy as np
   import time
   import os
   from datetime import datetime
   import calendar   
   
   fn = os.path.normpath(str(config[5]).strip('[]'))
   fn = fn[1:len(fn)-1] 
   
   try:
      df = pd.read_csv(fn)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn , ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   
   data.species1 = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X1 <= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   
   data.species1 = X1        
   if 'pp' in header[1]:
      if 'ppm' in header[1]:
         data.unit1 = '1e-6'
         data.practical_units1 = 'ppm'
      if 'ppb' in header[1]:
         data.unit1 = '1e-9'
         data.practical_units1 = 'ppb'
      if 'ppt' in header[1]:
         data.unit1 = '1e-12'
         data.practical_units1 = 'ppt'
   
   return data 

def ncas_ghg_gc_ecd_1(config, data, logfile): 
   import pandas as pd
   import numpy as np
   import time
   import os
   from datetime import datetime
   import calendar   
   
   fn = os.path.normpath(str(config[5]).strip('[]'))
   fn = fn[1:len(fn)-1] 
   
   try:
      df = pd.read_csv(fn)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn , ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
 
   # this code has to be able to read in two different types of file
   # sf6 only header has length 3
   # n20 and sf6 header has length 5
   
   # remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   if len(header) == 5:
      df[header[3]].fillna(-1.00e+20, inplace = True)
      
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   if len(header) == 5:
      X2 = np.array(df.loc[:, header[3]:header[3]:1].values)
      data.flag2 = np.array(df.loc[:, header[4]:header[4]:1].values)
   
   data.species1 = np.array([])
   if len(header) == 5:
      data.species2 = np.array([])
   
   # flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X1 <= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   if len(header) == 5:
      # flag any data < 0 cannot have a -'ve gas concentration
      ii = np.where(X2 <= 0)
      data.flag2[ii] = 2
      ii = np.where(X2 > 9000)
      data.flag2[ii] = 3
   
   data.species1 = X1   
   if 'pp' in header[1]:
      if 'ppm' in header[1]:
         data.unit1 = '1e-6'
         data.practical_units1 = 'ppm'
      if 'ppb' in header[1]:
         data.unit1 = '1e-9'
         data.practical_units1 = 'ppb'
      if 'ppt' in header[1]:
         data.unit1 = '1e-12'
         data.practical_units1 = 'ppt'
      
   if len(header) == 5:  
      data.species2 = X2      
      if 'pp' in header[3]:
         if 'ppm' in header[3]:
            data.unit2 = '1e-6'
            data.practical_units2 = 'ppm'
         if 'ppb' in header[3]:
            data.unit2 = '1e-9'
            data.practical_units2 = 'ppb'
         if 'ppt' in header[3]:
            data.unit2 = '1e-12'
            data.practical_units2 = 'ppt'  
   return data 
         
def ncas_o2_1(config, data, logfile): 
   import pandas as pd
   import numpy as np
   import time
   import os
   from datetime import datetime
   import calendar   
   
   fn = os.path.normpath(str(config[5]).strip('[]'))
   fn = fn[1:len(fn)-1] 
   
   try:
      df = pd.read_csv(fn)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn , ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   
   data.species1 = np.array(X1)
   
   # -'ve data here is valid
   ii = np.where(X1 >= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   
   return data

def ncas_rga3_1(config, data, logfile): 
   import pandas as pd
   import numpy as np
   import time
   import os
   from datetime import datetime
   import calendar   
   
   fn = os.path.normpath(str(config[5]).strip('[]'))
   fn = fn[1:len(fn)-1] 
   
   try:
      df = pd.read_csv(fn)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn , ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   # this code has to be able to read in two different types of file
   # h2 and co header has length 5
   # h2 only header has length 3
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   if len(header) == 5:
      df[header[3]].fillna(-1.00e+20, inplace = True)
      
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   if len(header) == 5:
      X2 = np.array(df.loc[:, header[3]:header[3]:1].values)
      data.flag2 = np.array(df.loc[:, header[4]:header[4]:1].values)
   
   data.species1 = np.array([])
   if len(header) == 5:
      data.species2 = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X1 <= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   if len(header) == 5:
      #flag any data < 0 cannot have a -'ve gas concentration
      ii = np.where(X1 <= 0)
      data.flag2[ii] = 2
      ii = np.where(X1 > 9000)
      data.flag2[ii] = 3
   
   data.species1 = X1   
   if 'pp' in header[1]:
      if 'ppm' in header[1]:
         data.unit1 = '1e-6'
         data.practical_units1 = 'ppm'
      if 'ppb' in header[1]:
         data.unit1 = '1e-9'
         data.practical_units1 = 'ppb'
      if 'ppt' in header[1]:
         data.unit1 = '1e-12'
         data.practical_units1 = 'ppt'
      
   if len(header) == 5:  
      data.species2 = X2         
      if 'pp' in header[3]:
         if 'ppm' in header[3]:
            data.unit2 = '1e-6'
            data.practical_units2 = 'ppm'
         if 'ppb' in header[3]:
            data.unit2 = '1e-9'
            data.practical_units2 = 'ppb'
         if 'ppt' in header[3]:
            data.unit2 = '1e-12'
            data.practical_units2 = 'ppt'
   
   return data 
        
def uea_42i_nox_1(config, data, logfile): 
   import pandas as pd
   import numpy as np
   import time
   import os
   from datetime import datetime
   import calendar   
   
   fn = os.path.normpath(str(config[5]).strip('[]'))
   fn = fn[1:len(fn)-1] 
   
   try:
      df = pd.read_csv(fn)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn , ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)

   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   df[header[3]].fillna(-1.00e+20, inplace = True) 
   df[header[5]].fillna(-1.00e+20, inplace = True) 
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   X2 = np.array(df.loc[:, header[3]:header[3]:1].values)
   data.flag2 = np.array(df.loc[:, header[4]:header[4]:1].values)
   X3 = np.array(df.loc[:, header[5]:header[5]:1].values)
   data.flag3 = np.array(df.loc[:, header[6]:header[6]:1].values)
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X1 <= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   
   ii = np.where(X2 <= 0)
   data.flag2[ii] = 2
   ii = np.where(X2 > 9000)
   data.flag2[ii] = 3
   
   ii = np.where(X3 <= 0)
   data.flag3[ii] = 2
   ii = np.where(X3 > 9000)
   data.flag3[ii] = 3
   
   data.species1 = np.array([])
   data.species2 = np.array([])
   data.species3 = np.array([])
  
   data.species1 = X1  
   if 'pp' in header[1]:
      if 'ppm' in header[1]:
         data.unit1 = '1e-6'
         data.practical_units1 = 'ppm'
      if 'ppb' in header[1]:
         data.unit1 = '1e-9'
         data.practical_units1 = 'ppb'
      if 'ppt' in header[1]:
         data.unit1 = '1e-12'
         data.practical_units1 = 'ppt'
   
   data.species2 = X2        
   if 'pp' in header[3]:
      if 'ppm' in header[3]:
         data.unit2 = '1e-6'
         data.practical_units2 = 'ppm'
      if 'ppb' in header[3]:
         data.unit2 = '1e-9'
         data.practical_units2 = 'ppb'
      if 'ppt' in header[3]:
         data.unit2 = '1e-12'
         data.practical_units2 = 'ppt'
   
   data.species3 = X3   
   if 'pp' in header[5]:
      data.mass_frac3 = X3
      if 'ppm' in header[5]:
         data.unit3 = '1e-6'
         data.practical_units3 = 'ppm'
      if 'ppb' in header[5]:
         data.unit3 = '1e-9'
         data.practical_units3 = 'ppb'
      if 'ppt' in header[5]:
         data.unit3 = '1e-12'
         data.practical_units3 = 'ppt'

   return data    
         
def uea_43i_so2_1(config, data, logfile):
   import pandas as pd
   import numpy as np
   import time
   import os
   from datetime import datetime
   import calendar   
   
   fn = os.path.normpath(str(config[5]).strip('[]'))
   fn = fn[1:len(fn)-1] 
   
   try:
      df = pd.read_csv(fn)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn , ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   
   data.species1 = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X1 <= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   
   data.species1 = X1       
   if 'pp' in header[1]:
      if 'ppm' in header[1]:
         data.unit1 = '1e-6'
         data.practical_units1 = 'ppm'
      if 'ppb' in header[1]:
         data.unit1 = '1e-9'
         data.practical_units1 = 'ppb'
      if 'ppt' in header[1]:
         data.unit1 = '1e-12'
         data.practical_units1 = 'ppt'
   
   return data 
      
def uea_49i_o3_1(config, data, logfile):
   import pandas as pd
   import numpy as np
   import time
   import os
   from datetime import datetime
   import calendar   
   
   fn = os.path.normpath(str(config[5]).strip('[]'))
   fn = fn[1:len(fn)-1] 
   
   try:
      df = pd.read_csv(fn)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn , ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   
   data.species1 = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X1 <= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   
   data.species1 = X1     
   if 'pp' in header[1]:
      if 'ppm' in header[1]:
         data.unit1 = '1e-6'
         data.practical_units1 = 'ppm'
      if 'ppb' in header[1]:
         data.unit1 = '1e-9'
         data.practical_units1 = 'ppb'
      if 'ppt' in header[1]:
         data.unit1 = '1e-12'
         data.practical_units1 = 'ppt'
   
   return data 
   
def uea_t200up_1(config, data, logfile): 
   import pandas as pd
   import numpy as np
   import time
   import os
   from datetime import datetime
   import calendar   
   
   fn = os.path.normpath(str(config[5]).strip('[]'))
   fn = fn[1:len(fn)-1] 
   
   try:
      df = pd.read_csv(fn)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn , ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)

   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   df[header[3]].fillna(-1.00e+20, inplace = True) 
   df[header[5]].fillna(-1.00e+20, inplace = True) 
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   X2 = np.array(df.loc[:, header[3]:header[3]:1].values)
   data.flag2 = np.array(df.loc[:, header[4]:header[4]:1].values)
   X3 = np.array(df.loc[:, header[5]:header[5]:1].values)
   data.flag3 = np.array(df.loc[:, header[6]:header[6]:1].values)
   
   #flag any data < -1 NOx can have a slightly negative concentration as sometime we float around zero
   ii = np.where(X1 <= -1)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   
   ii = np.where(X2 <= -1)
   data.flag2[ii] = 2
   ii = np.where(X2 > 9000)
   data.flag2[ii] = 3
   
   ii = np.where(X3 <= -1)
   data.flag3[ii] = 2
   ii = np.where(X3 > 9000)
   data.flag3[ii] = 3
   
   data.species1 = np.array([])
   data.species2 = np.array([])
   data.species3 = np.array([])
  
   data.species1 = X1  
   if 'pp' in header[1]:
      if 'ppm' in header[1]:
         data.unit1 = '1e-6'
         data.practical_units1 = 'ppm'
      if 'ppb' in header[1]:
         data.unit1 = '1e-9'
         data.practical_units1 = 'ppb'
      if 'ppt' in header[1]:
         data.unit1 = '1e-12'
         data.practical_units1 = 'ppt'
   
   data.species2 = X2        
   if 'pp' in header[3]:
      if 'ppm' in header[3]:
         data.unit2 = '1e-6'
         data.practical_units2 = 'ppm'
      if 'ppb' in header[3]:
         data.unit2 = '1e-9'
         data.practical_units2 = 'ppb'
      if 'ppt' in header[3]:
         data.unit2 = '1e-12'
         data.practical_units2 = 'ppt'
   
   data.species3 = X3   
   if 'pp' in header[5]:
      data.mass_frac3 = X3
      if 'ppm' in header[5]:
         data.unit3 = '1e-6'
         data.practical_units3 = 'ppm'
      if 'ppb' in header[5]:
         data.unit3 = '1e-9'
         data.practical_units3 = 'ppb'
      if 'ppt' in header[5]:
         data.unit3 = '1e-12'
         data.practical_units3 = 'ppt'

   return data 

def uea_t200up_2(config, data, logfile): 
   import pandas as pd
   import numpy as np
   import time
   import os
   from datetime import datetime
   import calendar   
   
   fn = os.path.normpath(str(config[5]).strip('[]'))
   fn = fn[1:len(fn)-1] 
   
   try:
      df = pd.read_csv(fn)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn , ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)

   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   df[header[3]].fillna(-1.00e+20, inplace = True) 
   df[header[5]].fillna(-1.00e+20, inplace = True) 
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   X2 = np.array(df.loc[:, header[3]:header[3]:1].values)
   data.flag2 = np.array(df.loc[:, header[4]:header[4]:1].values)
   X3 = np.array(df.loc[:, header[5]:header[5]:1].values)
   data.flag3 = np.array(df.loc[:, header[6]:header[6]:1].values)
   
   #flag any data < -1 NOx can have a slightly negative concentration as sometime we float around zero
   ii = np.where(X1 <= -1)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   
   ii = np.where(X2 <= -1)
   data.flag2[ii] = 2
   ii = np.where(X2 > 9000)
   data.flag2[ii] = 3
   
   ii = np.where(X3 <= -1)
   data.flag3[ii] = 2
   ii = np.where(X3 > 9000)
   data.flag3[ii] = 3
   
   data.species1 = np.array([])
   data.species2 = np.array([])
   data.species3 = np.array([])
  
   data.species1 = X1  
   if 'pp' in header[1]:
      if 'ppm' in header[1]:
         data.unit1 = '1e-6'
         data.practical_units1 = 'ppm'
      if 'ppb' in header[1]:
         data.unit1 = '1e-9'
         data.practical_units1 = 'ppb'
      if 'ppt' in header[1]:
         data.unit1 = '1e-12'
         data.practical_units1 = 'ppt'
   
   data.species2 = X2        
   if 'pp' in header[3]:
      if 'ppm' in header[3]:
         data.unit2 = '1e-6'
         data.practical_units2 = 'ppm'
      if 'ppb' in header[3]:
         data.unit2 = '1e-9'
         data.practical_units2 = 'ppb'
      if 'ppt' in header[3]:
         data.unit2 = '1e-12'
         data.practical_units2 = 'ppt'
   
   data.species3 = X3   
   if 'pp' in header[5]:
      data.mass_frac3 = X3
      if 'ppm' in header[5]:
         data.unit3 = '1e-6'
         data.practical_units3 = 'ppm'
      if 'ppb' in header[5]:
         data.unit3 = '1e-9'
         data.practical_units3 = 'ppb'
      if 'ppt' in header[5]:
         data.unit3 = '1e-12'
         data.practical_units3 = 'ppt'

   return data          
         
def uea_aws_1and2(config, data, logfile):
   import pandas as pd
   import numpy as np
   import time
   import os
   from datetime import datetime
   import calendar   
   
   fn = os.path.normpath(str(config[5]).strip('[]'))
   fn = fn[1:len(fn)-1] 
   
   try:
      df = pd.read_csv(fn)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn , ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   df[header[3]].fillna(-1.00e+20, inplace = True) 
   df[header[5]].fillna(-1.00e+20, inplace = True) 
   df[header[7]].fillna(-1.00e+20, inplace = True) 
   df[header[9]].fillna(-1.00e+20, inplace = True) 
   df[header[11]].fillna(-1.00e+20, inplace = True) 
   df[header[13]].fillna(-1.00e+20, inplace = True)
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   X2 = np.array(df.loc[:, header[3]:header[3]:1].values)
   data.flag2 = np.array(df.loc[:, header[4]:header[4]:1].values)
   X3 = np.array(df.loc[:, header[5]:header[5]:1].values)
   data.flag3 = np.array(df.loc[:, header[6]:header[6]:1].values)
   X4 = np.array(df.loc[:, header[7]:header[7]:1].values)
   data.flag4 = np.array(df.loc[:, header[8]:header[8]:1].values)
   X5 = np.array(df.loc[:, header[9]:header[9]:1].values)
   data.flag5 = np.array(df.loc[:, header[10]:header[10]:1].values)
   X6 = np.array(df.loc[:, header[11]:header[11]:1].values)
   data.flag6 = np.array(df.loc[:, header[12]:header[12]:1].values)
   X7 = np.array(df.loc[:, header[13]:header[13]:1].values)
   data.flag7 = np.array(df.loc[:, header[14]:header[14]:1].values)
   
   data.species1 = np.array([])
   data.species2 = np.array([])
   data.species3 = np.array([])
   data.species4 = np.array([])
   data.species5 = np.array([])
   data.species6 = np.array([])
   data.species7 = np.array([])
   
   # RH
   ii = np.where(X1 <= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 100)
   data.flag1[ii] = 3
   # Temperature
   ii = np.where(X2 <= -50)
   data.flag2[ii] = 2
   ii = np.where(X2 > 100)
   data.flag2[ii] = 3
   ii = np.where((X2 > -50) & (X1 < -20))
   data.flag2[ii] = 4
   ii = np.where((X2 > 40) & (X1 < 100))
   data.flag2[ii] = 5
   # Irradiance
   ii = np.where(X3 < 0)
   data.flag3[ii] = 2
   ii = np.where(X3 > 1000)
   data.flag3[ii] = 3
   # Net irradiance
   ii = np.where(X4 < -1000)
   data.flag4[ii] = 2
   ii = np.where(X4 > 1000)
   data.flag4[ii] = 3
   # Wind speed
   ii = np.where(X5 < 0)
   data.flag5[ii] = 2
   ii = np.where(X5 > 60)
   data.flag5[ii] = 3
   ii = np.where(X5 == 0)
   data.flag5[ii] = 4
   data.flag6[ii] = 4
   # Wind direction
   ii = np.where(X6 < 0)
   data.flag6[ii] = 2
   ii = np.where(X6 > 359)
   data.flag6[ii] = 3
   # Pressure
   ii = np.where(X7 <= 600)
   data.flag7[ii] = 2
   ii = np.where(X7 > 11000)
   data.flag7[ii] = 3
   
   data.species1 = np.float32(X1) # RH
   data.species2 = np.float32(X2) + 273.15 # TT
   data.species3 = np.float32(X3) # IR
   data.species4 = np.float32(X4) # net IR
   data.species5 = np.float32(X5) # WS
   data.species6 = np.float32(X6) # WD
   data.species7 = np.float32(X7) # PP
   
   return data      

def uea_caps_1(config, data, logfile):
   import pandas as pd
   import numpy as np
   import time
   import os
   from datetime import datetime
   import calendar   
   
   fn = os.path.normpath(str(config[5]).strip('[]'))
   fn = fn[1:len(fn)-1] 
   
   try:
      df = pd.read_csv(fn)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn , ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   
   data.species1 = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X1 <= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   
   data.species1 = X1       
   if 'pp' in header[1]:
      if 'ppm' in header[1]:
         data.unit1 = '1e-6'
         data.practical_units1 = 'ppm'
      if 'ppb' in header[1]:
         data.unit1 = '1e-9'
         data.practical_units1 = 'ppb'
      if 'ppt' in header[1]:
         data.unit1 = '1e-12'
         data.practical_units1 = 'ppt'
   
   return data 
         
def uea_fidas200E_1(config, data, logfile):
   import pandas as pd
   import numpy as np
   import time
   import os
   from datetime import datetime
   import calendar   
   
   fn = os.path.normpath(str(config[5]).strip('[]'))
   fn = fn[1:len(fn)-1] 
   
   try:
      df = pd.read_csv(fn)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn , ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   df[header[3]].fillna(-1.00e+20, inplace = True) 
   df[header[5]].fillna(-1.00e+20, inplace = True) 
   df[header[7]].fillna(-1.00e+20, inplace = True) 
   df[header[9]].fillna(-1.00e+20, inplace = True) 
   df[header[11]].fillna(-1.00e+20, inplace = True) 
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   X2 = np.array(df.loc[:, header[3]:header[3]:1].values)
   data.flag2 = np.array(df.loc[:, header[4]:header[4]:1].values)
   X3 = np.array(df.loc[:, header[5]:header[5]:1].values)
   data.flag3 = np.array(df.loc[:, header[6]:header[6]:1].values)
   X4 = np.array(df.loc[:, header[7]:header[7]:1].values)
   data.flag4 = np.array(df.loc[:, header[8]:header[8]:1].values)
   X5 = np.array(df.loc[:, header[9]:header[9]:1].values)
   data.flag5 = np.array(df.loc[:, header[10]:header[10]:1].values)
   X6 = np.array(df.loc[:, header[11]:header[11]:1].values)
   data.flag6 = np.array(df.loc[:, header[12]:header[12]:1].values)
   
   data.species1 = np.array([])
   data.species2 = np.array([])
   data.species3 = np.array([])
   data.species4 = np.array([])
   data.species5 = np.array([])
   data.species6 = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X1 <= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   
   ii = np.where(X2 <= 0)
   data.flag2[ii] = 2
   ii = np.where(X2 > 9000)
   data.flag2[ii] = 3
   
   ii = np.where(X3 <= 0)
   data.flag3[ii] = 2
   ii = np.where(X3 > 9000)
   data.flag3[ii] = 3
   
   ii = np.where(X4 <= 0)
   data.flag4[ii] = 2
   ii = np.where(X4 > 9000)
   data.flag4[ii] = 3
   
   ii = np.where(X5 <= 0)
   data.flag5[ii] = 2
   ii = np.where(X5 > 9000)
   data.flag5[ii] = 3
   
   ii = np.where(X6 <= 0)
   data.flag6[ii] = 2
   ii = np.where(X6 > 9000)
   data.flag6[ii] = 3
   
   data.species1 = X1 #pm1
   data.species2 = X2 #pm2.5
   data.species3 = X3 #pm4
   data.species4 = X4 #pm10
   data.species5 = X5 #pc
   data.species6 = X6 #tsp
   
   return data
          
def uea_radon_1(config, data, logfile):
   import pandas as pd
   import numpy as np
   import time
   import os
   from datetime import datetime
   import calendar   
   
   fn = os.path.normpath(str(config[5]).strip('[]'))
   fn = fn[1:len(fn)-1] 
   
   try:
      df = pd.read_csv(fn)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn , ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn + 'Program will terminate.\n')
      g.close()
      exit()
    
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%d/%m/%Y %H:%M:%S']")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6])
   
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
   
   #remove any nans from data
   df[header[1]].fillna(-1.00e+20, inplace = True) 
   
   X1 = np.array(df.loc[:, header[1]:header[1]:1].values)
   data.flag1 = np.array(df.loc[:, header[2]:header[2]:1].values)
   
   data.species1 = np.array([])
   
   #flag any data < 0 cannot have a -'ve gas concentration
   ii = np.where(X1 <= 0)
   data.flag1[ii] = 2
   ii = np.where(X1 > 9000)
   data.flag1[ii] = 3
   
   data.species1 = X1   
   if 'pp' in header[1]:
      if 'ppm' in header[1]:
         data.unit1 = '1e-6'
         data.practical_units1 = 'ppm'
      if 'ppb' in header[1]:
         data.unit1 = '1e-9'
         data.practical_units1 = 'ppb'
      if 'ppt' in header[1]:
         data.unit1 = '1e-12'
         data.practical_units1 = 'ppt'
   
   return data 
         
def uea_sodar_rass_1(config, data, logfile):
   import numpy as np
   import WAO_sodar as WAOC

   #parse the data  
   data = WAOC.sodar_parse(config, data)      
   
   return data
   
def data_chunker(config, data, logfile):  
   import numpy as np

   st = []; ed = [] # holding array for start and stop points

   # all data
   if config[2] == 'all':
      # year long files
      if config[1] == 'year':
         st.append(0)
         for n in range (1, len(data.ET)):
            if data.DT[n, 0] != data.DT[n-1, 0]:
               st.append(n)
               ed.append(n)
         if len(st) != len(ed):
            ed.append(len(data.ET))   
      # month long files
      if config[1] == 'month':
         st.append(0)
         for n in range (1, len(data.ET)):
            if data.DT[n, 1] != data.DT[n-1, 1]:
               st.append(n)
               ed.append(n)
         if len(st) != len(ed):
            ed.append(len(data.ET))
      # day long files
      if config[1] == 'day':
         st.append(0)
         for n in range (1, len(data.ET)):
            if data.DT[n, 2] != data.DT[n-1, 2]:
               st.append(n)
               ed.append(n)
         if len(st) != len(ed):
            ed.append(len(data.ET))
      # convert to np array of integer and save to data tuple   
      data.st = np.array(st)
      data.ed = np.array(ed)
   else: # specific date
      xx = str(config[2]).strip("[]").strip("'")
      xx = xx.split(",")
      
      # specific year
      if config[1] == 'year':
         for n in range (len(data.ET)):
            if data.DT[n, 0] == np.int(xx[2]):
               st.append(n)               
      # specific month
      if config[1] == 'month':
         for n in range (len(data.ET)):
            if data.DT[n, 1] == np.int(xx[1]):
               st.append(n)  
      # specific day
      if config[1] == 'day':
         for n in range (len(data.ET)):
            if data.DT[n, 2] == np.int(xx[0]):
               st.append(n)
      # convert to np array of integer and save to data tuple          
      ST = np.array(st)  
      
      data.st = ST[0]
      data.ed = ST[-1] + 1
      
   # add an initalise a counter 
   data.counter = -1
   
   #add the file version number
   data.ver = config[0]
   
   return data
 