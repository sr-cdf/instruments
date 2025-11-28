import csv
import matplotlib.pyplot as plt
import numpy as np

#read csv into dict
filename = 'instruments.csv'
reader = csv.DictReader(open(filename), delimiter = '\t', quotechar = '"')
instruments = [i for i in reader if i['Date'].isdigit()]

textPositionUpper=['FIRAS','MSAM','FIRP','SHARC','SPIFI','MAMBO-1','HUMBA','MAXIMA','ARCHEOPS01','HAWC','AZTEC','QUAD','APEX-SZ','ACT/MBAC','NIKA09','EBEX','BICEP3','ZEUS2','ARCONS','AdvACT','DARKNESS','TolTEC','SO-SATs','ModCam','CMB-S4','Prime-Cam','DESHIMA-2.0','SO-LAT']

#prepare plot and add points
f = plt.figure(figsize=(16,10))
ax = f.add_subplot(111)
####for i in instruments:
  #####choose colour / marker
  ####if i['Detector_Subtype'] in ['MKIDCAM', 'First_MKID','MKID','AMKID']:
    ####colour = 'green'
    ####marker = 'o'
  ####elif i['Detector_Subtype'] in ['KIDCAM', 'First_LEKID']:
    ####colour = 'green'
    ####marker = '*'
  ####elif i['Detector_Subtype'] in ['NIKA']:
    ####colour = 'green'
    ####marker = 'v'
  ####elif i['Detector_Subtype'] in ['BLAST']:
    ####colour = 'green'
    ####marker = '^'
  ####elif i['Platform'] == 'Ground':
    ####colour = 'red'
    ####marker = 'v'
  ####elif i['Platform'] == 'Balloon':
    ####colour = 'red'
    ####marker = '^'
  ####elif i['Platform'] == 'Space':
    ####colour = 'red'
    ####marker = '*'
  ####else:
    ####print i['Instrument']
    ####colour = 'red'
    ####marker = 'o'
    
for cnt,i in enumerate(instruments):
  #choose colour / marker
  if i['Detector_Type'] in ['Bolometer','Bolometer1']:
    colour = 'red'
    marker = 'o'
    if i['Detector_Subtype'] in ['TES','TES1']:
      colour = 'gold'
      marker = 'o'
    # Space-based TES (e.g., LiteBIRD)
    if i['Detector_Subtype'] == 'TES-Space':
      colour = 'gold'
      marker = '*'
    # Discontinued TES (e.g., CMB-S4)
    if i['Detector_Subtype'] == 'TES-Discontinued':
      colour = 'gray'
      marker = 'o'
  
  elif i['Detector_Type'] in ['KID','KID1']:
    colour = 'green'
    marker='o'
    # UV/Optical/IR MKIDs (e.g., DARKNESS, ARCONS)
    if i['Detector_Subtype'] == 'MKID-OIR':
      colour = 'purple'
      marker = 'D'
    # Spectrometer MKIDs (e.g., DESHIMA, SuperSpec)
    elif i['Detector_Subtype'] == 'MKID-Spec':
      colour = 'blue'
      marker = 's'
    # Standard mm/submm/FIR KIDs (including LEKID, MKID, NIKA)
    elif i['Detector_Subtype'] in ['LEKID','LEKID1','MKID','NIKA']:
      colour = 'green'
      marker = 'o'
  
  if i['Platform']=='Space':
    marker='*'
  
  #else:
    #print i['Instrument']
  
  #choose marker symbol
  #if i['Detector_Subtype'] in ['KIDCAM', 'First_LEKID']:
    #marker = 'D'
  #elif i['Detector_Subtype'] in ['MKIDCAM', 'First_MKID']: 
    #marker = 's'
  #elif i['Detector_Subtype'] in ['NIKA']:
    #marker = 's'
  #else:
    #marker = 'o'
  
  #gather data and ignore bad fields
  x = i['Date']
  y = i['Total_Detectors']
  if not x.isdigit():
    print(i['Instrument']+': date is not a number:', i)
    continue
  if not y.isdigit():
    print(i['Instrument']+': number of detectors is not a number:', i)
    continue
  
  #plot
  ax.plot(float(x), float(y), marker = marker, color = colour,  ms=10, alpha=0.7)
  if i['Instrument'] in textPositionUpper:
    ax.text(float(x),float(y)*1.05, i['Instrument'],size=9,va='bottom',ha='center')
  else:
    ax.text(float(x),float(y)*0.9, i['Instrument'],size=9,va='top',ha='center')
  

#gather data for fits to log10 of number of detectors
bolos_x = [float(i['Date']) for i in instruments if i['Detector_Type'] == 'Bolometer']
bolos_y = [np.log10(float(i['Total_Detectors'])) for i in instruments if i['Detector_Type'] == 'Bolometer']

# TES trend excludes space-based (TES-Space) and discontinued (TES-Discontinued) instruments
tes_x = [float(i['Date']) for i in instruments if i['Detector_Subtype'] == 'TES']
tes_y = [np.log10(float(i['Total_Detectors'])) for i in instruments if i['Detector_Subtype'] == 'TES']

semicond_x = [float(i['Date']) for i in instruments if (i['Detector_Type'] == 'Bolometer' and i['Detector_Subtype'] not in ['TES', 'TES-Space', 'TES-Discontinued'])]
semicond_y = [np.log10(float(i['Total_Detectors'])) for i in instruments if (i['Detector_Type'] == 'Bolometer' and i['Detector_Subtype'] not in ['TES', 'TES-Space', 'TES-Discontinued'])]

