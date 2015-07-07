from AIPS import AIPS
from AIPSTask import AIPSTask, AIPSList
from AIPSData import AIPSUVData, AIPSImage
import argparse, sys, time, os, cleaner
from subprocess import call
vers="v1.0.1"
"""This is to parse the command line arguments and contol the cleaning"""

def main(**args):
    
    print("\nThanks for all the fish! Now cleaning with {0}.\n".format(vers))

    args["date"] = "{0}{1}".format(time.strftime("%d"), time.strftime("%B"))
    if not os.path.exists("./images_{0}".format(args["date"])):
        os.makedirs("./images_{0}".format(args["date"]))
    if os.path.isfile('./images_{0}/locations.txt'.format(args["date"])):
        os.remove('./images_{0}/locations.txt'.format(args["date"]))
    if os.path.isfile('./images_{0}/badtimes.txt'.format(args["date"])):
        os.remove('./images_{0}/badtimes.txt'.format(args["date"]))

    args["bchan"] = 30
    args["echan"] = 240
    args["antPath"] = "PWD:NEW.antab"
    args["flagPath"] = "PWD:flagout1"
    logFile = "./images_{0}/log.txt".format(args["date"])
    AIPS.log = open(logFile, 'a')
    timelist = [[0,18,59,30, 1,3,46,30], [1,2,1,30, 1,9,0,30], [1,8,18,30, 1,18,30,0]] 
    for k,j in enumerate(timelist,start=1):
        if k == 1:
            args["refTelly"] = 11
            args["numBoxes"] = 6
            args["cleanBoxCoords"] = [[None,124.0,125.0,133.0,132.0], [None,133.0,115.0,141.0,129.0],\
                                      [None,122.0,132.0,131.0,140.0], [None,124.0,119.0,133.0,125.0],\
                                      [None,131.0,128.0,140.0,136.0], [None,141.33,114.0,145.67,124.0]]
            args["fitBox"] = [None,129.33,120.67,141.67,132.33]
            args["timeList"] = 'timeranges.list.1'
        elif k == 2:
            sys.exit()
            args["refTelly"] = 16
            args["numBoxes"] = 3
            args["cleanBoxCoords"] = [[None,121.00,114.00,136.00,146.00],[None,136.00,106.00,144.00,133.00],\
                                      [None,113.67,146.00,133.6,152.33]]
            args["fitBox"] = [None,129.00,101.00,141.33,132.67]
            args["timeList"] = 'timeranges.list.2'
        elif k == 3:
            args["refTelly"] = 25
            args["numBoxes"] = 2
            args["cleanBox"] = [[None,74.00,79.00,189.00,176.00],[187.33,69.00,250.67,132.33]]
            args["fitBox"] = [None,134.00,114.67,174.33,149.00]
            args["timeList"] = 'timeranges.list.3'
        args["time"] = AIPSList(j) 
        cleaned = cleaner.Cleaner(k, **args)
    call(["/astroware/bin/python2.7","ploter.py"]) #need to use special python for matpltlib
if __name__ == "__main__":
    parser=argparse.ArgumentParser(
        description="Image cleaner for MEX",
        prog='clean.py',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    required=parser.add_argument_group('required arguments:')
    parser.add_argument('--user', type=int,help="User number for AIPS.",
                        required=True)
    parser.add_argument('--name', type=str, 
                        help="Internal file name for AIPS.",
                        required=True)
    parser.add_argument('--dataPath', type=str,
                        help="Path to the data.",
                        required=True)
    parser.add_argument('--fileCount', type=int,
                        help="Number of files to load.",
                        required=True)
    parser.add_argument('--cal', type=str,
                        help="Cal source.",
                        required=True)
    parser.add_argument('--inseq', type=int,
                        help="Inseq to start at.",
                        required=True)
    #parser.add_argument('--times', type=str,
    #                    help="Path to file containing the times",
    #                    required=True)
    parser.add_argument('--source', type=str,
                        help="Source to be imaged",
                        required=True)
    parser.add_argument('--bandPassCal', type=str,
                        help="Source to do band pass calibration on",
                        required=True)
    args = vars(parser.parse_args())
    main(**args)
