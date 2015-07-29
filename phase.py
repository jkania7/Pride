from AIPS import AIPS
from AIPSTask import AIPSTask, AIPSList
from AIPSData import AIPSUVData, AIPSImage

time = AIPSList([1,8,18,30, 1,18,30,0])
AIPS.userno = 1010
uvdata = AIPSUVData('gr035', 'UVDATA', 1, 1)
if uvdata.exists():
    uvdata.zap()
fitld = AIPSTask('FITLD')
fitld.datain = 'PWD:gr035.sb5.idi'
fitld.outname = 'gr035'
fitld.outclass = 'UVDATA'
fitld.ncount = 6
fitld.doconcat = 1
#fitld.timer = time
fitld.go()

fring = AIPSTask('FRING')
fring.indata = uvdata
fring.calsour = AIPSList(['J1232-0224'])
fring.docalib = 1
fring.gainuse = 1
fring.timer = time
fring.go()

clcal = AIPSTask('clcal')
clcal.calsour = AIPSList(['J1232-0224'])
clcal.indata = uvdata
clcal.timer = time
clcal.go()




imagr = AIPSTask('IMAGR')
imagr.indata = uvdata
imagr.docal = 1
imagr.gainuse = 2
imagr.sources = AIPSList(['J1232-0224'])
imagr.dotv = 1
imagr.imsize = AIPSList([256,256])
imagr.cellsize = AIPSList([0.00001, 0.00001])
imagr.timer  = time
imagr.go()
