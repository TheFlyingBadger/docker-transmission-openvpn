#!/usr/bin/env python3

import os
from datetime import datetime

def _print (s : str):
    print (f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : {s}')

def getTheFiles(thisPath : str):
    files = []
    for file in os.listdir(thisPath):
        if file.endswith(".sh"):
            files.append(file)
    return  files

def doFile (thisPath : str, thisFile : str):
    srcPath = os.path.join(thisPath,thisFile)
    _print (srcPath)
    with open (srcPath, 'r') as f:
        src = f.readlines()
    
    destPath = '/scripts'
    if not os.path.exists(destPath):
        _print (f"Creating {destPath}")
        os.makedirs(destPath)

    theCall = f'. {srcPath}\n'

    destFile = os.path.join (destPath,thisFile)
    _print (destFile)
    if not os.path.exists(destFile):
        print ("destfile not found")
        dest =  ["#!/bin/bash\n"
                ,theCall
                ]
        callExists = False
    else:
        print ("destfile found")
        with open (destFile, 'r') as f:
            dest = f.readlines()
        callExists = False
        for l in dest:
            if theCall in l:
                callExists = True
                break
        if not callExists:
            print ("appending call")
            dest.append ("\n")
            dest.append (theCall)
        else:
            print ("call already there")
    if not callExists:
        print ("writing file back out")
        with open (destFile, 'w') as f:
            f.writelines(dest)

    # Make sure the destfile is executable!
    os.chmod(path = destFile
            ,mode = 0o755 
            )

def main():
    thisPath = os.path.dirname(os.path.realpath(__file__))
    files    = getTheFiles(thisPath)
    for f in files:
        doFile(thisPath, f)

if __name__ == '__main__':
   main()