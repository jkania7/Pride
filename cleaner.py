from AIPS import AIPS
from AIPSTask import AIPSTask, AIPSList
from AIPSData import AIPSUVData, AIPSImage
import argparse, sys, location_finder, os

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
        cleaninseq = iterNum
        imageClean = AIPSImage(self.args["name"], 'ICL001', 1, cleaninseq)
        imageDirty = AIPSImage(self.args["name"], 'IBM001', 1, cleaninseq)
        flag = AIPSUVData(self.args["name"], 'TASAV', 1, 100)
        if uvdata.exists() and iterNum == 1:
            print("Data is already present")
            ans1 = raw_input('\033[33mDo you want to zap the data (yes/no)? \033[0m').upper()
            if ans1 == 'YES':
                print("Zapping data and reloading.")
                uvdata.clrstat()
                uvdata.zap()

                fitld = AIPSTask('fitld')
                fitld.datain = self.args["dataPath"]
                fitld.outname = self.args["name"]
                fitld.outseq = self.args["inseq"]
                fitld.ncount = self.args["fileCount"]
                fitld.doconcat = 1

                #fitldFL = AIPSTask("FITLD")
                #fitldFL.datain = args["flagPath"]
                #fitldFL.outname = self.args["name"]
                #fitldFL.outseq = 100
                #fitldFL.ncount = 1
                #fitldFL.go()

                snVers = 0
                clVers = 1
                fitld.go()
            else:
                ans2 = raw_input('\033[33mDo you want to zap the tables and images(yes/no)? \033[0m').upper()
                if ans2 == 'YES':
                    print("Zapping tables/images.")
                    uvdata.clrstat()
                    uvdata.zap_table('SN', -1)
                    uvdata.zap_table('FL', -1)
                    tablesToDelete = 0
                    for i in uvdata.tables:
                        if i[1] == 'AIPS CL' and i[0]>tablesToDelete:
                            tablesToDelete = i[0]
                    for k in range(tablesToDelete,1,-1):
                        uvdata.zap_table('CL', k)

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
                    sys.exit()
        elif not uvdata.exists():

            print("Loading data")
            fitld = AIPSTask('fitld')
            fitld.datain = self.args["dataPath"]
            fitld.outname = self.args["name"]
            fitld.outseq = self.args["inseq"]
            fitld.ncount = self.args["fileCount"]
            fitld.doconcat = 1
            fitld.go()

            #fitldFL = AIPSTask("FITLD")
            #fitldFL.datain = args["flagPath"]
            #fitldFL.outname = self.args["name"]
            #fitldFL.outseq = 100
            #fitldFL.ncount = 1
            #fitldFL.go()

            snVers = 0
            clVers = 1
        else:
            snVers = 0
            clVers = 0
            for i in uvdata.tables:
                if i[1] == 'AIPS SN' and i[0] > snVers:
                    snVers = i[0]
                if i[1] == 'AIPS CL' and i[0] > clVers:
                    clVers = i[0]
            print("Setting SN table version to {0}".format(snVers))
            print("Setting CL table version to {0}".format(clVers))
            uvdata.zap_table('SN', -1)
            for k in range(clVers,1,-1):
                uvdata.zap_table('CL', k)
            snVers = 0
            clVers = 1
        if imageClean.exists():
            imageClean.clrstat()
            imageClean.zap()
        if imageDirty.exists():
            imageDirty.clrstat()
            imageDirty.zap()
        if flag.exists():
            flag.clrstat()
            flag.zap()
        """
        fitldFL = AIPSTask("FITLD")
        fitldFL.datain = args["flagPath"]
        fitldFL.outname = self.args["name"]
        fitldFL.outseq = 100
        fitldFL.ncount = 1
        fitldFL.go()

        print("Copying flagging")                
        tacop = AIPSTask("TACOP")
        tacop.indata = flag
        tacop.invers = 3
        tacop.ncount = 1 
        tacop.outname = self.args["name"]
        tacop.outseq = self.args["inseq"]
        tacop.outclass = 'UVDATA'
        tacop.outdisk = 1
        tacop.outver = 0
        tacop.inext = 'FG'
        tacop.go()        
        
        uvdata.zap_table('BP', -1) #create a new bp table for each reftelly
        print("Running bandpass")
        bpass = AIPSTask('BPASS')
        bpass.indata = uvdata
        bpass.calsour[1] = self.args["bandPassCal"]
        bpass.timer = self.args["time"]
        bpass.refant = self.args["refTelly"]
        bpass.go()
        
        uvdata.zap_table('TY', -1)
        uvdata.zap_table('GC', -1)
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
        """
        print("Running Fring.")
        fring = AIPSTask('fring') #finds fringes
        fring.indata = uvdata
        fring.docalib = 1
        fring.gainuse = clVers
        fring.calsour[1] = self.args["cal"]
        fring.bchan = self.args["bchan"]
        fring.echan = self.args["echan"]
        fring.timer = self.args["time"]
        fring.refant = self.args["refTelly"]
        #fring.doband = 1
        #fring.bpver = 1
        fring.go()
        
        snVers = snVers + 1
        SN = 0
        for i in uvdata.tables:
            if i[1] == 'AIPS SN' and i[0]>SN:
                SN = i[0]
        if not SN == snVers:
            sys.exit("SN table number missmatch")
        print("Fring created SN table {0}".\
              format(snVers))

        
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
        #clcal.interpol = "ambg"
        #clcal.opcode = "calp"
        clcal.refant = self.args["refTelly"]
        clcal.go()
        """
        clcal.snver = snVers
        clcal.inver = snVers
        clcal.gainver = clVers
        clcal.go()
        """
        CL = 0
        clVers = clVers + 1 
        clFring = clVers
        for i in uvdata.tables:
            if i[1] == 'AIPS CL' and i[0]>CL:
                CL = i[0]
        if not CL == clVers:
            sys.exit("CL table number missmatch")
        print("Clcal created CL table {0}".\
              format(clVers))

        #determines calibration, creates new SN
        print("Running calib")
        calib = AIPSTask('calib')
        calib.indata = uvdata
        calib.calsour[1] = self.args["cal"]
        calib.docalib = 1
        calib.gainuse = clVers
        calib.smodel[1] = 1
        calib.solint = 0.2
        calib.soltype = 'L1'
        calib.solmode = 'P'
        #calib.doband = 1
        #calib.bpver = 1
        calib.timer = self.args["time"]
        calib.refant = self.args["refTelly"]
        calib.go()

        snVers = snVers + 1
        SN = 0
        for i in uvdata.tables:
            if i[1] == 'AIPS SN' and i[0]>SN:
                SN = i[0]
        if not SN == snVers:
            sys.exit("SN table number missmatch")
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
        CL = 0
        for i in uvdata.tables:
            if i[1] == 'AIPS CL' and i[0]>CL:
                CL = i[0]
        if not CL == clVers:
            sys.exit("CL table number missmatch")
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
        imagr.bchan = self.args["bchan"]
        imagr.echan = self.args["echan"]
        imagr.nchav = self.args["achan"]
        #imagr.doband = 1
        #imagr.bpver = 1
        imagr.cellsize = AIPSList([0.0001,0.0001])
        imagr.imsize = AIPSList([256,256])
        imagr.nboxes = len(self.args["CalCleanBox"])
        imagr.clbox[1:] = self.args["CalCleanBox"]
        imagr.niter = 1000
        imagr.go()
        print("Done with imagr")
       
        #to get last positive row
        latestImgTable = 0
        for j in imageClean.tables:
            if j[1] == 'AIPS CC' and j[0]>latestImgTable:
                latestImgTable = j[0]
        ccTable = imageClean.table('CC', latestImgTable)
        for row, i in enumerate(ccTable, start=2): #start @ 2 to get last positive
            if i['flux']<0:
                lastPositive = row
                break
        print("The last positive component number is: {0}".\
              format(lastPositive))

        print("Running Calib")
        calibSelf = AIPSTask('calib')
        calibSelf.in2data = imageClean 
        calibSelf.indata = uvdata
        calibSelf.calsour[1] = self.args["cal"]
        calibSelf.docalib = 1
        calibSelf.gainuse = clFring
        calibSelf.solint = 0.2
        calibSelf.soltype = 'L1'
        calibSelf.solmode = 'A&P'
        calibSelf.ncomp[1] = lastPositive
        calibSelf.timer = self.args["time"]
        #calibSelf.doband = 1
        #calibSelf.bpver = 1
        calibSelf.go()
        snVers = snVers + 1
        SN = 0
        for i in uvdata.tables:
            if i[1] == 'AIPS SN' and i[0]>SN:
                SN = i[0]
        if not SN == snVers:
            print("SN = {0} , snVers = {1}".format(SN, snVers))
            sys.exit("SN table number missmatch")


        print("calibSelf created SN table {0}".format(snVers))

        #makes contour plot
        kntr = AIPSTask('KNTR')
        kntr.indata = imageClean
        kntr.levs = AIPSList([2,3,4,5,7,10,13,17])
        kntr.dogrey = -1
        kntr.dotv = -1 
        kntr.dovect = - 1 
        #kntr.blc[1] = .80*self.args["fitBox"][1]
        #kntr.blc[2] = .80*self.args["fitBox"][2]
        #kntr.trc[1] = 1.20*self.args["fitBox"][3]
        #kntr.trc[2] = 1.20*self.args["fitBox"][4]
        kntr.go()
        

        lwmp = AIPSTask('LWPLA')
        lwmp.indata = imageClean
        lwmp.plver = 1
        lwmp.invers = 1
        lwmp.outfile = os.getcwd() + '/images_{0}/{1}_run{2}'.format(self.args["date"],self.args["cal"],self.iterNum) + '.ps'
        lwmp.go()

        print("Running clcal")
        clcal.snver = snVers
        clcal.inver = snVers
        clcal.sources[1] = self.args["cal"]
        clcal.calsour[1] = self.args["cal"] 
        clcal.gainver = clVers
        print("clVers = {0}".format(clVers))
        clcal.go() #Apply only to cal
        clVers = clVers + 1
        CL = 0
        for i in uvdata.tables:
            if i[1] == 'AIPS CL' and i[0]>CL:
                CL = i[0]
        if not CL == clVers:
            sys.exit("CL table number missmatch")
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
        print("clFring = {0}".format(clFring))
        clcalFinal.go()

        clVers = clVers +1
        CL = 0
        for i in uvdata.tables:
            if i[1] == 'AIPS CL' and i[0]>CL:
                CL = i[0]
        if not CL == clVers:
            sys.exit("CL table number missmatch")
        print("clcalFinal created CL table {0}".format(clVers))

        loc = location_finder.Location_finder(clVers, **self.args)
        imageClean.zap()
        imageDirty.zap()
        #flag.zap()
        
        with open(os.getcwd() + '/images_{0}/params{1}.txt'.format(self.args["date"],self.iterNum),'w') as f:
            for l in self.args:
                f.write("\n{0}".format(l))

if __name__ == "__main__":
    sys.exit("This model is not designed to be run by itself, you must use clean.py.")
