from AIPS import AIPS
from AIPSTask import AIPSTask, AIPSList
from AIPSData import AIPSUVData, AIPSImage
from subprocess import call 

class Printer(object):
    def __init__(self, name, **args):
        
        


        lwpla = AIPSTask('LWPLA')
        image = AIPSImage(name, 'IC001', 1, 1)
        lwpla.indata = image
        lwpla.lpen = 3
        lwpla.outfile = 'PWD:' + name + '.ps'
        lwpla.copies = 1 
        lwpla.dodark = 1
        
        call("gs", name + ".ps")
