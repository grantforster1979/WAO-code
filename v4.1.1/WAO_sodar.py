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
      
      if a.count('SDR') == 1:
         start_of_block.append(i)
            
   return start_of_block

def parse_time(lines, start_of_block, data):
   import time
   from datetime import datetime
   import calendar
   import numpy as np
   
   DT = []
   DoY = []
   ET = []
    
   for i in range(len(start_of_block)-1):
      a = lines[start_of_block[i]]
      ds = a[a.index('R')+2:a.index('U')-1] 
      
      tt = time.strptime(ds, "%y%m%d%H%M%S")
    
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
   
def parse_HK(lines, start_of_block, data):
   import numpy as np
   
   AVE = [] # avaeraging time (s)
   MIN = [] # min height (m)
   MAX = [] # max height (m)
   NOI = [] # noise
   STP = [] # step
   VOL = [] # volume (5 or 6 values)
   XMT = [] # transmit frequencies (last value rass)
   MIX = [] # mixing requencies (5 or 6 values)
   SMP = [] # sample frequensy = half rass sampling frequency
   AZI = [] # Azimuth angles (5 values)
   ZEN = [] # Zenith angles (5 values)
   TMP = [] # temperature
   FEC = [] # no idea not mentioned in manual
   DST = [] # rass - sodar separation
   XTL = [] # no idea not mentioned in manual
   ACL = [] # Absolute significance threshold
   RCL = [] # Relative threshold significance
   SCL = [] # SN theshold - raw
   ICL = [] # SN theshold - clusrter
   ECL = [] # Program switch - not available
   NCL = [] # Program switch - not available
   SVS = [] # software version
   
   for i in range(len(start_of_block)-1):
      a = lines[start_of_block[i]]
      AVE.append(a[a.index('AVE')+3:a.index('MIN')-1])
      MIN.append(a[a.index('MIN')+3:a.index('MAX')-1])
      MAX.append(a[a.index('MAX')+3:a.index('NOI')-1])
      NOI.append(a[a.index('NOI')+3:a.index('STP')-1])
      STP.append(a[a.index('STP')+3:a.index('VOL')-1])
      VOL.append(a[a.index('VOL')+3:a.index('XMT')-1])
      XMT.append(a[a.index('XMT')+3:a.index('MIX')-1])
      MIX.append(a[a.index('MIX')+3:a.index('SMP')-1])
      SMP.append(a[a.index('SMP')+3:a.index('AZI')-1])
      AZI.append(a[a.index('AZI')+3:a.index('ZEN')-1])
      ZEN.append(a[a.index('ZEN')+3:a.index('TMP')-1])
      TMP.append(a[a.index('TMP')+3:a.index('FEC')-1])
  
   # single valued variables
   data.AVE = np.array(np.float32(AVE))
   data.MIN = np.array(np.float32(MIN))
   data.MAX = np.array(np.float32(MAX))
   data.NOI = np.array(np.float32(NOI))
   data.STP = np.array(np.float32(STP))
   data.TMP = np.array(np.float32(TMP))
   
   # multivalued variables
   data.VOL = np.ones((len(AVE),6))
   data.XMT = np.ones((len(AVE),2))
   data.MIX = np.ones((len(AVE),6))
   data.SMP = np.ones((len(AVE),2))
   data.AZI = np.ones((len(AVE),5))
   data.ZEN = np.ones((len(AVE),5))
   # VOL(6), XMT(2), MIX(6), SMP(2), AZI(5), ZEN(5)
   for i in range(len(start_of_block)-1):
      # VOL
      vv = []
      a = VOL[i]
      vv.append(a[2:2+4])
      vv.append(a[8:8+4])
      vv.append(a[14:14+4])
      vv.append(a[20:20+4])
      vv.append(a[26:26+4])
      vv.append(a[32:32+4])
      for n in range(6):
         data.VOL[i,n] = np.float32(vv[n]) 
      
      # XMT
      vv = []
      a = XMT[i]
      vv.append(a[2:2+4])
      vv.append(a[8:8+4])
      for n in range(2):
         data.XMT[i,n] = np.float32(vv[n])
      
      # MIX
      vv = []
      a = MIX[i]
      vv.append(a[2:2+4])
      vv.append(a[8:8+4])
      vv.append(a[14:14+4])
      vv.append(a[20:20+4])
      vv.append(a[26:26+4])
      vv.append(a[32:32+4])
      for n in range(6):
         data.MIX[i,n] = np.float32(vv[n])
         
      # SMP
      vv = []
      a = SMP[i]
      vv.append(a[1:1+5])
      vv.append(a[7:7+5])
      for n in range(2):
         data.SMP[i,n] = np.float32(vv[n])
         
      # AZI
      vv = []
      a = AZI[i]
      vv.append(a[2:2+4])
      vv.append(a[8:8+4])
      vv.append(a[14:14+4])
      vv.append(a[20:20+4])
      vv.append(a[26:26+4])
      for n in range(5):
         data.AZI[i,n] = np.float32(vv[n])
      
      # ZEN
      vv = []
      a = ZEN[i]
      vv.append(a[2:2+4])
      vv.append(a[8:8+4])
      vv.append(a[14:14+4])
      vv.append(a[20:20+4])
      vv.append(a[26:26+4])
      for n in range(5):
         data.ZEN[i,n] = np.float32(vv[n])
         
   return data 

