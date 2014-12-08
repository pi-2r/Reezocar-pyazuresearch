#!/bin/bash
# Global Variables
userid=`id -u`
osinfo=`cat /etc/issue|cut -d" " -f1|head -n1`
eplpkg='http://linux.mirrors.es.net/fedora-epel/6/i386/epel-release-6-8.noarch.rpm'
# Clear Terminal (For Prettyness)
clear
# Print Title
echo '#######################################################################'
echo '# Python setup                                                        #'
echo '#######################################################################'
echo
# Check to make sure you are root!
# Thanks to @themightyshiv for helping to get a decent setup script out
if [ "${userid}" != '0' ]; then
echo '[Error]: You must run this setup script with root privileges.'
echo
exit 1
fi

apt-get update
apt-get install -y python python-pip
pip install simplejson httplib2

echo
echo "Finish, you can launch bulkapi.py"
