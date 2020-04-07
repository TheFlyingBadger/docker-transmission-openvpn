#!/usr/bin/env python3

import requests
import re
import os
import tarfile
import humanize
import shutil

from bs4            import BeautifulSoup
from urllib.parse   import urlparse
from urllib.parse   import urlunparse
from datetime       import datetime

headers = None
url = "https://github.com/Jackett/Jackett/releases/latest"


def _print (s : str):
    print (f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} : {s}')

def getSize(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def getDownloadURL():

    global headers

    # Set headers
    headers = requests.utils.default_headers()
    headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
    
    o = urlparse(url)

    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    thingy = soup.findAll('span', text = re.compile('(Jackett\.Binaries\.LinuxAMDx64\.tar\.gz)'), attrs = {'class','pl-2'})

    if not len(thingy) == 1:
        raise Exception ("Not able to find span")
    p = urlunparse([o.scheme, o.netloc, thingy[0].parent["href"], None, None, None])
    
    return p


def getFilenames():
    saveFolder = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists (saveFolder):
        os.makedirs(saveFolder)
    return [saveFolder, os.path.join (saveFolder,'jackett.tar.gz'), os.path.join (saveFolder,'jackett.url.txt'), saveFolder, os.path.abspath(os.path.join(saveFolder,'..','container','Jackett')), os.path.join (saveFolder,'jackett.ver.txt')]

def deleteFile (fName : str):    
    try:
        os.remove(fName)
    except FileNotFoundError:
        # Seek forgiveness, not permission
        pass

def versionFromURL (url : str) -> str:
    version = ""
    if url is not None and len(url) > 0:
        version = ','.join((v for v in url.split('/') if len(v) > 1 and v[0] == 'v'))
    if version is None:
        version = ""
    return version


def getJackett  (extractFile    : bool = True
                ,forceDownload  : bool = False
                ):

    releaseFilename = getFilenames()
    releaseURL      = getDownloadURL()
    releaseVersion  = versionFromURL (releaseURL)

    outLines =  [f"Page URL         : {url}"
                ,f"Release URL      : {releaseURL}"
                ,f"        Version  : {releaseVersion}"
                ,f"Cache   Path     : {releaseFilename[3]}"
                ,f"        Archive  : {releaseFilename[1]}"
                ,f"        URL File : {releaseFilename[2]}"
                ]

    sepLine = "~"*len(max(outLines, key=len))
    _print (sepLine)
    _print (f"Downloading latest Jackett Release")
    _print ("-"*34)
    for l in outLines:
        _print (l)

    if forceDownload:
        _print ("                   - Forcing Download, ignoring local cache")
        deleteFile(releaseFilename[1])
        deleteFile(releaseFilename[2])
        deleteFile(releaseFilename[5])
    elif os.path.exists(releaseFilename[1]) and os.path.exists(releaseFilename[2]):
        with open(releaseFilename[2],'r') as f:
            existingURL = f.read()
        _print (f"        URL      : {existingURL}")
        cacheVersion = versionFromURL (existingURL)
        _print (f"        Version  : {cacheVersion}")

        if releaseURL == existingURL:
            _print ("                   - Local cache is up to date")
        else:
            _print ("                   - Local cache is outdated")
            deleteFile(releaseFilename[1])
            deleteFile(releaseFilename[2])
            deleteFile(releaseFilename[5])
    else:
        _print ("                   - No local cache exists")
    
    freshDownload = not (os.path.exists(releaseFilename[1]) and os.path.exists(releaseFilename[2]))
    if not freshDownload:
        archiveSize = os.stat(releaseFilename[1]).st_size
    else:
        with open(releaseFilename[2],'w') as f:
            f.write(releaseURL)
        r = requests.get(releaseURL, headers, allow_redirects=True)
        archiveSize = len(r.content)
        with open(releaseFilename[1], 'wb') as f:
            f.write(r.content)
    _print (f"Archive Size     : {humanize.naturalsize(archiveSize)}")

    if  (extractFile
     and (freshDownload or not os.path.exists (releaseFilename[4]))
        ):
        try:
            shutil.rmtree(releaseFilename[4])
        except FileNotFoundError:
            pass
        with tarfile.open(releaseFilename[1]) as tar:
            tar.extractall(path=os.path.abspath(os.path.join(releaseFilename[4],'..')))
    else:
        _print ('                   - Not extracting archive')
    with open(releaseFilename[5],'w') as f:
        f.write(releaseVersion)
    if os.path.exists (releaseFilename[4]):
        _print (f"Extract Folder   : {releaseFilename[4]}")
        _print (f"Folder Size      : {humanize.naturalsize(getSize(releaseFilename[4]))}")
    
    _print (sepLine)

if __name__ == '__main__':
   getJackett()