def parse_H(lines, start_of_block, data):
   import numpy as np 
  
   data.H = np.ones((len(start_of_block)-1,46))
   for i in range(len(start_of_block)-1):
      a = lines[start_of_block[i] + 1] 
      H = []
      for n in range(46):
         off = 3
         span = 6
         H.append(a[(off + (n * span)):(off + (n * span) + span)])
      
      H2 = np.array(H)
      for n in range(46):
         data.H[i,n] = np.float32(H2[n])  
   
   return data

def parse_DATA(lines, start_of_block, data):
   import numpy as np 
   
   data.V = np.ones((len(start_of_block)-1,44))
   data.D = np.ones((len(start_of_block)-1,44))
   data.R1 = np.ones((len(start_of_block)-1,44))
   data.R2 = np.ones((len(start_of_block)-1,44))
   data.R3 = np.ones((len(start_of_block)-1,44))
   data.R4 = np.ones((len(start_of_block)-1,44))
   data.R5 = np.ones((len(start_of_block)-1,44))
   data.VVU = np.ones((len(start_of_block)-1,44))
   data.VVV = np.ones((len(start_of_block)-1,44))
   data.VVW = np.ones((len(start_of_block)-1,44))
   data.SN1 = np.ones((len(start_of_block)-1,44))
   data.SN2 = np.ones((len(start_of_block)-1,44))
   data.SN3 = np.ones((len(start_of_block)-1,44))
   data.SN4 = np.ones((len(start_of_block)-1,44))
   data.SN5 = np.ones((len(start_of_block)-1,44))
   data.RTP = np.ones((len(start_of_block)-1,44))
   
   for i in range(len(start_of_block)-1):
      #Reflectivity
      a = lines[start_of_block[i] + 200] 
      R1 = []
      for n in range(44):
         off = 3
         span = 6
         R1.append(a[(off + (n * span)):(off + (n * span) + span)])
      
      a = lines[start_of_block[i] + 202]
      R2 = []
      for n in range(44):
         off = 3
         span = 6
         R2.append(a[(off + (n * span)):(off + (n * span) + span)])
      
      a = lines[start_of_block[i] + 204]
      R3 = []
      for n in range(44):
         off = 3
         span = 6
         R3.append(a[(off + (n * span)):(off + (n * span) + span)])
      
      a = lines[start_of_block[i] + 201]
      R4 = []
      for n in range(44):
         off = 3
         span = 6
         R4.append(a[(off + (n * span)):(off + (n * span) + span)])
      
      a = lines[start_of_block[i] + 203]
      R5 = []
      for n in range(44):
         off = 3
         span = 6
         R5.append(a[(off + (n * span)):(off + (n * span) + span)])
      
      #components
      a = lines[start_of_block[i] + 224]
      VVU = []
      for n in range(44):
         off = 3
         span = 6
         VVU.append(a[(off + (n * span)):(off + (n * span) + span)])
      
      a = lines[start_of_block[i] + 225]
      VVV = []
      for n in range(44):
         off = 3
         span = 6
         VVV.append(a[(off + (n * span)):(off + (n * span) + span)])
      
      a = lines[start_of_block[i] + 226]
      VVW = []
      for n in range(44):
         off = 3
         span = 6
         VVW.append(a[(off + (n * span)):(off + (n * span) + span)])
      
      #wind speed and direction
      a = lines[start_of_block[i] + 230]
      V = []
      for n in range(44):
         off = 3
         span = 6
         V.append(a[(off + (n * span)):(off + (n * span) + span)])
      
      a = lines[start_of_block[i] + 231]
      D = []
      for n in range(44):
         off = 3
         span = 6
         D.append(a[(off + (n * span)):(off + (n * span) + span)])
           
      #signal-to-noise
      a = lines[start_of_block[i] + 251]
      SN1 = []
      for n in range(44):
         off = 3
         span = 6
         SN1.append(a[(off + (n * span)):(off + (n * span) + span)])
         
      a = lines[start_of_block[i] + 252]
      SN4 = []
      for n in range(44):
         off = 3
         span = 6
         SN4.append(a[(off + (n * span)):(off + (n * span) + span)])
      
      a = lines[start_of_block[i] + 253]
      SN2 = []
      for n in range(44):
         off = 3
         span = 6
         SN2.append(a[(off + (n * span)):(off + (n * span) + span)])
         
      a = lines[start_of_block[i] + 254]
      SN5 = []
      for n in range(44):
         off = 3
         span = 6
         SN5.append(a[(off + (n * span)):(off + (n * span) + span)])
      
      a = lines[start_of_block[i] + 255]
      SN3 = []
      for n in range(44):
         off = 3
         span = 6
         SN3.append(a[(off + (n * span)):(off + (n * span) + span)])
      
      #rass temperature
      a = lines[start_of_block[i] + 244]
      RTP = []
      for n in range(44):
         off = 3
         span = 6
         RTP.append(a[(off + (n * span)):(off + (n * span) + span)])
      
      #replace blanks with -9999
      for n in range(44):
         try: 
            np.float32(R1[n])
         except:
            R1[n] = -9999
            
         try: 
            np.float32(R2[n])
         except:
            R2[n] = -9999 
            
         try: 
            np.float32(R3[n])
         except:
            R3[n] = -9999   
            
         try: 
            np.float32(R4[n])
         except:
            R4[n] = -9999   
            
         try: 
            np.float32(R5[n])
         except:
            R5[n] = -9999
            
         try: 
            np.float32(V[n])
         except:
            V[n] = -9999 

         try: 
            np.float32(D[n])
         except:
            D[n] = -9999
            
         try: 
            np.float32(VVU[n])
         except:
            VVU[n] = -9999
            
         try: 
            np.float32(VVV[n])
         except:
            VVV[n] = -9999
            
         try: 
            np.float32(VVW[n])
         except:
            VVW[n] = -9999
         
         try: 
            np.float32(SN1[n])
         except:
            SN1[n] = -9999
            
         try: 
            np.float32(SN2[n])
         except:
            SN2[n] = -9999 
            
         try: 
            np.float32(SN3[n])
         except:
            SN3[n] = -9999   
            
         try: 
            np.float32(SN4[n])
         except:
            SN4[n] = -9999   
            
         try: 
            np.float32(SN5[n])
         except:
            SN5[n] = -9999    

         try: 
            np.float32(RTP[n])
         except:
            RTP[n] = -9999             
      
      for n in range(44):
         data.V[i,n] = np.float32(V[n])
         data.D[i,n] = np.float32(D[n])
         data.R1[i,n] = np.float32(R1[n])
         data.R2[i,n] = np.float32(R2[n])
         data.R3[i,n] = np.float32(R3[n])
         data.R4[i,n] = np.float32(R4[n])
         data.R5[i,n] = np.float32(R5[n])
         data.VVU[i,n] = np.float32(VVU[n]) 
         data.VVV[i,n] = np.float32(VVV[n])
         data.VVW[i,n] = np.float32(VVW[n]) 
         data.SN1[i,n] = np.float32(SN1[n])
         data.SN2[i,n] = np.float32(SN2[n])
         data.SN3[i,n] = np.float32(SN3[n])
         data.SN4[i,n] = np.float32(SN4[n])
         data.SN5[i,n] = np.float32(SN5[n])   
         data.RTP[i,n] = np.float32(RTP[n])        
   
   return data   
   
