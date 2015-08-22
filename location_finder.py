from AIPS import AIPS
from AIPSTask import AIPSTask, AIPSList
from AIPSData import AIPSUVData, AIPSImage
import sys, os, ParallelTask
vers="v1.0.0"
class Location_finder(object):
    def __init__(self, clVers, **args):
        self.clVers = clVers
        self.args = args
        self.clVers = 3
        AIPS.userno=self.args["user"]
        uvdata = AIPSUVData(self.args["name"], 'UVDATA', 1, self.args["inseq"])
        t = [] #files t with [day, hour, min, sec, day, hour, min, sec]
        with open(self.args["timeList"], 'r') as f:
            for l in f.readlines():
                t.append(map(str,l.split()[1:9]))
        
        
        for j in t:
            realtime = ''.join([j[i] for i in range(len(j))])[0:7]
            imgname = realtime[0:5]
            #need to shorten the names for AIPS
            imagr = AIPSTask('IMAGR')
            imagr.indata = uvdata
            imagr.sources[1] = self.args["source"]
            imagr.docalib = 1
            imagr.gainuse = self.clVers
            imagr.bchan = self.args["SCbchan"]
            imagr.echan = self.args["SCechan"]
            imagr.nchav = (self.args["SCechan"] - self.args["SCbchan"] + 1)
            #averages over all channels
	    if self.args["doBP"]:
	      imagr.doband = 1	
	      imagr.bpver = 1
            if self.args["excludeTelly"]:
                imagr.antennas[1:] = self.args["excludedTellys"]
            imagr.outname = imgname
            imagr.outseq = 1
            imagr.cellsize = AIPSList([0.0001,0.0001])
            imagr.imsize = AIPSList([1024,1024])
            #imagr.imsize = AIPSList([256,256])
            imagr.nboxes = 1
            imagr.clbox[1] = self.args["fitBox"]
            imagr.niter = 1000
            imagr.timerang[1:] = [int(j[i]) for i in range(len(j))]#AIPSList(j)
            good = True
            
            try:
                imagr.go()
            except RuntimeError as e:
                print("\nSomething went wrong!\n  => {0}".format(e))
                with open(os.getcwd() + '/images_{0}/badtimes.txt'.format(self.args["date"]), 'a') as out:
                    out.write("{0}\n".format(imgname))
                good = False
            if good:
                imageClean = AIPSImage(imgname, 'ICL001',1,1)
                imageDirty = AIPSImage(imgname, 'IBM001',1,1)
                imageClean.clrstat() #makes sure AIPS does not trip
                imageDirty.clrstat()

                jmfit = AIPSTask('JMFIT')
                jmfit.indata = imageClean
                jmfit.blc[1] = .80*self.args["fitBox"][1]#fraction to increase box size
                jmfit.blc[2] = .80*self.args["fitBox"][2]
                jmfit.trc[1] = 1.20*self.args["fitBox"][3]
                jmfit.trc[2] = 1.20*self.args["fitBox"][4]
                jmfit.niter = 1000
                jmfit.doprint = 1 #CHANGED TO doprint!  
                address = os.getcwd() + '/images_{0}/'.format(self.args["date"]) + realtime
                jmfit.fitout = address + '.crd'
                jmfit.go()

                RA = [None]*4 #holds locations
                DEC = [None]*4
                with open(address + '.crd', 'r') as f:
                    for l in f.readlines():
                        temp = l.split()
                        #for j in range(len(temp)):
                        if len(temp)>0:
                            if temp[0] == 'RA':
                                RA[0] = int(temp[1])
                                RA[1] = int(temp[2])
                                RA[2] = float(temp[3])
                                RA[3] = float(temp[5])
                            elif temp[0] =='DEC':
                                DEC[0] = int(temp[1])
                                DEC[1] = int(temp[2])
                                DEC[2] = float(temp[3])
                                DEC[3] = float(temp[5])
                                

                with open(os.getcwd() + '/images_{0}/locations.txt'.format(self.args["date"]), 'a') as out:
                    out.write("{0}\t{1}\t{2}\t{3:^10}\t{4:^6}\t{5}\t{6}\t{7:^7}\t{8}\n".
                              format(realtime, RA[0], RA[1], RA[2], RA[3], \
                                     DEC[0], DEC[1], DEC[2], DEC[3]))
                #makes contour plot
                kntr = AIPSTask('KNTR')
                kntr.indata = imageClean
                kntr.levs = AIPSList([2,3,4,5,7,10,13,17])
                kntr.dogrey = -1
                kntr.dotv = -1 
                kntr.dovect = -1 
                #kntr.blc[1] .80*self.args["fitBox"][1]
                #kntr.blc[2] .80*self.args["fitBox"][2]
                #kntr.trc[1] 1.20*self.args["fitBox"][3]
                #kntr.trc[2] 1.20*self.args["fitBox"][4]
                kntr.go()
                
                lwmp = AIPSTask('LWPLA')
                lwmp.indata = imageClean
                lwmp.plver = 1
                lwmp.invers = 1
                if good:
                    lwmp.outfile = address +  '.ps'
                else:
                    lwmp.outfile = address  + '_bad.ps'
                lwmp.go()

                imageClean.zap()
                imageDirty.zap()
            
                
if __name__ == "__main__":
    sys.exit("This model is not designed to be run by itself, you must use clean.py.")
