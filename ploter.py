import sys, os, datetime,time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

timeList = []
RA = []
RAError = []
DEC = []
DECError = []
date = "{0}{1}".format(time.strftime("%d"), time.strftime("%B"))
with open(os.getcwd() + '/images_{0}/locations.txt'.format(date), 'r') as f:
    for l in f.readlines():
        [imgnameTemp, RA0Temp, RA1Temp, RA2Temp, RA3Temp, \
         DEC0Temp, DEC1Temp, DEC2Temp, DEC3Temp] = l.split()
        day = int(imgnameTemp[0])
        hour = int(imgnameTemp[1:3])
        min = int(imgnameTemp[3:5])
        timeList.append(datetime.datetime(2013, 12, 28 + day, hour, min))
        RA.append(float(RA2Temp))
        RAError.append(float(RA3Temp))
        DEC.append(float(DEC2Temp))
        DECError.append(float(DEC3Temp))
        
meanRA = np.mean(59.6)
meanDEC = np.mean(55.0)
displacementRA = 1000*(meanRA-RA)*(360/(23+56/60+4.1/3600))
displacementDEC = 1000*(meanDEC-DEC)

plt.plot(timeList, displacementRA, 'ro', timeList, displacementDEC, 'bo', linewidth=1.0)
plt.xlabel('Time')
plt.ylabel('Displacement [mas]')
plt.title('RA and DEC Offsets.')
plt.grid(True)
plt.tight_layout()
plt.margins(0.04,0.04)
fig = plt.gcf()
plt.show()
fig.savefig('displacements.pdf')
