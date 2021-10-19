def get_file(fn, lines):
   ll=[]
   f = open(fn, 'r') 
   ll = f.readlines()
   f.close()
   for i in ll:
      lines.append(i)
    
   return lines
   
def parse_block(lines, start_of_block):
   for i in range(len(lines)):
      a = lines[i]
      
      if a.count('CT') == 1:
         start_of_block.append(i)
            
   return start_of_block

def parse_time(lines, start_of_block, np, data):
   import time
   from datetime import datetime
   import calendar
   
   DT = []
   DoY = []
   ET = []
    
   for i in range(len(start_of_block)-1):
      a = lines[start_of_block[i]]
      ds = a[0:a.index('C')-1]   
           
      try: 
         tt = time.strptime(ds, "%Y-%m-%dT%H:%M:%S.%f")
      except:
         tt = time.strptime(ds, "%Y-%m-%dT%H:%M:%S")
      
      #DoY
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      #DT
      DT.append(tt[0:6]) 
       
   data.DT = np.array(DT)
   data.DoY = np.array(DoY)
   data.ET = np.array(ET)
    
   return data
  
def parse_line1(lines, start_of_block, np, data):
   l11 = []
   l12 = []
   l13 = []
   for i in range(len(start_of_block)-1):
      a = lines[start_of_block[i]]
      b = a[a.index('C'):len(a)-1] 
      
      l11.append(b[2])    #unit ID
      l12.append(b[3:5])  #software level
      l13.append(b[5])    #message number
    
   data.HK1 = np.empty([len(l11),3], dtype = object)
   
   data.HK1[:,0] = np.array(l11)
   data.HK1[:,1] = np.array(l12)
   data.HK1[:,2] = np.array(l13)
   
   return data
   
def parse_CBH(lines, start_of_block, np, data, offset):
   l21 = []
   l22 = []
   cbh1 = []
   cbh2 = []
   cbh3 = []
   cflag = []
   for i in range(len(start_of_block)-1):
      a = lines[start_of_block[i]+offset]
      b = a[a.index(' ')+1:len(a)-1]
      
      l21.append(b[0])            #message status
      l22.append(b[1])            #warning
      cbh1.append(b[3:8])         #cloudbase height 1
      cbh2.append(b[9:14])        #cloudbase height 2
      cbh3.append(b[15:20])       #cloudbase height 3
      cflag.append(b[21:len(b)])  #flag 
      
   data.L21 = np.array(l21)
   data.L22 = np.array(l22)
   data.CBH1 = np.array(cbh1)
   data.CBH2 = np.array(cbh2)
   data.CBH3 = np.array(cbh3)
   data.CFLAG = np.array(cflag)
   
   # AMF flags: 
   #1 - good data, 2 - no sig backscatter, 3 - full obfurscation no cloud base
   #4 - some obfurscation - transparent, 5 - time stamp
   
   # vaisala flags:
   #0 - no sig backscatter, 1 - one cb, 2 - two cbs, 3 - 3 cbs,
   #4 - full obfurscation no cloud base, 5 - some obfurscation - transparent
   #/ - Raw data input to algorithm missing or suspect
    
   #get rid of '/////'
   for n in range(len(data.ET)):
      if data.CBH1[n].find('/') > -1:
         data.CBH1[n] = -99
      else:
         data.CBH1[n] = int(data.CBH1[n])    
            
   for n in range(len(data.ET)):
      if data.CBH2[n].find('/') > -1:
         data.CBH2[n] = -99
      else:
         data.CBH2[n] = int(data.CBH2[n]) 
        
   for n in range(len(data.ET)):
      if data.CBH3[n].find('/') > -1:
         data.CBH3[n] = -99
      else:
         data.CBH3[n] = int(data.CBH3[n])      
    
   data.CBH_flag = np.ones([len(data.CBH1),3])
 
   ii_0 = np.where(l21 == 0)
   data.CBH_flag[ii_0,:] = 2
   data.CBH1[ii_0] = -99
   data.CBH2[ii_0] = -99
   data.CBH3[ii_0] = -99
    
   ii_0 = np.where(l21 == 1)
   data.CBH2[ii_0] = -99
   data.CBH3[ii_0] = -99
    
   ii_0 = np.where(l21 == 2)
   data.CBH3[ii_0] = -99
    
   ii_0 = np.where(l21 == 4)
   data.CBH_flag[ii_0,:] = 3
   data.CBH1[ii_0] = -99
   data.CBH2[ii_0] = -99
   data.CBH3[ii_0] = -99
    
   ii_0 = np.where(l21 == 5)
   data.CBH_flag[ii_0,:] = 4
   data.CBH1[ii_0] = -99
   data.CBH2[ii_0] = -99
   data.CBH3[ii_0] = -99
  
   s = (len(data.ET),3)
   data.CBH = np.ones(s)
    
   #cloudbase height (m)
   for n in range(len(data.ET)):
      data.CBH[n,0] = np.float32(data.CBH1[n])*0.3048 #now in m
      data.CBH[n,1] = np.float32(data.CBH2[n])*0.3048 #now in m
      data.CBH[n,2] = np.float32(data.CBH3[n])*0.3048 #now in m
   
   for n in range(len(data.ET)):
      for i in range(3):
         if data.CBH[n,i] < 0:
            data.CBH[n,i] = -1e+20
 
   return data 

