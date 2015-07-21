import sys, os, time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import numpy as np 
from datetime import datetime

centerRA  = 59.60
centerDEC = 55.00

def plot():
    timeList = [];
    RAhour = []; RAmin = []; RAsec = []; RAerror = [];
    DECdeg = []; DECmin = []; DECsec = []; DECerror = [];
    
    date = "{0}{1}".format(time.strftime("%d"), time.strftime("%B"))
    with open(os.getcwd() + '/images_{0}/locations.txt'.format(date), 'r') as f:
        for l in f.readlines():
            [imgnameTemp, RAhourT, RAminT, RAsecT, RAerrorT, \
             DECdegT, DECminT, DECsecT, DECerrorT] = l.split()
            day = int(imgnameTemp[0])
            hour = int(imgnameTemp[1:3])
            minutes = int(imgnameTemp[3:5])
            timeList.append(datetime(2013, 12, 28 + day, hour, minutes))
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
        displacementRA.append(((RA[2][q] - centerRA)*(360/(23+56.0/60.0+4.1/3600)*np.cos(np.deg2rad(DECmean))))*1000.0)
        errRA.append((RA[3][q]**(360/(23+56.0/60.0+4.1/3600)*np.cos(np.deg2rad(DECmean))))*1000.0)
        displacementDEC.append((DEC[2][q] - centerDEC)*1000.0)
        errDEC.append(DEC[3][q]*1000.0)
        
    RAstd = np.std((RA[2]-centerRA)*(360.0/(23+56.0/60+4.1/3600)*np.cos(np.deg2rad(DECmean))))
    DECstd = np.std(np.square(DEC[2]-centerDEC))
    print("RA std = {0}".format(RAstd))
    print("DEC std = {0}".format(DECstd))

    RAline = plt.errorbar(timeList, displacementRA, yerr=errRA,color='red',marker='o', linestyle='', markersize=3, label='RA')
    DECline = plt.errorbar(timeList, displacementDEC, yerr=errDEC, color='blue',marker='o',linestyle='', label='DEC', markersize = 3)
    plt.xlabel('Time')
    plt.ylabel('Displacement [mas]')
    plt.ylim(-10,10)
    plt.title('RA and DEC Offsets.')
    plt.grid(True)
    #x0, x1, y0, y1 = plt.axis()
    #plt.axis([x0,x1,-10,10])
    plt.tight_layout()
    plt.margins(0.04,0.04)
    plt.legend()
    fig = plt.gcf()
    if raw_input("Would you like to see the plot? ").upper() == 'YES':
        plt.show()
    fig.savefig(os.getcwd()+'/images_{0}/displacements.pdf'.format(date))
    

if __name__ == '__main__':
    plot()