# KID trend excludes UV/optical/IR MKIDs (MKID-OIR) and Spectrometer MKIDs (MKID-Spec)
kids_x = [float(i['Date']) for i in instruments if (i['Detector_Type'] == 'KID' and i['Detector_Subtype'] not in ['MKID-OIR', 'MKID-Spec'])]
kids_y = [np.log10(float(i['Total_Detectors'])) for i in instruments if (i['Detector_Type'] == 'KID' and i['Detector_Subtype'] not in ['MKID-OIR', 'MKID-Spec'])]

mkids_x = [float(i['Date']) for i in instruments if i['Detector_Subtype'] in ['MKIDCAM', 'First_MKID','MKID','NIKA','LEKID']]
mkids_y = [np.log10(float(i['Total_Detectors'])) for i in instruments if i['Detector_Subtype'] in ['MKIDCAM','MKID','NIKA','LEKID']]

lekids_x = [float(i['Date']) for i in instruments if i['Detector_Subtype'] in ['NIKA','KIDCAM', 'LEKID']]
lekids_y = [np.log10(float(i['Total_Detectors'])) for i in instruments if i['Detector_Subtype'] in ['NIKA','KIDCAM','LEKID']]


#fit lines between given dates
bolorange = np.linspace(1980, 2030., 10)
tesrange = np.linspace(1980, 2030., 10)
semicondrange = np.linspace(1980, 2030., 10)
kidrange = np.linspace(1980, 2030., 10)
mkidrange = np.linspace(1980., 2030., 10)
lekidrange = np.linspace(1980., 2030., 10)

bolo_poly = np.polyfit(bolos_x, bolos_y, 1)
bolo_fit = np.poly1d(bolo_poly)(bolorange)

semicond_poly =  np.polyfit(semicond_x, semicond_y, 1)
semicond_fit = np.poly1d(semicond_poly)(semicondrange)

tes_poly =  np.polyfit(tes_x, tes_y, 1)
tes_fit = np.poly1d(tes_poly)(tesrange)


kids_poly = np.polyfit(kids_x, kids_y, 1)
kids_fit = np.poly1d(kids_poly)(kidrange)

mkid_poly = np.polyfit(mkids_x, mkids_y, 1)
mkid_fit = np.poly1d(mkid_poly)(mkidrange)

lekid_poly = np.polyfit(lekids_x, lekids_y, 1)
lekid_fit = np.poly1d(lekid_poly)(lekidrange)


##make points for legend
#plt.plot([], 'v', ms=16, color = 'red', label = 'Ground based bolometers')
#plt.plot([], 'o', ms=16, color = 'red', label = 'Air-borne bolometers')
#plt.plot([], '*', ms=16, color = 'red', label = 'Space based bolometers')
#plt.plot([], '^', ms=16, color = 'red', label = 'Balloon-borne bolometers')
#plt.plot([], 'v', ms=16, color = 'green', label = 'NIKA KIDs')
#plt.plot([], 'o', ms=16, color = 'green', label = 'Caltech/JPL KIDs')
#plt.plot([], '*', ms=16, color = 'green', label = 'Cardiff KIDs')
#plt.plot([], '^', ms=16, color = 'green', label = 'Balloon KIDs')

#make points for legend
plt.plot([], 'o', ms=16, color = 'red',alpha=0.7, label = 'Semiconductor Bolometers')
plt.plot([], 'o', ms=16, color = 'gold',alpha=0.7, label = 'TES Bolometers')
plt.plot([], 'o', ms=16, color = 'gray',alpha=0.7, label = 'TES (Discontinued)')
plt.plot([], 'o', ms=16, color = 'green',alpha=0.7, label = 'mm/submm/FIR MKIDs')
plt.plot([], 'D', ms=16, color = 'purple',alpha=0.7, label = 'UV/Optical/IR MKIDs')
plt.plot([], 's', ms=16, color = 'blue',alpha=0.7, label = 'MKID Spectrometers')
plt.plot([], '*', ms=16, color = 'gold',alpha=0.7, label = 'Space-based TES')

#plot trends accounting for log axis
#ax.plot(bolorange, 10**bolo_fit, 'b--')#label = 'Bolometers trend')
#ax.plot(semicondrange,10**semicond_fit, '-',color='red',lw=64,zorder=0,alpha=0.15)#label = 'Non-TES bolometer trend')
#ax.plot(tesrange,10**tes_fit, '-',color='gold',lw=64,zorder=0,alpha=0.15)#label = 'TES trend')
#ax.plot(kidrange, 10**kids_fit, '-',color='green',lw=64,zorder=0,alpha=0.15)#label = 'KIDs trend')
ax.plot(semicondrange,10**semicond_fit, '-',color='red',lw=40,zorder=0,alpha=0.3)#label = 'Non-TES bolometer trend')
ax.plot(tesrange,10**tes_fit, '-',color='gold',lw=40,zorder=0,alpha=0.3)#label = 'TES trend')
ax.plot(kidrange, 10**kids_fit, '-',color='green',lw=40,zorder=0,alpha=0.3)#label = 'KIDs trend')

#ax.plot(mkidrange, 10**mkid_fit, 'g--', )#label = 'KIDs trend')
#ax.plot(lekidrange, 10**lekid_fit, 'r--', )#label = 'Cardiff KIDs trend')


#decorations
ax.semilogy()
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%0.0f'))
ax.set_ylim(0.6, 1000000.)
ax.set_xlim(1985, 2030)
ax.tick_params(axis='x', labelsize='x-large')
ax.tick_params(axis='y', labelsize='x-large')
ax.set_ylabel('Detectors per instrument',fontsize='x-large')
ax.set_xlabel('Year',fontsize='x-large')
plt.grid()
plt.legend(loc = 0, numpoints = 1, prop = {'size':'x-large'})
#plt.title(' Bolometric Instruments and KIDs in the FIR/(sub)mm \n')
plt.savefig('instruments.png')

plt.show()
