from AIPS import AIPS
from AIPSTask import AIPSTask, AIPSList
from AIPSData import AIPSUVData, AIPSImage
import sys, time, os, cleaner
from subprocess import call

def main(**args):
    args["date"] = "{0}{1}".format(time.strftime("%d"), time.strftime("%B"))
    args["logFile"] = "./images_{0}/log.txt".format(args["date"])

    if not os.path.exists("./images_{0}".format(args["date"])):
        os.makedirs("./images_{0}".format(args["date"]))
    #if os.path.isfile('./images_{0}/locations.txt'.format(args["date"])):
    #    os.remove('./images_{0}/locations.txt'.format(args["date"]))
    #if os.path.isfile('./images_{0}/badtimes.txt'.format(args["date"])):
    #    os.remove('./images_{0}/badtimes.txt'.format(args["date"]))

    AIPS.log = open(args["logFile"], 'a')

    for k,j in enumerate(args["timeSections"],start=1):
        #------------------------------------

        if k == 1:
            args["refTelly"] = 11
            args["numBoxes"] = 6
            args["cleanBoxCoords"] = [[None,124.0,125.0,133.0,132.0], [None,133.0,115.0,141.0,129.0],\
                                      [None,122.0,132.0,131.0,140.0], [None,124.0,119.0,133.0,125.0],\
                                      [None,131.0,128.0,140.0,136.0], [None,141.33,114.0,145.67,124.0]]
            args["fitBox"] = [None,129.33,120.67,141.67,132.33]
            args["timeList"] = 'timeranges.list.1'

            args["time"] = AIPSList(j) 
            cleaned1 = cleaner.Cleaner(k, **args)
        elif k == 2:
            args["refTelly"] = 16
            args["numBoxes"] = 3
            args["cleanBoxCoords"] = [[None,121.00,114.00,136.00,146.00],[None,136.00,106.00,144.00,133.00],\
                                      [None,113.67,146.00,133.6,152.33]]
            args["fitBox"] = [None,129.00,101.00,141.33,132.67]
            args["timeList"] = 'timeranges.list.2'
            args["time"] = AIPSList(j) 
            cleaned1 = cleaner.Cleaner(k, **args)
        if k == 3:
            args["refTelly"] = 25
            args["numBoxes"] = 2
            args["cleanBoxCoords"] = [[None,74.00,79.00,189.00,176.00],[None,187.33,69.00,250.67,132.33]]
            args["fitBox"] = [None,134.00,114.67,174.33,149.00]
            args["timeList"] = 'timeranges.list.3'
            #------------------------------------
            args["time"] = AIPSList(j) 
            cleaned3 = cleaner.Cleaner(k, **args)
   



if __name__ == "__main__":
    args = dict()
    #------------------------------------
    args["flagPath"] = "PWD:flagout"
    args["bchan"] = 30
    args["echan"] = 240
    args["achan"] = 211
    args["antPath"] = "PWD:NEW.antab"
    args["timeSections"] = [[0,18,59,30, 1,3,46,30], [1,2,1,30, 1,9,0,30], \
                           [1,8,18,30, 1,18,30,0]] 
    args["user"] = 916
    args["name"] = "gr035"
    args["dataPath"] = "PWD:gr035.sb5.idi"
    args["fileCount"] = 6
    args["cal"] = "J1232-0224"
    args["inseq"] = 1
    args["source"] = "MEX"
    args["bandPass"] = "J1222+0413"
    args["bandPassCal"] = "J1222+0413"
    #------------------------------------

    startTime = time.time()
    main(**args)
    print("\n--  {0} --\n".format(time.time()-startTime))
    call(["/astroware/bin/python2.7","ploter.py"]) #need to use special python for matpltlib
    #------------------------------------