def sort_DATA(data, data_final):
   import numpy as np
   # 4 blocks of data per time stamp
   # only want vertically point SNR and Reflectivity
   # 46 altitude values but only 44 varaible values
   
   # time
   ET = []
   DoY = []
   DT = []
   ET.append(data.ET[0])
   DoY.append(data.DoY[0])
   DT.append(data.DT[0,:])
   for n in range(1, len(data.ET)):
      a = data.ET[n]
      if a != ET[len(ET)-1]:
         ET.append(data.ET[n])
         DoY.append(data.DoY[n])
         DT.append(data.DT[n,:])        
         
   H = [] 
   V = [] 
   D = [] 
   VVU = []
   VVV = []
   VVW = []
   R = []
   SN = []
   RTP = []
   for n in range(len(ET)):
      h = []
      v = []
      d = []
      vvu = []
      vvv =[]
      vvw = []
      r = []
      sn = []
      rtp = []
      for i in range(len(data.ET)):
         if data.ET[i] == ET[n]:
            h.append(data.H[i,0:len(data.V[i,:])])
            
            a = data.V[i,:]
            np.putmask(a, a == -9999, np.nan)
            v.append(a)
           
            a = data.D[i,:]
            np.putmask(a, a == -9999, np.nan)
            d.append(a)
            
            a = data.VVU[i,:]
            np.putmask(a, a == -9999, np.nan)
            vvu.append(a)
            
            a = data.VVV[i,:]
            np.putmask(a, a == -9999, np.nan)
            vvv.append(a)
            
            a = data.VVW[i,:]
            np.putmask(a, a == -9999, np.nan)
            vvw.append(a)
            
            a = data.R3[i,:]
            np.putmask(a, a == -9999, np.nan)
            r.append(a)
            
            a = data.SN3[i,:]
            np.putmask(a, a == -9999, np.nan)
            sn.append(a)
            
            a = data.RTP[i,:]
            np.putmask(a, a == -9999, np.nan)
            rtp.append(a)
                 
      H.append(np.mean(np.array(h), axis = 0))
      V.append(np.nanmean(v, axis = 0))
      D.append(np.nanmean(d, axis = 0))
      VVU.append(np.nanmean(vvu, axis = 0))
      VVV.append(np.nanmean(vvv, axis = 0))
      VVW.append(np.nanmean(vvw, axis = 0))
      R.append(np.nanmean(r, axis = 0))
      SN.append(np.nanmean(sn, axis = 0))
      RTP.append(np.nanmean(rtp, axis = 0))
   
   data_final.ET = np.array(ET)
   data_final.DoY = np.array(DoY)
   data_final.DT = np.array(DT)
   data_final.H = np.nan_to_num(H, nan = -1.00e+20)
   data_final.V = np.nan_to_num(V, nan = -1.00e+20)
   data_final.D = np.nan_to_num(D, nan = -1.00e+20)
   data_final.VVU = np.nan_to_num(VVU, nan = -1.00e+20)
   data_final.VVV = np.nan_to_num(VVV, nan = -1.00e+20)
   data_final.VVW = np.nan_to_num(VVW, nan = -1.00e+20)
   data_final.R = np.nan_to_num(R, nan = -1.00e+20)
   data_final.SN = np.nan_to_num(SN, nan = -1.00e+20)
   data_final.RTP = np.nan_to_num(RTP, nan = -1.00e+20)
            
   return data_final 