def parse_HK(lines, start_of_block, np, data, offset):
   l31 = []
   l32 = []
   l33 = []
   l34 = []
   l35 = []
   l36 = []
   l37 = []
   l38 = []
   l39 = []
   l310 = []
   
   for i in range(len(start_of_block)-1):
      a = lines[start_of_block[i]+offset]
      b = a[a.index(' ')+1:len(a)-1]
     
      l31.append(b[0:3])       #scale
      l32.append(b[4])         #measurement mode
      l33.append(b[6:9])       #laser pulse energy
      l34.append(b[10:13])     #laser temperature
      l35.append(b[14:17])     #receiver sensitivity
      l36.append(b[19:22])     #window contamination
      l37.append(b[24:27])     #tilt angle
      l38.append(b[28:31])     #background light
      l39.append(b[32:38])     #measurement parameters
      l310.append(b[39:len(b)]) #sum 
        
   data.HK2 = np.empty([len(l31),10], dtype = object)
   
   data.HK2[:,0] = np.array(np.float32(l31))
   data.HK2[:,1] = np.array(l32)
   data.HK2[:,2] = np.array(np.float32(l33))
   data.HK2[:,3] = np.array(np.float32(l34) + 273.15)
   data.HK2[:,4] = np.array(np.float32(l35))
   data.HK2[:,5] = np.array(np.float32(l36))
   data.HK2[:,6] = np.array(np.float32(l37))
   data.HK2[:,7] = np.array(np.float32(l38))
   data.HK2[:,8] = np.array(l39)
   data.HK2[:,9] = np.array(np.float32(l310)/10000) #now in sr-1
   
   return data 

def parse_PROF(lines, start_of_block, np, data, offset):
   line4 = []
    
   for i in range(len(start_of_block)-1):
      z = []
      bb = []
      for ii in range(16): #16 lines of data
         a = lines[start_of_block[i]+offset+ii]
         b = a[a.index(' ')+1:len(a)-1]
         z1 = int(b[0:3])*100#start of line height
         c = b[3:len(b)]
         for cc in range(16): #16 range gates per line
            z.append((z1+(cc*100))*0.3048) #profile height
            temp = int(c[cc*4:((cc*4)+4)],16)##(10 000.sr.km)-1 = 10 000 sr-1 * 1 000 m-1 = 1e7
            bb.append(float(temp/1e7)) #sr-1 m-1
         
      line4.append(bb)
          
   data.ZZ = np.array(np.float32(z))
   data.BB = np.array(np.float32(line4))   

   #backscatter flag
   data.BB_flag = np.ones(data.BB.shape)
   ii_min = np.where(data.BB <= 1e-7)
   data.BB_flag[ii_min] = 2
   ii_max = np.where(data.BB > 0.06)
   data.BB_flag[ii_max] = 2
       
   return data
    
def ceil_parse(config, data): 
   import os
   import numpy as np
   
   din = os.path.normpath(str(config[5]).strip('[]'))
   din = din[1:len(din)-1]  
   
   infiles = os.listdir(din)
   lines = []
   start_of_block = []
    
   #read all file in directory
   for ii in range(0,len(infiles)):
      lines = get_file((din + infiles[ii]), lines)
   
   #find the start of the data blocks 
   start_of_block = parse_block(lines, start_of_block)    
    
   #parse time
   data = parse_time(lines, start_of_block, np, data) 
   
   #parse line 1 - housekeeping
   data = parse_line1(lines, start_of_block, np, data) # housekeeping 1
   
   #parse line 2 - cloud base height
   data = parse_CBH(lines, start_of_block, np, data, 1) # cloudbase height
  
   #parse line 3 - housekeeping  
   data = parse_HK(lines, start_of_block, np, data, 2) # housekeeping 2

   #parse line 4 - profile   
   data = parse_PROF(lines, start_of_block, np, data, 3) # backscatter profile 
   
   return data