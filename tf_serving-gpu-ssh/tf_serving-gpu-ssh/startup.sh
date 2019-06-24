#!/bin/bash
echo "root:$PASSWORD" | chpasswd
#start xrdp
rm -f /run/xrdp/xrdp*
/root/.init/config.sh
#config nvidia
ldconfig
/etc/init.d/xrdp restart
#start sshd
/usr/sbin/sshd -D