def qc_DATA(data_final):   
   import numpy as np
   # flag arays
   data_final.qc_backscatter = np.ones(data_final.SN.shape)
   data_final.qc_mean_winds = np.ones(data_final.SN.shape)
   data_final.qc_wind_component_eastward = np.ones(data_final.SN.shape)
   data_final.qc_wind_component_northward = np.ones(data_final.SN.shape)
   data_final.qc_wind_component_upward_air_velocity = np.ones(data_final.SN.shape)
   data_final.qc_temperature = np.ones(data_final.RTP.shape)
   #1. Valid Sn >1 and <50
   ii = np.where(data_final.SN <= 1)
   data_final.qc_backscatter[ii] = 2
   data_final.qc_mean_winds[ii] = 2
   data_final.qc_wind_component_eastward[ii] = 2
   data_final.qc_wind_component_northward[ii] = 2
   data_final.qc_wind_component_upward_air_velocity[ii] = 2
   data_final.qc_temperature[ii] = 2
   ii = np.where(data_final.SN >= 50)
   data_final.qc_backscatter[ii] = 3
   data_final.qc_mean_winds[ii] = 3
   data_final.qc_wind_component_eastward[ii] = 3
   data_final.qc_wind_component_northward[ii] = 3
   data_final.qc_wind_component_upward_air_velocity[ii] = 3
   data_final.qc_temperature[ii] = 3
   #2. Backscatter >0 and <90dB
   ii = np.where((data_final.R <= 1) & (data_final.SN == 1))
   data_final.qc_backscatter[ii] = 4
   ii = np.where((data_final.R >= 90) & (data_final.SN == 1))
   data_final.qc_backscatter[ii] = 5
   #3. mean wind <0 and >35
   ii = np.where((data_final.V <= 0) & (data_final.SN == 1))
   data_final.qc_mean_winds[ii] = 4
   ii = np.where((data_final.V >= 35) & (data_final.SN == 1))
   data_final.qc_mean_winds[ii] = 5
   ii = np.where((data_final.D <= 0) & (data_final.SN == 1))
   data_final.qc_mean_winds[ii] = 6
   ii = np.where((data_final.D >= 360) & (data_final.SN == 1))
   data_final.qc_mean_winds[ii] = 7
   ii = np.where((data_final.V == 0) & (data_final.SN == 1))
   data_final.qc_mean_winds[ii] = 8
   #4. U components <-10 and >10
   ii = np.where((data_final.VVU <= -10) & (data_final.SN == 1))
   data_final.qc_wind_component_eastward[ii] = 4
   ii = np.where((data_final.VVU >= 10) & (data_final.SN == 1))
   data_final.qc_wind_component_eastward[ii] = 5
   ii = np.where((data_final.VVU == 0) & (data_final.SN == 1))
   data_final.qc_wind_component_eastward[ii] = 6
   #5. V components <-10 and >10
   ii = np.where((data_final.VVV <= -10) & (data_final.SN == 1))
   data_final.qc_wind_component_northward[ii] = 4
   ii = np.where((data_final.VVV >= 10) & (data_final.SN == 1))
   data_final.qc_wind_component_northward[ii] = 5
   ii = np.where((data_final.VVV == 0) & (data_final.SN == 1))
   data_final.qc_wind_component_northward[ii] = 6
   #6. W components <-10 and >10
   ii = np.where((data_final.VVW <= -10) & (data_final.SN == 1))
   data_final.qc_wind_component_upward_air_velocity[ii] = 4
   ii = np.where((data_final.VVW >= 10) & (data_final.SN == 1))
   data_final.qc_wind_component_upward_air_velocity[ii] = 5
   ii = np.where((data_final.VVW == 0) & (data_final.SN == 1))
   data_final.qc_wind_component_upward_air_velocity[ii] = 6
   #7. Rass Temperatrue <-50 and >50
   ii = np.where(data_final.RTP <= -50)
   data_final.qc_temperature[ii] = 4
   ii = np.where(data_final.RTP >= 50)
   data_final.qc_temperature[ii] = 5
   
   return data_final
    
def sodar_parse(config, data): 
   import os
   
   lines = []
   start_of_block = []
   
   fn = os.path.normpath(str(config[5]).strip('[]'))
   fn = fn[1:len(fn)-1] 
   
   #create a blank copy data
   data_final = data
   
   #read all file in directory
   lines = get_file(fn, lines)
   
   #find the start of the data blocks 
   start_of_block = parse_block(lines, start_of_block)    
    
   #parse time
   data = parse_time(lines, start_of_block, data) 
   
   #parse houskeeping
   data = parse_HK(lines, start_of_block, data) 
   
   #parse height
   data = parse_H(lines, start_of_block, data)
  
   #parse data
   data = parse_DATA(lines, start_of_block, data)
   
   #sort data
   data_final = sort_DATA(data, data_final)
   
   #QC data
   data_final = qc_DATA(data_final)
   
   return data_final