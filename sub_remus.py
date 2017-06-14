import subprocess

#-----------------Bridge-------------------

def get_bridge(bridge):
    x = subprocess.check_output(["sudo", "ovs-vsctl", "list", "Bridge", bridge])
    return x

def add_bridge(bridge):
    subprocess.call(["sudo", "ovs-vsctl", "add-br", bridge])

def update_bridge(bridge, option):
    subprocess.call(["sudo", "ovs-vsctl", "set", "Bridge", bridge, option])

def delete_bridge(bridge):
    subprocess.call(["sudo", "ovs-vsctl", "del-br", bridge])


#-------------------Flow---------------------

def get_flow(bridge):
    x = subprocess.check_output(["sudo", "ovs-ofctl", "dump-flows", bridge])
    return x

def add_flow(bridge, flow):
    subprocess.call(["sudo", "ovs-ofctl", "add-flow", bridge, flow])

def delete_allflow(bridge):
    subprocess.call(["sudo", "ovs-ofctl", "del-flows", bridge])    

def delete_specificflow(bridge,flow):
    subprocess.call(["sudo", "ovs-ofctl", "del-flows", "--strict", bridge, flow])

def update_allflow(bridge, flow):
    subprocess.call(["sudo", "ovs-ofctl", "mod-flows", bridge, flow])

def update_specificflow(bridge, flow):
    subprocess.call(["sudo", "ovs-ofctl", "mod-flows", "--strict", bridge, flow])


#------------------TableFile-------------------

def get_flowtablefile(flowtablefile):
    x = subprocess.check_output(["sudo", "cat", flowtablefile])
    return x

def create_flowtablefile(flowtablefile):
    subprocess.call(["sudo", "touch", flowtablefile])
    subprocess.call(["sudo", "chmod", "777", flowtablefile])
    
def add_flowtablefile(flow, flowtablefile):
    x = 'echo \"' + flow + '\" >> \"' + flowtablefile + '\"'
    subprocess.call(["sh", "-c", x])

def apply_flowtablefile(bridge, flowtablefile):
    subprocess.call(["sudo", "ovs-ofctl", "add-flows", bridge, flowtablefile])

def applyupdated_flowtablefile(bridge, flowtablefile):
    x = 'sudo ovs-ofctl mod-flows ' + bridge + ' - < ' + flowtablefile
    subprocess.call(["sh", "-c", x])   

def delete_flowtablefile(flowtablefile):
    subprocess.call(["sudo", "rm", flowtablefile])


#---------------------FlowGroup---------------------

def get_flowgroup(bridge):
    x = subprocess.check_output(["sudo", "ovs-ofctl", "-O", "OpenFlow11", "dump-groups", bridge])
    return x

def add_flowgroup(bridge, groupid, type1, action):
    x = 'sudo ovs-ofctl -O OpenFlow11 add-group ' + bridge + ' group_id=' + groupid + ',type=' + type1 + ',bucket=' + action
    subprocess.call(["sh", "-c", x])

def update_flowgroup(bridge, groupid, type1, action):
    x = 'sudo ovs-ofctl -O OpenFlow11 mod-group ' + bridge + ' group_id=' + groupid + ',type=' + type1 + ',bucket=' + action
    subprocess.call(["sh", "-c", x])

def delete_allflowgroup(bridge):
    x = 'sudo ovs-ofctl -O OpenFlow11 del-groups ' + bridge
    subprocess.call(["sh", "-c", x])

def delete_specificflowgroup(bridge, groupid):
    x = 'sudo ovs-ofctl -O OpenFlow11 del-groups ' + bridge + ' group_id=' + groupid
    subprocess.call(["sh","-c", x])



