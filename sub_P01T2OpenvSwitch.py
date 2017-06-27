import subprocess, sys

#-----------------------------Bridge----------------------------

#Show Bridge
def get_ovsvsctl(bridge_id):
    output = subprocess.check_output(['sudo','ovs-vsctl','list', 'Bridge', bridge_id])
    return output

#Create Bridge
def create_input(bridge):
    bridge = subprocess.call(['sudo','ovs-vsctl','add-br', bridge])

#Delete bridge
def delete_input(bridge):
    delete = subprocess.call(['sudo','ovs-vsctl','del-br', bridge])

#Update Bridge on a particular br
def update_bridge(bridge_id,enable):
    updatebr = subprocess.call(['sudo','ovs-vsctl','set', 'Bridge', bridge_id, enable])


#---------------------------Failmode--------------------------

#Show failmode
def read_failmode(bridge_id):
    output = subprocess.check_output(['sudo','ovs-vsctl','get-fail-mode', bridge_id])
    return output    

#Create failmode on a particular br
def create_failmode(bridge_id, mode):
    modes = subprocess.call(['sudo','ovs-vsctl','set-fail-mode', bridge_id, mode])

#Delete failmode on a particular br
def delete_mode(bridge_id):
    deletemode = subprocess.call(['sudo','ovs-vsctl','del-fail-mode', bridge_id])

#Update Failmode on a particular br
def update_failmode(bridge_id, mode):
    update = subprocess.call(['sudo','ovs-vsctl','set-fail-mode', bridge_id, mode])


#--------------------------Controller-------------------------
    
#Show Controller
def read_controller(bridge_id):
    output = subprocess.check_output(['sudo','ovs-vsctl','get-controller', bridge_id])
    return output    

#Create Controller on a particular br
def create_controller(bridge_id, control):
    bridge = subprocess.call(['sudo','ovs-vsctl','set-controller', bridge_id, control])

#Delete Controller on a particular br
def delete_controller(bridge_id):
    deletecont = subprocess.call(['sudo','ovs-vsctl','del-controller', bridge_id])

#Update Controller on a particular br
def update_controller(bridge_id, control):
    updatecont = subprocess.call(['sudo','ovs-vsctl','set-controller', bridge_id, control])


#------------------------------Flow------------------------------

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


#-----------------------------TableFile----------------------------

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


#---------------------------FlowGroup----------------------------

def get_flowgroup(openflowversion, bridge):
    x = 'sudo ovs-ofctl -O ' + openflowversion + ' dump-groups ' + bridge
    y = subprocess.check_output(["sh", "-c", x])
    return y

def add_flowgroup(openflowversion, bridge, groupid, type1, action):
    x = 'sudo ovs-ofctl -O ' + openflowversion + ' add-group ' + bridge + ' group_id=' + groupid + ',type=' + type1 + ',bucket=' + action
    subprocess.call(["sh", "-c", x])

def update_flowgroup(openflowversion, bridge, groupid, type1, action):
    x = 'sudo ovs-ofctl -O ' + openflowversion + ' mod-group ' + bridge + ' group_id=' + groupid + ',type=' + type1 + ',bucket=' + action
    subprocess.call(["sh", "-c", x])

def delete_allflowgroup(openflowversion, bridge):
    x = 'sudo ovs-ofctl -O ' + openflowversion + ' del-groups ' + bridge
    subprocess.call(["sh", "-c", x])

def delete_specificflowgroup(openflowversion, bridge, groupid):
    x = 'sudo ovs-ofctl -O ' + openflowversion + ' del-groups ' + bridge + ' group_id=' + groupid
    subprocess.call(["sh","-c", x])


#--------------------------PORT------------------------------

def get_ports(bridge):
	read = subprocess.check_output(['sudo', 'ovs-ofctl', 'dump-ports-desc', bridge])
	return read

def add_ports(bridge, port):
	subprocess.call(['sudo', 'ovs-vsctl', '--may-exist', 'add-port', bridge, port])

def del_ports(bridge, port):
	subprocess.call(['sudo', 'ovs-vsctl', '--if-exists', 'del-port', bridge, port])

