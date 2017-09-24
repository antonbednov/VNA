import re
from enum import Enum
import numpy as np

class _s2pBlocks(Enum):
    SETTINGS = 1
    HEAD = 2
    DATA = 3
    
def getparams():
    return {'freq-unit':'GHZ', 'param-type':'S', 'data-format':'RI', 'keyword':'R', 'impedance-ohms':50}

def readFile(sFullPath):
    ptrn = re.compile('[\w-]+')
    ptrnData = re.compile('-{0,1}\d+\.{0,1}\d*')
    f = open(sFullPath,'r')
    fileBlock = None
    listData = []
    for line in f:
        if fileBlock is None and line[0] == '!':
            paramNames = ptrn.findall(line)
            if len(paramNames) > 0:
                params = dict.fromkeys(paramNames)
                fileBlock = _s2pBlocks.SETTINGS
        elif fileBlock == _s2pBlocks.SETTINGS and line[0] =='#':
            paramValues = ptrn.findall(line)
            if len(paramValues) == len(paramNames):
                for i in range(len(paramNames)):
                    params[paramNames[i]] = paramValues[i]
                fileBlock = _s2pBlocks.HEAD
        elif fileBlock == _s2pBlocks.HEAD  and line[:2] =='!-':
            fileBlock = _s2pBlocks.DATA
        elif fileBlock == _s2pBlocks.DATA and line[0] != '!':
            listData.append(ptrnData.findall(line))
    arrLen = len(listData)
    arrFreq = np.empty(arrLen)
    arrS = np.empty((arrLen,2,2),dtype=np.complex)
    for i in range(arrLen):
        arrFreq[i] = listData[i][0]
        if params['data-format'] == 'RI':
            arrS[i,0,0] = complex(float(listData[i][1]),float(listData[i][2]))
            arrS[i,1,0] = complex(float(listData[i][3]),float(listData[i][4]))
            arrS[i,0,1] = complex(float(listData[i][5]),float(listData[i][6]))
            arrS[i,1,1] = complex(float(listData[i][7]),float(listData[i][8]))
        else:
            raise RuntimeError('Only RI data-format supported')
    f.close()
    return [arrFreq, arrS, params]

def writeFile(sFullPath, arrFreq, arrS, params):
    f = open(sFullPath,'w')
    f.write('!freq-unit  param-type  data-format  keyword  impedance-ohms\n')
    f.write('# {0:<8}  {1:^10}  {2:^11}  {3:^7}  {4:^14}\n'.format(params['freq-unit'], params['param-type'], params['data-format'], params['keyword'], params['impedance-ohms']))
    f.write('!-----------------------------------------------------------------------------\n')
    f.write('!Freq             ReS11           ImS11           ReS21           ImS21           ReS12           ImS12           ReS22           ImS22\n')
    for i in range(len(arrFreq)):
        f.write('{:<16}'.format(arrFreq[i]))
        for j in range(2):
            for k in range(2):
                f.write('{0:<16}{1:<16}'.format(arrS[i][k][j].real, arrS[i][k][j].imag))
        f.write('\n')
    f.close()         