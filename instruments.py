import csv
import matplotlib.pyplot as plt
import numpy as np

#read csv into dict
filename = 'instruments.csv'
reader = csv.DictReader(open(filename), delimiter = '\t', quotechar = '"')
instruments = [i for i in reader if i['Date'].isdigit()]

# Instruments with labels positioned ABOVE the marker
textPositionUpper=['FIRAS','MSAM','FIRP','SHARC','SPIFI','MAMBO-1','HUMBA','MAXIMA','ARCHEOPS01','HAWC','AZTEC','QUAD','APEX-SZ','ACT/MBAC','NIKA09','EBEX','BICEP3','ARCONS','BOLOCAM','MKID_DEMOCAM','POLARBEAR-2','AdvACT','LiteBIRD','DARKNESS','SO-LAT','MUSIC','BICEP2','SPIRE','SPT-3G','DESHIMA-2.0']

# Instruments with labels positioned BELOW the marker (explicitly listed)
textPositionLower=['KISS','SPT-SLIM','TolTEC','TIM','ModCam','SOUK-SATs','SO-LAT-FULL','CMB-S4','ZEUS2','SPT-3G','BLAST_TNG','BICEP2']

# Future instruments (>2025) get parentheses
futureYear = 2025

#prepare plot and add points
f = plt.figure(figsize=(12,8))
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
    # On-chip Spectrometer MKIDs (e.g., DESHIMA, SuperSpec, SPT-SLIM)
    elif i['Detector_Subtype'] == 'MKID-Spec':
      colour = 'blue'
      marker = 's'
    # Conventional Spectrometer MKIDs (e.g., KISS, CONCERTO, TIM)
    elif i['Detector_Subtype'] == 'MKID-Spec-Conv':
      colour = 'darkgreen'
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
  ax.plot(float(x), float(y), marker = marker, color = colour,  alpha=1)
  
  # Determine label text (add parentheses for future instruments)
  label_text = i['Instrument']
  if int(x) > futureYear:
    label_text = '(' + label_text + ')'
  
  # Apply position for labels
  if i['Instrument'] in textPositionUpper:
    ax.text(float(x),float(y)*1.05, label_text,size=9,va='bottom',ha='center')
  elif i['Instrument'] in textPositionLower:
    ax.text(float(x),float(y)*0.9, label_text,size=9,va='top',ha='center')
  else:
    # Default: below
    ax.text(float(x),float(y)*0.9, label_text,size=9,va='top',ha='center')
  

#gather data for fits to log10 of number of detectors
# Only include instruments up to 2025 in trend lines
maxYearForTrend = 2025

bolos_x = [float(i['Date']) for i in instruments if i['Detector_Type'] == 'Bolometer' and float(i['Date']) <= maxYearForTrend]
bolos_y = [np.log10(float(i['Total_Detectors'])) for i in instruments if i['Detector_Type'] == 'Bolometer' and float(i['Date']) <= maxYearForTrend]

# TES trend excludes space-based (TES-Space) and discontinued (TES-Discontinued) instruments
tes_x = [float(i['Date']) for i in instruments if i['Detector_Subtype'] == 'TES' and float(i['Date']) <= maxYearForTrend]
tes_y = [np.log10(float(i['Total_Detectors'])) for i in instruments if i['Detector_Subtype'] == 'TES' and float(i['Date']) <= maxYearForTrend]

semicond_x = [float(i['Date']) for i in instruments if (i['Detector_Type'] == 'Bolometer' and i['Detector_Subtype'] not in ['TES', 'TES-Space', 'TES-Discontinued'] and float(i['Date']) <= maxYearForTrend)]
semicond_y = [np.log10(float(i['Total_Detectors'])) for i in instruments if (i['Detector_Type'] == 'Bolometer' and i['Detector_Subtype'] not in ['TES', 'TES-Space', 'TES-Discontinued'] and float(i['Date']) <= maxYearForTrend)]

# KID trend excludes UV/optical/IR MKIDs (MKID-OIR), on-chip Spectrometer MKIDs (MKID-Spec), and future instruments
kids_x = [float(i['Date']) for i in instruments if (i['Detector_Type'] == 'KID' and i['Detector_Subtype'] not in ['MKID-OIR', 'MKID-Spec'] and float(i['Date']) <= maxYearForTrend)]
kids_y = [np.log10(float(i['Total_Detectors'])) for i in instruments if (i['Detector_Type'] == 'KID' and i['Detector_Subtype'] not in ['MKID-OIR', 'MKID-Spec'] and float(i['Date']) <= maxYearForTrend)]

mkids_x = [float(i['Date']) for i in instruments if i['Detector_Subtype'] in ['MKIDCAM', 'First_MKID','MKID','NIKA','LEKID'] and float(i['Date']) <= maxYearForTrend]
mkids_y = [np.log10(float(i['Total_Detectors'])) for i in instruments if i['Detector_Subtype'] in ['MKIDCAM', 'First_MKID','MKID','NIKA','LEKID'] and float(i['Date']) <= maxYearForTrend]

lekids_x = [float(i['Date']) for i in instruments if i['Detector_Subtype'] in ['NIKA','KIDCAM', 'LEKID'] and float(i['Date']) <= maxYearForTrend]
lekids_y = [np.log10(float(i['Total_Detectors'])) for i in instruments if i['Detector_Subtype'] in ['NIKA','KIDCAM','LEKID'] and float(i['Date']) <= maxYearForTrend]


#fit lines between given dates
bolorange = np.linspace(1980, 2040., 10)
tesrange = np.linspace(1980, 2040., 10)
semicondrange = np.linspace(1980, 2040., 10)
kidrange = np.linspace(1980, 2040., 10)
mkidrange = np.linspace(1980., 2040., 10)
lekidrange = np.linspace(1980., 2040., 10)

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
plt.plot([], 'o',  color = 'red',alpha=1, label = 'Semiconductor Bolometers')
plt.plot([], '*',  color = 'red',alpha=1, label = 'Semiconductor Bolometers (Space)')
plt.plot([], 'o',  color = 'gold',alpha=1, label = 'TES Bolometers')
plt.plot([], '*',  color = 'gold',alpha=1, label = 'TES Bolometers (Space)')
plt.plot([], 'o',  color = 'gray',alpha=1, label = 'TES (Discontinued)')
plt.plot([], 'o',  color = 'green',alpha=1, label = 'mm/submm/FIR MKIDs')
plt.plot([], 's',  color = 'darkgreen',alpha=1, label = 'MKID Spectrometers')
plt.plot([], 'D',  color = 'purple',alpha=1, label = 'UV/Optical/IR MKIDs')
plt.plot([], 's',  color = 'blue',alpha=1, label = 'MKID On-chip Spectrometers')

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
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
ax.set_ylim(0.6, 1000000.)
ax.set_xlim(1985, 2035)
ax.tick_params(axis='x', labelsize='x-large')
ax.tick_params(axis='y', labelsize='x-large')
ax.set_ylabel('Detectors per instrument',fontsize='x-large')
ax.set_xlabel('Year',fontsize='x-large')
plt.grid(which='major')
plt.grid(which='minor', axis='y', linestyle=':', alpha=0.5)
ax.minorticks_on()
plt.legend(loc = 0, numpoints = 1)
#plt.title('Detector counts over time for mm/sub-mm/FIR astronomical instruments', fontsize='xx-large')
plt.tight_layout()
plt.savefig('instruments.png')

plt.show()