def update_ports(bridge, port, action):
	subprocess.call(['sudo', 'ovs-ofctl', 'mod-port', bridge, port, action])


#--------------------------Port mirror--------------------------

def get_mirror(mirror):
        read = subprocess.check_output(['sudo', 'ovs-vsctl', 'list', 'mirror', mirror])
        return read

def add_mirror(bridge, port1, port2, port3, port4, name, dest, source, output):
        subprocess.call(['sudo', 'ovs-vsctl', '--', 'set', 'Bridge', bridge, 'mirrors=@m', '--', port1, 'get', 'Port', port2, '--', port3, 'get', 'Port', port4, '--', '--id=@m', 'create', 'Mirror', name, dest, source, output])

def del_mirror(bridge, mirror):
        subprocess.call(['sudo', 'ovs-vsctl', '--', '--id=@m', 'get', 'mirror', mirror, '--', 'remove', 'bridge', bridge, 'mirrors', '@m'])


#---------------------------Netflow--------------------------

def get_netflow(bridge):
        read = subprocess.check_output(['sudo', 'ovs-vsctl', 'list', 'netflow', bridge])
        return read

def add_netflow(bridge, target, timeout):
        subprocess.call(['sudo', 'ovs-vsctl', '--', 'set', 'Bridge', bridge, 'netflow=@nf', '--', '--id=@nf', 'create', 'NetFlow', target, timeout])

def update_netflow(bridge, options):
        subprocess.call(['sudo', 'ovs-vsctl', 'set', 'NetFlow', bridge, options])

def del_netflow(bridge):
        subprocess.call(['sudo', 'ovs-vsctl', 'clear', 'Bridge', bridge, 'netflow'])


#-----------------------------VLAN-----------------------------

def add_vlan(bridge,interface,tag):
	test4 = subprocess.call(['sudo','ovs-vsctl','add-port',bridge, interface, tag])

def del_vlan(interface):
	test5 = subprocess.call(['sudo','ovs-vsctl','del-port', interface])

def update_vlan(interface,tag):
	test6 = subprocess.call(['sudo','ovs-vsctl','set','port',interface, tag])

def show_vlan():
	test7 = subprocess.call(['sudo','ovs-vsctl','show'])
	return test7


#-----------------------------Trunking--------------------------

def show_trunk():
	test8 = subprocess.call(['sudo','ovs-vsctl','show'])
	return test12

def add_trunk(interface,trunk):
	test9 = subprocess.call(['sudo','ovs-vsctl','set','port', interface, trunk])

def update_trunk(interface,trunk):
	test10 = subprocess.call(['sudo','ovs-vsctl','set','port', interface, trunk])

def del_trunk(interface):
        test11 = subprocess.call(['sudo','ovs-vsctl','del-port', interface])


#----------------------------------QoS----------------------------------

#Add a QoS Configuration
def add_qos(interface,qos):
        addqos = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'interface', interface, qos])

#Update a QoS Configuration
def update_qos(interface,qos):
        updateqos = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'interface', interface, qos])

#Show QoS Configuration for the particular interface
def show_qos(interface):
        showqos = subprocess.check_output(['sudo', 'ovs-vsctl', 'list', 'interface', interface])
        return showqos

#Show ingress_policing_rate for the particular interface
def show_qosrate(interface):
	showqosrate = subprocess.check_output(['sudo', 'ovs-vsctl', 'get', 'interface', interface, 'ingress_policing_rate'])
	return showqosrate

#Show ingress_policing_burst for the particular interface
def show_qosburst(interface):
	showqosburst = subprocess.check_output(['sudo', 'ovs-vsctl', 'get', 'interface', interface, 'ingress_policing_burst'])
	return showqosburst

#Delete by setting the QoS rate to 0
def del_qosrate(interface):
        delqosr = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'interface', interface, 'ingress_policing_rate=0'])

#Delete by setting the QoS burst to 0
def del_qosburst(interface):
        delqosb = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'interface', interface, 'ingress_policing_burst=0'])


#--------------------------------SSL---------------------------------

