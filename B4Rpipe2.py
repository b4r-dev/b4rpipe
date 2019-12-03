#!/usr/bin/env python3
import LibB4Rtools as Lib
import importlib
import os
import numpy as np
importlib.reload(Lib)

globBaseDir = '/Volumes/hdd_mac/b4r'
globLogDir = '/Volumes/hdd_mac/b4r/logv1'

def PipelineAnalysis(obsnum):

    Lib.globBaseDir = globBaseDir
    Lib.globLogDir = globLogDir

    os.system('mkdir -p '+Lib.globLogDir)
    os.system('mkdir -p '+Lib.globLogDir+'/'+str(obsnum))

    logf = open(Lib.globLogDir+'/'+str(obsnum)+'/PipelineAnalysis.'+str(obsnum)+'.log','w')

    try:
        obj = Lib.B4Rdataset(obsnum=obsnum,calnum=obsnum-1)
        obj.Pipeline(binning=8)
        obj.LinePointingQlook()
        logf.write('LinePointing: PASS'+'\n')
    except:
        logf.write('LinePointing: FAIL'+'\n')

    try:
        obj = Lib.B4Rdataset(obsnum=obsnum,calnum=obsnum-1)
        obj.Pipeline(binning=512,noRefCal=True)
        obj.ContPointingQlook()
        logf.write('ContPointing: PASS'+'\n')
    except:
        logf.write('ContPointing: FAIL'+'\n')

    try:
        obj = Lib.B4Rdataset(obsnum=obsnum,calnum=obsnum-1)
        obj.Pipeline(binning=8)
        obj.PsQlook(highz=False)
        logf.write('Ps(nearby): PASS'+'\n')
    except:
        logf.write('Ps(nearby): FAIL'+'\n')

    try:
        obj = Lib.B4Rdataset(obsnum=obsnum,calnum=obsnum-1)
        obj.Pipeline(binning=256)
        obj.PsQlook(highz=True)
        logf.write('Ps(High-z): PASS'+'\n')
    except:
        logf.write('Ps(High-z): FAIL'+'\n')


    try:
        obj = Lib.B4Rdataset(obsnum=obsnum,calnum=obsnum-1)
        obj.Pipeline(binning=1)
        obj.createPsData()
        logf.write('PsData: PASS'+'\n')
    except:
        logf.write('PsData: FAIL'+'\n')

    try:
        obj = Lib.B4Rdataset(obsnum=obsnum,calnum=obsnum-1)
        obj.Pipeline(binning=1,noRefCal=True)
        obj.createMS2()
        logf.write('MS2: PASS'+'\n')
    except:
        logf.write('MS2: FAIL'+'\n')

    logf.close()


if __name__ == '__main__':
    print('### Batch run start!! ###')
    obsnum_list = (np.array(Lib.returnFileList(mode='OBS'))[:,0]).astype('int')
    obsnum_list = obsnum_list[obsnum_list>79999] # 2019

    for obsnum in obsnum_list:
        PipelineAnalysis(obsnum)
