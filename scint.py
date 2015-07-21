
filename = "ScintObsSummaryTab_r103.txt"

import matplotlib.pyplot as plt
import os
from datetime import datetime
import numpy as np 

Obs = []; Run = []; Scan = []; StName = []; Time = [];
Dwell = []; RA = []; DEC = []; Az = []; El = []; 
SOT = []; Dist = []; EclObsLat = []; EclObsLong = [];
SysNrad = []; Scint = []; Broad = []; ScintSlope = [];
ScintSlopeErr = []; PeakSPD = []; SysNLev = []; 
SolarActivity1 = []; SolarActivity2 = []; 
IonoTECVEX = []; IonoTECCebre = []; IPS = [];


with open(os.getcwd()+'/'+filename, 'r') as f:
    for l in f.readlines():
        if not l[0:2] == '//':
            [line1, tObs, tRun, tScan, tStName, tYY, tMM, \
             tDD, thh, tmm, tss, tDwell, tRAdeg, tRAmin, \
             tRAsec, tDECdeg, tDECmin, tDECsec, tAz, tEl, \
             tSOT, tDist, tEclObsLat, tEclObsLong, line2, \
             tSysNrad, tScint, tBroad, tScintSlope, \
             tScintSlopeErr, tPeakSPD, tSysNLev, \
             tSolarActivity1, tSolarActivity2, tIonoTECVEX, \
             tIonoTECCebre, tIPS, line3] = l.split()
            Obs.append(int(tObs))
            Run.append(int(tRun))
            Scan.append(int(tScan))
            StName.append(int(tStName))
            Time.append(datetime(int(tYY), int(tMM), int(tDD), \
                                 int(thh), int(tmm), int(tss)))
            Dwell.append(int(tDwell))
            tDEC = int(tDECdeg) + float(tDECmin)/60.0 + float(tDECsec)/3600;
            DEC.append(tDEC)
            RA.append((int(tRAdeg) + float(tRAmin)/60.0+\
                       float(tRAsec)/3600.0)*(23+56.0/60.0+4.1/3600)*np.cos(np.deg2rad(tDEC)))
            Az.append(float(tAz))
            El.append(float(tEl))
            SOT.append(float(tSOT))
            Dist.append(float(tDist))
            EclObsLat.append(float(tEclObsLat))
            EclObsLong.append(float(tEclObsLong))
            SysNrad.append(float(tSysNrad))
            Scint.append(float(tScint))
            Broad.append(float(tBroad))
            ScintSlope.append(float(tScintSlope))
            ScintSlopeErr.append(float(tScintSlopeErr))
            PeakSPD.append(float(tPeakSPD))
            SysNLev.append(float(tSysNLev))
            SolarActivity1.append(float(tSolarActivity1))
            SolarActivity2.append(float(tSolarActivity2))
            IonoTECVEX.append(float(tIonoTECVEX))
            IonoTECCebre.append(float(tIonoTECCebre))
            IPS.append(float(tIPS))
            
ax1 = plt.scatter(SOT, IPS, color='red', marker='o')
plt.xlabel("SOT")
plt.ylabel("IPS")
plt.show()
