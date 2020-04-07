#!/usr/bin/env python3

import docker
import os
from datetime import datetime

THIS_PREFIX = 'volansmelesmeles.transmissionopenvpn'

def _print (s : str):
    print (f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : {s}')

def connect():
    return docker.DockerClient(base_url='unix://var/run/docker.sock')

def addLabel (d, key, val):
    d[f"{THIS_PREFIX}.{key.lower()}"] = val
    return d

def getFileContents (thePath):
    f = ""
    with open(thePath,"r") as j:
        f = j.readlines()
    return ';'.join(f)

def getJackettVer():
    return getFileContents ('getJackett/jackett.ver.txt')

def getJackettURL():
    return getFileContents ('getJackett/jackett.url.txt')

def main():
    baseImage = 'haugene/transmission-openvpn:latest'
    client = connect()
    theImages = client.images.list(baseImage)
    labels = {}
    for i in theImages:
        labels = i.labels

    labels = addLabel(labels, 'base.image',baseImage)
    labels = addLabel(labels, 'jackett.version',getJackettVer())
    labels = addLabel(labels, 'jackett.url',getJackettURL())

    if 'maintainer' in labels and labels['maintainer'] is not None and len(labels['maintainer']) > 0:
        labels = addLabel(labels, 'base.image.maintainer',labels['maintainer'])

    labels['maintainer'] = 'jon@badger.shoes'

    with open ("Dockerfile", "r") as f:
        dockerfile = f.readlines()

    # Stick a LF on the end...
    if not dockerfile[-1][-1] == "\n":
        dockerfile[-1] += "\n"

    dockerfile.append ("#\n")
    dockerfile.append ("# LABEL entries added by createLabelFile.py\n")
    dockerfile.append ("#\n")

    def thisLabel (k, v):
        dockerfile.append (f'LABEL {k}=\"{v}\"\n')


    for key in labels:
        escapedVal = labels[key].replace('"','\"')
        thisLabel (key, escapedVal)

    with open ("Dockerfile.labels", "w") as f:
        f.writelines(dockerfile)

if __name__ == '__main__':
   main()