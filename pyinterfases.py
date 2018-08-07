#this is network Interfaces manager libery for CentOS in python

import os
import subprocess
def get_uuid(name):
#Use to get UUID to the network device
    p = subprocess.Popen(["uuidgen", name], stdout=subprocess.PIPE)

    q=str(p.communicate())
    q=q.replace("(b\'", "")
    q=q.replace("\\n', None)", "")
    q=q.replace(" ", "")
    return q


def net_list():
#list all Network interfaces .... its   return list
  tru_list=[]
  list=os.listdir("/etc/sysconfig/network-scripts")

  for x in list:
    if "ifcfg-" in x:
      x=x.replace("ifcfg-", "")
      tru_list.append(x)
  return tru_list

def interfase(name):
 #Display the information of the network interface
# its need the interface name as a parameter
# its   return Dictionary
  netdec={
"ip":"no",
"gateway":"no",
"netmask":"no"
}


  filepath = "ifcfg-"+name
  with open(filepath) as fp:  
    for cnt, line in enumerate(fp):
      if "dhcp" in line:
        netdec["ip"]="dhcp"
        netdec["gateway"]="dhcp"
        netdec["netmask"]="dhcp"
      if "IPADDR" in line:
        line=line.replace("IPADDR=", "")
        line=line.replace("\n", "")
        netdec["ip"]=line

      if "GATEWAY" in line:
        line=line.replace("GATEWAY=", "")
        line=line.replace("\n", "")
        netdec["gateway"]=line
      if "PREFIX" in line:
        line=line.replace("PREFIX=", "")
        line=line.replace("\n", "")
        netdec["netmask"]=line
  return netdec

def add(name, ip, prefix, gateway):
# add new Network interface
  if name=="lo":
    return 0

  with open('ifcfg-'+name, 'w') as the_file:
      if "dhcp" in ip:

        the_file.write('TYPE=Ethernet\n')
        the_file.write('BOOTPROTO=dhcp\n')
        the_file.write('DEFROUTE=yes\n')
        the_file.write('PEERDNS=yes\n')
        the_file.write('PEERROUTES=yes\n')
        the_file.write('IPV4_FAILURE_FATAL=no\n')
        the_file.write('IPV6INIT=yes\n')
        the_file.write('IPV6_AUTOCONF=yes\n')
        the_file.write('IPV6_DEFROUTE=yes\n')
        the_file.write('IPV6_PEERDNS=yes\n')
        the_file.write('IPV6_PEERROUTES=yes\n')
        the_file.write('IPV6_FAILURE_FATAL=no\n')
        the_file.write('IPV6_ADDR_GEN_MODE=stable-privacy\n')
        the_file.write('NAME='+name+'\n')
        the_file.write('UUID=0eee1895-219f-48a1-8373-726ec5167f87\n')
        the_file.write('DEVICE='+name+'\n')
        the_file.write('ONBOOT=yes\n')
      else:

        the_file.write('TYPE=Ethernet\n')
        the_file.write('BOOTPROTO=none\n')
        the_file.write('DEFROUTE=yes\n')
        the_file.write('IPV4_FAILURE_FATAL=no\n')
        the_file.write('IPV6INIT=yes\n')
        the_file.write('IPV6_AUTOCONF=yes\n')
        the_file.write('IPV6_DEFROUTE=yes\n')
        the_file.write('IPV6_FAILURE_FATAL=no\n')
        the_file.write('IPV6_ADDR_GEN_MODE=stable-privacy\n')
        the_file.write('NAME='+name+'\n')
        the_file.write('UUID=0eee1895-219f-48a1-8373-726ec5167f87\n')
        the_file.write('DEVICE='+name+'\n')
        the_file.write('ONBOOT=yes\n')
        the_file.write('DNS1=8.8.8.8\n')
        the_file.write('IPADDR='+ip+'\n')
        the_file.write('PREFIX='+prefix+'28\n')
        the_file.write('GATEWAY='+gateway+'\n')
        the_file.write('IPV6_PEERDNS=yes\n')
        the_file.write('IPV6_PEERROUTES=yes\n')
        the_file.write('IPV6_PRIVACY=no\n')
  return 0

def add_v(name, ip, prefix):
#    name=name.replace(":", "_")
# add new v Network interface
  with open('ifcfg-'+name, 'w') as the_file:
#      name=name.replace("_", ":")

      the_file.write('TYPE=Ethernet\n')
      the_file.write('BOOTPROTO=none\n')
      the_file.write('NAME='+name+'\n')
      the_file.write('DEVICE='+name+'\n')
      the_file.write('ONBOOT=yes\n')
      the_file.write('IPADDR='+ip+'\n')
      the_file.write('PREFIX='+prefix+'28\n')
  return 0

def add_net(name, ip, prefix, gateway):
  if ":" in name:
    add_v(name, ip, prefix)
  else:
    add(name, ip, prefix, gateway)
  return 0

def restart(name):
#restart Network interface
# its need the interface name as a parameter

    name=name.replace(":", "_")

  net="ifdown "+name+" && ifup "+name
  run=subprocess.check_output(net, shell=True)
  return 0

def start(name):
#start Network interface
# its need the interface name as a parameter

    name=name.replace(":", "_")

  net="ifup "+name
  run=subprocess.check_output(net, shell=True)
  return 0

def stop(name):
#stop Network interface
# its need the interface name as a parameter

    name=name.replace(":", "_")

  net="ifdown "+name
  run=subprocess.check_output(net, shell=True)
  return 0
def remove(name):
#remove Network interface
# its need the interface name as a parameter

  os.remove("/etc/sysconfig/network-scripts/ifcfg-"+name
