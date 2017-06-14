import subprocess

#---------------------------Error Handling------------------------

def get_bridge_EH(bridge):
    x = subprocess.Popen(('sudo ovs-vsctl show | grep -w \"' + bridge + '\"'), shell=True, stdout=subprocess.PIPE).communicate()[0]
    return x

def get_flowtablefile_EH(flowtablefile):
    x = subprocess.Popen(('sudo ls -l | grep -w \"' + flowtablefile + '\"'), shell=True, stdout=subprocess.PIPE).communicate()[0]
    return x

def get_flowentry_flowtablefile_EH(flow, flowtablefile):
    x = subprocess.Popen(('sudo cat ' + flowtablefile + ' | grep -w \"' + flow + '\"'), shell=True, stdout=subprocess.PIPE).communicate()[0]
    return x 

def get_groupid_EH(bridge, groupid):
    x = subprocess.Popen(('sudo ovs-ofctl -O OpenFlow11 dump-groups ' + bridge + ' | grep -w \"group_id=' + groupid + '\"'), shell=True, stdout=subprocess.PIPE).communicate()[0]
    return x 

def get_any_groupid_EH(bridge):
    x = subprocess.Popen(('sudo ovs-ofctl -O OpenFlow11 dump-groups ' + bridge + ' | grep -w \"group_id=\"'), shell=True, stdout=subprocess.PIPE).communicate()[0]
    return x
 
