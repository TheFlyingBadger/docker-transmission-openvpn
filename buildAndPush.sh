#!/bin/bash
theLog="latestBuild.log"
theImage="volansmelesmeles/transmission-openvpn"
masterImage="haugene/transmission-openvpn"
echo "This Image : '$theImage'" | tee $theLog 
echo "Master     : '$masterImage'" | tee -a $theLog 
echo "Locale     : '$LANG'" | tee -a  $theLog 
echo "Language   : '$LANGUAGE'" | tee -a  $theLog 
rm Dockerfile.labels
set -x
docker pull $masterImage
./getJackett/getLatestJackett.py | tee -a  $theLog
./createLabelFile.py | tee -a  $theLog
docker build -t $theImage --build-arg container_language=$LANGUAGE --build-arg container_locale=$LANG --file Dockerfile.labels . | tee -a  $theLog
docker push $theImage | tee -a  $theLog
set +x
echo "All done"
