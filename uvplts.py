"""
Created on 23 July 2015 by jwkania to plot uvcoverages
"""
from AIPS import AIPS
from AIPSTask import AIPSTask, AIPSList
from AIPSData import AIPSUVData, AIPSImage
from subprocess import call
import os
AIPSTask.msgkill = 3
AIPS.userno = 916
uvdata = AIPSUVData('gr035', 'UVDATA', 1, 1)

for i,t in enumerate([[None,0], [None,0,18,59,30, 1,3,46,30], [None,1,2,1,30, 1,9,0,30], \
                      [None,1,8,18,30, 1,18,30,0]],start=0): 
    uvdata.zap_table('PL', -1)
    uvplt = AIPSTask('UVPLT')
    uvplt.timerang = t
    uvplt.indata = uvdata
    uvplt.bchan = 1
    uvplt.echan = 256
    uvplt.nchav = 256
    #uvplt.docalib = 1
    #uvplt.gainuse = 1 
    #uvplt.doband = 1
    #uvplt.bpver = 1
    uvplt.bparm = AIPSList([6, 7])
    uvplt.dotv = -1 
    uvplt.xinc = 20
    uvplt.go()

    lwpla = AIPSTask('LWPLA')
    lwpla.indata = uvdata
    lwpla.plver = 1
    lwpla.outfile = 'PWD:uvplt_time{0}.ps'.format(i)
    lwpla.go()
    """
    pwd = os.getcwd()
    p = "{0}/uvplt_time*.ps".format(pwd)
    print p
    call("ps2pdf","uvplt_time*.ps" )
    """
