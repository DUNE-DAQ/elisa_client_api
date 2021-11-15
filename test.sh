#!/bin/bash
ELISA_HERE=$(cd $(dirname $(readlink -f ${BASH_SOURCE})) && pwd)
echo $ELISA_HERE
export TDAQ_PYTHONPATH=${ELISA_HERE}
export PYTHONPATH=${ELISA_HERE}
# export USE_ELISA_MERGED=true
# cern-get-sso-cookie --krb -r -u https://np-vd-coldbox-elog.cern.ch -o ${ELISA_HERE}/cookie.txt
# python ${ELISA_HERE}/src/elisa_client_api/scripts/elisa_get.py -s https://np-vd-coldbox-elog.cern.ch  -i 108 -k "np-vd-coldbox-elog"
elisa_get -s https://np-vd-coldbox-elog.cern.ch  -i 108 -k "np-vd-coldbox-elog"
#python ${ELISA_HERE}/src/elisa_client_api/scripts/elisa_insert.py -o ${ELISA_HERE}/cookie.txt -s https://np-vd-coldbox-elog.cern.ch -j "Testing the Elisa API" -y "Default" -b "This is a test to insert entries from CLI" -a "Alessandro Thea" -e "Infrastructure" -k "np-vd-coldbox-elog"
