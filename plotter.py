"""
This program is designed to plot the residuals of the location of the spacecraft 
as found by pipeline and printed in locations.txt. The user must specify centerRA, 
centerDEC, offsetMin, offsetSec, dist. CenterRA/DEC is the predicted 
spacecraft location. The offsets are to move the points from the 
beginning of the scan to the middle. Dist specifies the distance to the 
spacecraft, allowing the standard deviations to be specified in meters. 
The default is to run off of a file called images_dayMonth[0:3]
"""

import sys, os, time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import numpy as np 
from datetime import datetime


centerRA  = 59.60
centerDEC = 55.00
offsetMin = 3 #time set to middle of scan 
offsetSec = 30
dist = 1.395

print("\Assuming center RA = {0}".format(centerRA))
print("Assumign center DEC = {0}".format(centerDEC))

def plot():
    timeList = [];
    RAhour = []; RAmin = []; RAsec = []; RAerror = [];
    DECdeg = []; DECmin = []; DECsec = []; DECerror = [];
    
    date = "{0}{1}".format(time.strftime("%d"), time.strftime("%B")[0:3])
    with open(os.getcwd() + '/images_{0}/locations.txt'.format(date), 'r') as f:
        for l in f.readlines():
            [imgnameTemp, RAhourT, RAminT, RAsecT, RAerrorT, \
             DECdegT, DECminT, DECsecT, DECerrorT] = l.split()
            day = int(imgnameTemp[0])
            hour = int(imgnameTemp[1:3])
            minutes = int(imgnameTemp[3:5])
            second = int(imgnameTemp[5:7])
            second = second + offsetSec
            if second >= 60:
                minutes = minutes + 1 
                second = second - 60
            minutes = minutes + offsetMin
            if minutes >= 60:
                hour = hour + 1
                minutes = minutes - 60
            if hour >= 24:
                day = day + 1
                hour = hour - 24
            timeList.append(datetime(2013, 12, 28 + day, hour, minutes, second))
            RAhour.append(float(RAhourT))
            RAmin.append(float(RAminT))
            RAsec.append(float(RAsecT))
            RAerror.append(float(RAerrorT))
            DECdeg.append(float(DECdegT))
            DECmin.append(float(DECminT))
            DECsec.append(float(DECsecT))
            DECerror.append(float(DECerrorT))
            
    RA = np.array([RAhour, RAmin, RAsec, RAerror])
    DEC = np.array([DECdeg, DECmin, DECsec, DECerror])       
    DECdecimal = []
    for j in range(len(DEC[0])):
        DECdecimal.append(DEC[0][j] + DEC[1][j]/60.0 + DEC[2][j]/3600.0)

    DECmean = np.mean(DECdecimal)
    #centerRA = centerRA*(360/(23+56/60+4.1/3600)*np.cos(np.deg2rad(DECmean)))
    RAdeg = [[None]*len(RA[0])]*4
    #for k in range(len(RA[0])):
    #    RAdeg[0][k] = RA[0][k]*(360/(23+56/60+4.1/3600)*np.cos(np.deg2rad(DECmean)))
    #    RAdeg[1][k] = RA[1][k]*(360/(23+56/60+4.1/3600)*np.cos(np.deg2rad(DECmean)))
    #    RAdeg[2][k] = RA[2][k]*(360/(23+56/60+4.1/3600)*np.cos(np.deg2rad(DECmean)))
    #    RAdeg[3][k] = RA[3][k]*(360/(23+56/60+4.1/3600)*np.cos(np.deg2rad(DECmean)))

    RAdec = np.array(RAdeg)
    displacementRA = []
    displacementDEC = []
    errRA = []
    errDEC = []

    for q in range(len(RAdec[0])):
        displacementRA.append(((centerRA - RA[2][q])*(360/(23+56.0/60.0+4.1/3600)*np.cos(np.deg2rad(DECmean))))*1000.0)
        errRA.append((RA[3][q]*(360/(23+56.0/60.0+4.1/3600)*np.cos(np.deg2rad(DECmean))))*1000.0)
        displacementDEC.append((DEC[2][q]-centerDEC)*1000.0)
        errDEC.append(DEC[3][q]*1000.0)
        
    print("Number of RA points {0}".format(len(displacementRA)))
    print("Number of DEC points {0}".format(len(displacementDEC)))    
    RAstd = np.std(displacementRA)
    DECstd = np.std(displacementDEC)
    RAstdM = RAstd/(1000.0*3600.0)*np.pi/180.0*dist*1.496*10**11
    DECstdM = DECstd/(1000.0*3600.0)*np.pi/180.0*dist*1.496*10**11
    print("\033[32mRA std = {0:.3f}".format(RAstd))
    print("DEC std = {0:.3f}".format(DECstd))
    print("RA std = {0:.3f}".format(RAstdM))
    print("DEC std = {0:.3f}\033[0m".format(DECstdM))
    
    """
    RArms = np.sqrt(np.mean(np.square((RA[2]-centerRA)*(360/(23+56/60+4.1/3600)*np.cos(np.deg2rad(DECmean))))))*1000
    DECrms = np.sqrt(np.mean(np.square(DEC[2]-centerDEC)))*1000
    RArmsM = RArms/(1000.0*3600.0)*np.pi/180.0*dist*1.496*10**11
    DECrmsM = DECrms/(1000.0*3600.0)*np.pi/180.0*dist*1.496*10**11

    print('\033[32mRA rms = {0} mas'.format(RArms))
    print('DEC rms = {0} mas'.format(DECrms))
    print('RA rms = {0} meter'.format(RArmsM))
    print('DEC rms = {0} meter\033[0m'.format(DECrmsM))
    """
    RAline = plt.errorbar(timeList, displacementRA, yerr=errRA,color='red',marker='o', linestyle='', markersize=3, label='RA')
    DECline = plt.errorbar(timeList, displacementDEC, yerr=errDEC, color='blue',marker='o',linestyle='', label='DEC', markersize = 3)
    plt.xlabel('Time')
    plt.ylabel('Displacement [mas]')
    plt.ylim(-10,10)
    plt.title('RA and DEC Offsets.')
    plt.grid(True)
    plt.figtext(0.2,0.2,"RA$\sigma$ = {0:.1f} m \nDEC$\sigma$ = {1:.1f} m ".format(RAstdM, DECstdM))
    #x0, x1, y0, y1 = plt.axis()
    #plt.axis([x0,x1,-10,10])
    plt.tight_layout()
    plt.margins(0.04,0.04)
    plt.legend()
    
    fig = plt.gcf()
    if raw_input("\033[33mWould you like to see the plot? \033[0m").upper() == 'YES':
        plt.show()
    fig.savefig(os.getcwd()+'/images_{0}/displacements.pdf'.format(date))
    
    with open(os.getcwd()+'/images_{0}/rms.txt'.format(date), 'w') as f:
        f.write("RA std = {0:.3f} mas".format(RAstd))
        f.write("\nDEC std = {0:.3f} mas".format(DECstd))
        f.write("\nRA std = {0:.3f} meter".format(RAstdM))
        f.write("\nDEC std = {0:.3f} meter".format(DECstdM))

if __name__ == '__main__':
    plot()
