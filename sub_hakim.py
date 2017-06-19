import subprocess
from flask import Flask, jsonify

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
