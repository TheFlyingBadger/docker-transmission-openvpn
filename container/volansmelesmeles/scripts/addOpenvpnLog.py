#!/usr/bin/env python3

import os
import glob
from  datetime import datetime

THISFILE : str = os.path.realpath(__file__)
BASE_DIR : str = '/etc/openvpn/'
LOG_PATH : str = '/config/log/transmission-openvpn/openvpn.log'
APPEND_HEADER : str = f'# <{THISFILE}>'
APPEND_FOOTER : str = f'# </{THISFILE}>'

P_USER   : str = ""
P_GROUP  : str = ""

def _print (s : str):
    print (f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : {s}')

def getTheFiles(thisPath : str):
    return list(sorted(glob.glob(f'{thisPath}**/*.ovpn', recursive = True)))


def doFile (theFile):

    global P_USER,P_GROUP

    with open (theFile,'r') as f:
        lines = f.readlines()

    if (lines[-1][-1] == "\n"):
        theLine = ""
    else: # no LF on the end of the last line of the file
        theLine = "\n"
    theLine += APPEND_HEADER
    extraLines = []
    extraLines.append (theLine)
    fileChanged = False

    if ( (P_USER  is not None and len(P_USER)  > 0)
     and (P_GROUP is not None and len(P_GROUP) > 0)
     and (len([l for l in lines
                if (l[0:5] == "user "
                    or l[0:6] == "group "
                    )
                ]
             ) == 0
         )
       ):
        extraLines.append ('# Downgrade privileges after initialization')
        extraLines.append (f'user {P_USER}')
        extraLines.append (f'group {P_GROUP}')
        fileChanged = True

    if len([l for l in lines
            if (l[0:3] == "log "
                or l[0:11] == "log-append "
                )
            ]
          ) == 0: # no "log" records

        extraLines.append (f'log-append "{LOG_PATH}"')
        fileChanged = True

    if fileChanged:
        extraLines.append (APPEND_FOOTER)
        with open (theFile,'a') as f:
            f.write('\n'.join(extraLines))
    lines   = None
    return fileChanged

def main():

    global P_USER,P_GROUP

    P_USER           = os.getenv('runUser')
    P_GROUP          = os.getenv('runGroup')
    OPENVPN_PROVIDER = os.getenv('OPENVPN_PROVIDER')

    _print (f"Run User         : {P_USER}")
    _print (f"Run Group        : {P_GROUP}")
    _print (f"OpenVPN Provider : {OPENVPN_PROVIDER}")

    filesDone = []
    padLen    = 0

    if OPENVPN_PROVIDER is None or len(OPENVPN_PROVIDER) == 0:
        providerPath = BASE_DIR
    else:
        providerPath = os.path.join(BASE_DIR,OPENVPN_PROVIDER)
        
    files        = getTheFiles(providerPath)
        
    for f in files:
        filesDone.append (dict(file=f,done=doFile(f)))
        if len(f) > padLen:
            padLen = len(f)

    lines = [f"{'Filename'.ljust(padLen)} Done\n"
            ,f"{'-' * padLen} -----\n"
            ]
    for d in filesDone:
        lines.append(f"{d['file'].ljust(padLen)} {d['done']}\n")
    with open (f"{LOG_PATH}.update.log",'w') as f:
        f.writelines(lines)

if __name__ == '__main__':
   main()