#Add SSL Config
def add_ssl(arg1,arg2,arg3):
	addssl = subprocess.call(['sudo', 'ovs-vsctl', 'set-ssl', arg1, arg2, arg3])

#Get SSL Config
def get_ssl():
	getssl = subprocess.check_output(['sudo', 'ovs-vsctl', 'get-ssl'])
	return getssl

#Update SSL Config
def update_ssl(arg1,arg2,arg3):
	updatessl = subprocess.call(['sudo', 'ovs-vsctl', 'set-ssl', arg1, arg2, arg3])

#Delete SSL Config
def del_ssl():
	delssl = subprocess.call(['sudo', 'ovs-vsctl', 'del-ssl'])


#--------------------------------STP---------------------------------

#Enable STP
def en_stp(bridge):
	enstp = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'bridge', bridge, 'stp_enable=true'])

#Disable STP
def dis_stp(bridge):
	disstp = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'bridge', bridge, 'stp_enable=false'])

#Get STP
def get_stp(bridge):
	getstp = subprocess.check_output(['sudo', 'ovs-vsctl', 'get', 'bridge', bridge, 'stp_enable'])
	return getstp

#Config STP Priority
def add_stppri(bridge,priority):
	addstppri = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'bridge', bridge, priority])

#Config STP Cost
def add_stpcost(port,cost):
	addstpcost = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'port', port, cost])

#Update STP Priority
def update_stppri(bridge,priority):
	upstppri = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'bridge', bridge, priority])

#Update STP Cost
def update_stpcost(port,cost):
	upstpcost = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'port', port, cost])

#Get STP Priority
def get_stppriority(bridge):
	getstppri = subprocess.check_output(['sudo', 'ovs-vsctl', 'get', 'bridge', bridge, 'other_config'])
	return  getstppri

#Get STP Cost
def get_stpcost(port):
	getstpcost = subprocess.check_output(['sudo', 'ovs-vsctl', 'get', 'port', port, 'other_config'])
	return getstpcost

#Clear the Configuration from the bridge
def del_stpbridge(bridge):
	delstpbridge = subprocess.call(['sudo', 'ovs-vsctl', 'clear', 'bridge', bridge, 'other_config'])

#Clear the Configuration from the port
def del_stpport(port):
	delstpport = subprocess.call(['sudo', 'ovs-vsctl', 'clear', 'port', port , 'other_config'])


#--------------------------OpenFlow Version---------------------------

#Add OpenFlow Version
def add_openflowv(bridge,protocols):
	addopenflowver = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'bridge', bridge, protocols])

#Update OpenFlow Version
def update_openflowv(bridge, protocols):
	updateopenflowver = subprocess.call(['sudo', 'ovs-vsctl', 'set', 'bridge', bridge, protocols])

#Get OpenFlow Version
def get_openflowv(bridge):
	getopenflowv = subprocess.check_output(['sudo', 'ovs-vsctl', 'get', 'bridge', bridge, 'protocols'])
	return getopenflowv

#Delete OpenFlow Version
def del_openflowv(bridge):
	delopenflowver = subprocess.call(['sudo', 'ovs-vsctl', 'clear', 'bridge', bridge, 'protocols'])


#-----------------------------Error Handling---------------------------

def bridge_pc(bridge):
	check = subprocess.Popen(('sudo ovs-vsctl list-br | grep -w ' + bridge), shell=True, stdout=subprocess.PIPE).communicate()[0]
	return check

def int_pc(interface):
        check = subprocess.Popen(('sudo ifconfig | grep -w ' + interface),shell=True, stdout=subprocess.PIPE).communicate()[0]
        return check

def port_bridge(bridge, port):
        check = subprocess.Popen(('sudo ovs-vsctl list-ports ' + bridge + ' | grep ' + port), shell=True, stdout=subprocess.PIPE).communicate()[0]
        return check

def check_mirror(mirror):
        check = subprocess.Popen(('sudo ovs-vsctl list mirror | grep ' + mirror), shell=True, stdout=subprocess.PIPE).communicate()[0]
        return check

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
