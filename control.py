"""



"""
from AIPS import AIPS
from AIPSTask import AIPSTask, AIPSList
from AIPSData import AIPSUVData, AIPSImage
import sys, time, os, cleaner
from subprocess import call

def main(**args):
    args["date"] = "{0}{1}".format(time.strftime("%d"), time.strftime("%B"))[0:5]
    args["logFile"] = "./images_{0}/log.txt".format(args["date"])

    if not os.path.exists("./images_{0}".format(args["date"])):
        os.makedirs("./images_{0}".format(args["date"]))
    #if os.path.isfile('./images_{0}/locations.txt'.format(args["date"])):
    #    os.remove('./images_{0}/locations.txt'.format(args["date"]))
    #if os.path.isfile('./images_{0}/badtimes.txt'.format(args["date"])):
    #    os.remove('./images_{0}/badtimes.txt'.format(args["date"]))

    AIPS.log = open(args["logFile"], 'a')

    for k,j in enumerate(args["timeSections"],start=1):
        if k == 1:
            args["refTelly"] = 10
            args["CalCleanBox"] = [[None,122.00,124.00,131.00,134.00], [None, 131.00,121.33,140.67,133.33]]
            args["fitBox"] = [None, 125.67,122.33,140.67,132.67]
            args["timeList"] = 'timeranges.list.1'
            args["SCbchan"] = 30
            args["SCechan"] = 240
            args["excludeTelly"] = True
            args["excludedTellys"] = [-7]
            args["time"] = AIPSList(j) 
            cleaned1 = cleaner.Cleaner(k, **args)
        elif k == 2:
            args["refTelly"] = 16
            args["CalCleanBox"] = [[None,123.00,117.00,132.00,141.00],[None,126.67,95.33,133.67,117.33]]
            args["fitBox"] = [None,131.00,98.67,143.67,134.00]
            args["timeList"] = 'timeranges.list.2'
            args["SCbchan"] = 130
            args["SCechan"] = 170
            args["excludeTelly"] = False 
            args["time"] = AIPSList(j) 
            cleaned2 = cleaner.Cleaner(k, **args)
        if k == 3:
            args["refTelly"] = 25
            args["CalCleanBox"] = [[None,122.00,121.00,135.00,140.00],[None,135.00,119.33,141.00,133.00]]
            args["fitBox"] = [None, 128.33,107.67,138.67,129.33]
            args["timeList"] = 'timeranges.list.3'
            args["SCbchan"] = 30
            args["SCechan"] = 240
            args["excludeTelly"] = False
            args["time"] = AIPSList(j) 
            cleaned3 = cleaner.Cleaner(k, **args)
    



if __name__ == "__main__":
    args = dict()
    #------------------------------------
    args["flagPath"] = "PWD:flagout"
    args["bchan"] = 30
    args["echan"] = 240
    args["antPath"] = "PWD:NEW.antab"
    args["timeSections"] = [[0,18,59,30, 1,3,46,30], [1,3,46,30, 1,18,18,30], \
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
    args["doBP"] = False
    #------------------------------------

    startTime = time.time()
    main(**args)
    print("\n--  {0} --\n".format(time.time()-startTime))
    call(["python","plotter.py"])
    #call(["/astroware/bin/python2.7","plotter.py"]) #need to use special python for matpltlib
    #------------------------------------

