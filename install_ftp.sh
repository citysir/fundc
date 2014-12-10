#!/bin/bash
# Remove=>Download=>Install=>Configure=>Start service "vsftpd"
#
# /usr/bin/yum => #!/usr/bin/python2.4

# Remove old
/sbin/service vsftpd stop
#/usr/bin/yum -y remove vsftpd db4-utils
/bin/rm -rf /etc/vsftpd

# Download and install new program
/usr/bin/yum -y install vsftpd db4-utils

#####################
# Configure from here

# Make directories
/bin/mkdir -p /etc/vsftpd/roles

# Use configuration settings below
test -f /etc/vsftpd/vsftpd.conf && /bin/mv /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.conf.old
/bin/cat > /etc/vsftpd/vsftpd.conf << _vsftpconfig
anon_mkdir_write_enable=NO
anon_root=/dev/zero
anon_upload_enable=NO
anon_world_readable_only=YES
anonymous_enable=NO
banner_file=/etc/vsftpd/issue
chroot_list_enable=YES
chroot_list_file=/etc/vsftpd/chroot_list
chroot_local_user=YES
connect_from_port_20=YES
data_connection_timeout=120
dirmessage_enable=YES
ftpd_banner=Welcome
guest_enable=YES
guest_username=nobody
pam_service_name=vsftpd.nobody
idle_session_timeout=600
local_enable=YES
local_umask=022
log_ftp_protocol=YES
passwd_chroot_enable=NO
pasv_enable=YES
pasv_min_port=50000
pasv_max_port=50300
listen_ipv6=NO
listen_port=7721
listen=YES
tcp_wrappers=YES
use_localtime=NO
user_config_dir=/etc/vsftpd/roles
userlist_enable=YES
virtual_use_local_privs=YES
write_enable=YES
xferlog_enable=YES
xferlog_std_format=YES
reverse_lookup_enable=NO
_vsftpconfig

/bin/mkdir -p /data/apps
/bin/chown nobody:nobody /data/apps
/bin/chmod 777 -R /data/apps

/bin/cat >> /etc/vsftpd/accounts << _accounts
ftp_deploy
kVsHOX2q2jA3TlgBPQr9EYDfNV21Bz
_accounts

/bin/cat > /etc/vsftpd/roles/ftp_deploy << _account_settings
local_root=/data/apps
write_enable=yes
anon_world_readable_only=no
anon_upload_enable=no
anon_mkdir_write_enable=no
virtual_use_local_privs=yes
_account_settings

/usr/bin/db_load -T -t hash -f /etc/vsftpd/accounts /etc/vsftpd/accounts.db
/bin/chmod 0600 /etc/vsftpd/accounts.db
echo "/usr/bin/db_load -T -t hash -f /etc/vsftpd/accounts /etc/vsftpd/accounts.db" > /etc/vsftpd/create.sh
echo "/bin/chmod 0600 /etc/vsftpd/accounts.db" >> /etc/vsftpd/create.sh
/bin/chmod u+x /etc/vsftpd/create.sh

# Add PAM
test $(/usr/bin/getconf LONG_BIT) -eq 64 && logBit=64
/bin/cat > /etc/pam.d/vsftpd.nobody << _pam
#%PAM-1.0
auth       sufficient     /lib${logBit:+64}/security/pam_userdb.so db=/etc/vsftpd/accounts
account    sufficient     /lib${logBit:+64}/security/pam_userdb.so db=/etc/vsftpd/accounts
_pam

# User permission
touch /etc/vsftpd/chroot_list
touch /etc/vsftpd/user_list

/bin/cat > /etc/vsftpd/issue << _ftpissue
==== Welcome to use ftp server ====
_ftpissue

# selinux
#SELINUX_FLAG=$(/usr/bin/awk -F"=" '/^SELINUX/ {print $2}' /etc/sysconfig/selinux)
#test "$SELINUX_FLAG" != "enforcing" && /bin/sed -i 's/SELINUX=.*$/SELINUX=enforcing/' /etc/sysconfig/selinux
/usr/sbin/setsebool -P ftpd_disable_trans on
# chkconfig
/sbin/chkconfig vsftpd on

# Start service "vsftpd"
setenforce 0
/sbin/service vsftpd start
# type "ftp localhost" to test
# END