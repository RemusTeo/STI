import subprocess
from flask import Flask, jsonify

#------------------------------------------Bridge-------------------------------

#Add a bridge
def add_bridge(bridge):
        addbridge = subprocess.call(['sudo', 'ovs-vsctl', 'add-br', bridge])

#Show bridge
def show_bridge():
        showbridge = subprocess.check_output(['sudo', 'ovs-vsctl', 'show'])
        return showbridge
#Delete a particular bridge
def del_bridge(bridge):
        delbridge = subprocess.call(['sudo', 'ovs-vsctl', 'del-br', bridge])

#--------------------------------------Port------------------------------------------

#Add a port to the bridge
def add_port(bridge,port):
        addport = subprocess.call(['sudo', 'ovs-vsctl', 'add-port', bridge, port])

#Show port for the bridge
def show_port():
        showports = subprocess.check_output(['sudo', 'ovs-vsctl', 'show'])
        return showports

#Delete a port for the particular bridge
def del_port(bridge,port):
        delport = subprocess.call(['sudo', 'ovs-vsctl', 'del-port', bridge, port])

#--------------------------------------QoS-----------------------------------------

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

#-------------------------------------SSL-------------------------------------------------

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
#------------------------------------STP------------------------------------------

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

#-------------------------------OpenFlow Version-------------------------------
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

#-------------------------------------------------------------------------------
