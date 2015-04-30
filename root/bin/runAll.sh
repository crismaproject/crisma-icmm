#!/bin/bash
#
# Peter.Kutschera@ait.ac.at, 2014-11-11

# offer swagger documentation && proxy to icmm_api
/usr/sbin/apachectl start


perl -i.bak -p -e  "s{discoveryUrl:\".*\"}{discoveryUrl:\"${ICMM_ENDPOINT}/resources\"}" /home/martin/icmm/swagger/index.html


# run with --link c_orion:orion 
# or with --env ORION_HOST='crisma-pilotC.ait.ac.at' --env ORION_PORT=80 --env ORION_PATH=orion
if [ "x$ORION_NAME" != "x" ]
then
   ORION_HOST=${ORION_PORT_1026_TCP_ADDR}
   ORION_PORT=${ORION_PORT_1026_TCP_PORT}
   ORION_PATH=""
fi

[ -e /icmmdata/CRISMA ] || cp -r /home/martin/icmm/data.setup/CRISMA /icmmdata
mkdir /icmmdata/CRISMA/ids
chown -R www-data:www-data /icmmdata/CRISMA/ids

# start ICMM
cd /home/martin/icmm/v2/lib/starterCrisma

java -ea \
    -DCRISMA_THIS_HOST=${ICMM_ENDPOINT} \
    -DCRISMA_ORION_HOST=${ORION_HOST} \
    -DCRISMA_ORION_PORT=${ORION_PORT} \
    -DCRISMA_ORION_PATH=${ORION_PATH} \
    -jar $(pwd)/cids-custom-crisma-server-0.2.1-starter.jar \
    9995 $ICMM_ENDPOINT \
    /icmmdata --non-interactive < /dev/null
