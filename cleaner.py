from AIPS import AIPS
from AIPSTask import AIPSTask, AIPSList
from AIPSData import AIPSUVData, AIPSImage
import argparse, sys, location_finder

vers="v1.0.1"
"""This model does the image cleaning"""
class Cleaner(object):
    def __init__(self, iterNum, **args):
        self.iterNum = iterNum
        self.args = args
            
        AIPS.userno=self.args["user"]#username
        snInit = 0
        clInit = 1

        AIPSTask.msgkill = -5 #makes the output less verbose
        uvdata = AIPSUVData(self.args["name"], 'UVDATA', 1, self.args["inseq"])
        imgClean = AIPSImage(self.args["name"], 'ICL001', 1, self.args["inseq"])
        imgDirty = AIPSImage(self.args["name"], 'IBM001', 1, self.args["inseq"])
        
        if uvdata.exists() and iterNum == 1:
            print("Data is already present")
            ans1 = raw_input('Do you want to zap the data (yes/no)? ').upper()
            if ans1 == 'YES':
                print("Zapping data and reloading.")
                uvdata.clrstat()
                uvdata.zap()
                if imgClean.exists():
                    imgClean.clrstat()
                    imgClean.zap()
                if imgDirty.exists():
                    imgDirty.clrstat()
                    imgDirty.zap()
                fitld = AIPSTask('fitld')
                fitld.datain = self.args["dataPath"]
                fitld.outname = self.args["name"]
                fitld.outseq = self.args["inseq"]
                fitld.ncount = self.args["fileCount"]
                fitld.doconcat = 1
                snVers = 0
                clVers = 1
                fitld.go()
            else:
                ans2 = raw_input('Do you want to zap the tables and images(yes/no)? ').upper()
                if ans2 == 'YES':
                    print("Zapping tables/images.")
                    uvdata.clrstat()
                    uvdata.zap_table('SN', -1)
                    uvdata.zap_table('BP', -1)
                    uvdata.zap_table('TY', -1)
                    uvdata.zap_table('GC', -1)
                    tablesToDelete = 0
                    for i in uvdata.tables:
                        if i[1] == 'AIPS CL' and i[0]>tablesToDelete:
                            tablesToDelete = i[0]
                    for k in range(tablesToDelete,1,-1):
                        uvdata.zap_table('CL', k)
                    if imgClean.exists():
                        imgClean.clrstat()
                        imgClean.zap()
                    if imgDirty.exists():
                        imgDirty.clrstat()
                        imgDirty.zap()
                    snVers = 0
                    clVers = 1
                else:
                    print("Going direclty to imaging.")
                    """
                    snVers = 0
                    clVers = 0
                    for i in uvdata.tables:
                        if i[1] == 'AIPS SN' and i[0] > snVers:
                            snVers = i[0]
                        if i[1] == 'AIPS CL' and i[0] > clVers:
                            clVers = i[0]
                    """
                    clVers = int(raw_input("What cl table would you like to use? "))
                    loc = location_finder.Location_finder(clVers, **self.args)
        elif not uvdata.exists():
            if imgClean.exists():
                imgClean.clrstat()
                imgClean.zap()
            if imgDirty.exists():
                imgDirty.clrstat()
                imgDirty.zap()
            print("Loading data")
            fitld = AIPSTask('fitld')
            fitld.datain = self.args["dataPath"]
            fitld.outname = self.args["name"]
            fitld.outseq = self.args["inseq"]
            fitld.ncount = self.args["fileCount"]
            fitld.doconcat = 1
            snVers = 0
            clVers = 1
            fitld.go()
        else:
            snVers = 0
            clVers = 0
            for i in uvdata.tables:
                if i[1] == 'AIPS SN' and i[0] > snVers:
                    snVers = i[0]
                if i[1] == 'AIPS CL' and i[0] > clVers:
                    clVers = i[0]
                
        print("Running bandpass")
        bpass = AIPSTask('BPASS')
        bpass.indata = uvdata
        bpass.calsour[1] = self.args["bandPassCal"]
        bpass.timer = self.args["time"]
        bpass.refant = self.args["refTelly"]
        bpass.go()

        print("Running antab")
        antab = AIPSTask('ANTAB')
        antab.indata = uvdata
        antab.calin = self.args["antPath"]
        antab.go()
        
        print("Running apcal")
        apcal = AIPSTask('APCAL')
        apcal.indata = uvdata
        apcal.timer = self.args["time"]
        apcal.tyver = 1
        apcal.gcver = 1
        apcal.go()
        
        snVers = snVers + 1
        print("apcal made snVers {0}".format(snVers))
        
        #applies new SN table to CL
        print("Running clcal.")
        clcal = AIPSTask('clcal') 
        clcal.indata = uvdata
        clcal.calsour[1] = self.args["cal"]
        clcal.timerang = self.args["time"]
        clcal.snver = snVers
        clcal.inver = snVers
        clcal.gainver = clInit #apply to original cl
        clcal.timer = self.args["time"]
        clcal.interpol = "ambg"
        clcal.opcode = "calp"
        clcal.refant = self.args["refTelly"]
        clcal.go()

        clVers = clVers + 1
        print("clcal made cl table {0}".format(clVers))

        print("Running Fring.")
        fring = AIPSTask('fring') #finds fringes
        fring.indata = uvdata
        fring.calsour[1] = self.args["cal"]
        fring.bchan = self.args["bchan"]
        fring.echan = self.args["echan"]
        fring.timer = self.args["time"]
        fring.refant = self.args["refTelly"]
        fring.doband = 1
        fring.bpver = 1
        fring.go()

        snVers = snVers + 1
        print("Fring created SN table {0}".\
              format(snVers))

        """
        #applies new SN table to CL
        print("Running clcal.")
        clcal = AIPSTask('clcal') 
        clcal.indata = uvdata
        clcal.calsour[1] = self.args["cal"]
        clcal.timerang = self.args["time"]
        clcal.snver = snVers
        clcal.inver = snVers
        clcal.gainver = clInit #apply to original cl
        clcal.timer = self.args["time"]
        clcal.interpol = "ambg"
        clcal.opcode = "calp"
        clcal.refant = self.args["refTelly"]
        clcal.go()
        """
        clcal.snver = snVers
        clcal.inver = snVers
        clcal.gainver = clInit +1 #WHAT SHOULD THIS BE?
        clcal.go()
        
        clVers = clVers + 1 
        clFring = clVers
        print("Clcal created CL table {0}".\
              format(clVers))

        #determines calibration, creates new SN
        print("running calib")
        calib = AIPSTask('calib')
        calib.indata = uvdata
        calib.calsour[1] = self.args["cal"]
        calib.docalib = 1
        calib.gainuse = clVers
        calib.smodel[1] = 1
        calib.solint = 0.2
        calib.soltype = 'L1'
        calib.solmode = 'P'
        calib.doband = 1
        calib.bpver = 1
        calib.timer = self.args["time"]
        calib.refant = self.args["refTelly"]
        calib.go()

        snVers = snVers + 1
        print("Calib created SN table {0}".\
              format(snVers))

        #takes SN table created by calib and applies to CL
        print("Running clcal")
        clcal.sources[1] = self.args["cal"]
        clcal.snver = snVers
        clcal.inver = snVers
        clcal.gainver = clVers
        clcal.go() #Apply only to cal
        clVers = clVers + 1
        print("Clcal created CL table {0}".format(clVers))

        #cleans the image
        print("Running imagr")
        imagr = AIPSTask('IMAGR')
        imagr.indata = uvdata
        imagr.sources[1] = self.args["cal"]
        imagr.timerang = self.args["time"]
        imagr.docalib = 1
        imagr.outseq = iterNum #test to force it to make file
        imagr.gainuse = clVers
        imagr.bchan = 30
        imagr.echan = 240
        imagr.nchav = 211
        imagr.doband = 1
        imagr.bpver = 1
        imagr.cellsize = AIPSList([0.0001,0.0001])
        imagr.imsize = AIPSList([256,256])
        imagr.nboxes = self.args["numBoxes"]
        imagr.clbox[1:] = self.args["cleanBoxCoords"]
        imagr.niter = 1000
        imagr.go()
 
        cleaninseq = iterNum
        imageclean = AIPSImage(self.args["name"], 'ICL001', 1, cleaninseq)
        
        #to get last positive row
        for j in imgClean.tables:
            if j[1] == 'AIPS CC':
                latestImgTable = j[0]
        ccTable = imgClean.table('CC', latestImgTable)
        for row, i in enumerate(ccTable, start=2): #start @ 2 to get last positive
            if i['flux']<0:
                lastPositive = row
                break
        print("The last positive component number is: {0}".\
              format(lastPositive))

        print("Running Calib")
        calibSelf = AIPSTask('calib')
        calibSelf.in2data = imageclean 
        calibSelf.indata = uvdata
        calibSelf.calsour[1] = self.args["cal"]
        calibSelf.docalib = 1
        calibSelf.gainuse = clFring
        calibSelf.solint = 0.2
        calibSelf.soltype = 'L1'
        calibSelf.solmode = 'A&P'
        calibSelf.ncomp[1] = lastPositive
        calibSelf.timer = self.args["time"]
        calibSelf.doband = 1
        calibSelf.bpver = 1
        calibSelf.go()

        snVers = snVers + 1
        print("calibSelf created SN table {0}".format(snVers))

        #maked contour plot
        #kntr = AIPSTask('KNTR')
        #kntr.indata = imgClean
        #kntr.levs = AIPSList([-10,-5,-3,-1,0,1,2,3,5,10])
        #kntr.dogrey = -1
        #kntr.dotv = -1 
        #kntr.go()
        

        #lwmp = AIPSTask('LWPLA')
        
        print("Running clcal")
        clcal.snver = snVers
        clcal.inver = snVers
        clcal.gainver = clVers
        clcal.go() #Apply only to cal
        clVers = clVers + 1
        print("clcal created CL table {0}".format(clVers))

        print("Running clcal.")
        clcalFinal = AIPSTask('clcal') 
        clcalFinal.indata = uvdata
        clcalFinal.sources[1] = self.args["source"]
        clcalFinal.calsour[1] = self.args["cal"]
        clcalFinal.timerang = self.args["time"]
        clcalFinal.snver = snVers
        clcalFinal.inver = snVers
        clcalFinal.gainver = clFring
        clcalFinal.timer = self.args["time"]
        clcalFinal.refant = self.args["refTelly"]
        clcalFinal.go()

        clVers = clVers +1
        print("clcalFinal created CL table {0}".format(clVers))
        loc = location_finder.Location_finder(clVers, **self.args)

if __name__ == "__main__":
    sys.exit("This model is not designed to be run by itself, you must use clean.py.")
