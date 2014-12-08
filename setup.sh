#!/bin/bash
userid=`id -u`
clear

# Print Title
echo '#######################################################################'
echo '# 		Python setup                                        #'
echo '#######################################################################'
echo

# Check to make sure you are root!
if [ "${userid}" != '0' ]; then
echo '[Error]: You must run this setup script with root privileges.'
echo
exit 1
fi

apt-get update
apt-get install -y python python-pip
pip install simplejson httplib2

echo
echo "Finish, you can launch test_client.py"
