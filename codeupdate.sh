#!/bin/bash
BASEDIR=`pwd`

prepareforUpdate() {
    cd $BASEDIR
    if [ ! -d /home/project/webapps/test ]; then
        mkdir -p /home/project/webapps/test
    fi
    if [ ! -d /home/project/webapps/test/Files ]; then
        mkdir -p /home/project/webapps/test/Files
    fi
    if [ ! -d /home/project/webapps/test/static ]; then
        mkdir -p /home/project/webapps/test/static
    fi
    if [ ! -d /home/project/webapps/test/synapapp ]; then
        mkdir -p /home/project/webapps/test/synapapp
    fi
    if [ ! -d /home/project/webapps/test/templates ]; then
        mkdir -p /home/project/webapps/test/templates
    fi
    
}

updateCode() {
    cd $BASEDIR
    rsync -avr  $BASEDIR/Files/* /home/project/webapps/test/Files
    rsync -avr $BASEDIR/static/* /home/project/webapps/test/static
    rsync -avr $BASEDIR/synapapp/* /home/project/webapps/test/synapapp
    rsync -avr $BASEDIR/templates/* /home/project/webapps/test/templates
    
    systemctl daemon-reload
}


restartServices() {
    systemctl enable synap.service
    systemctl restart synap.service
    sleep 5
}


prepareforUpdate
updateCode
restartServices
#
