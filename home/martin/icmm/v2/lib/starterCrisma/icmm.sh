#!/bin/bash

WD=/home/martin/icmm/v2/lib/starterCrisma

nohup /usr/local/java_sw/jdk1.8.0_05/bin/java -ea -DCRISMA_THIS_HOST=https://crisma-pilotEv1.ait.ac.at/icmm_api -DCRISMA_ORION_HOST=crisma-pilotEv1.ait.ac.at -jar $WD/cids-custom-crisma-server-0.2.1-starter.jar 9995 https://crisma-pilotEv1.ait.ac.at/icmm_api /home/martin/icmm/crisma-api-pilot-e --non-interactive < /dev/null > $WD/icmm.out 2>&1 &

echo $! > $WD/icmm.pid
