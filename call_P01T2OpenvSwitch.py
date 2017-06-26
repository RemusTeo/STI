#!flask/bin/python
import sub_remus
import sub_sean
import sub_abdullah
import sub_joey
import sub_hakim
import errorhandling_remus
from flask import Flask, jsonify, abort, request, make_response
from flask_httpauth import HTTPBasicAuth
import json


call = Flask(__name__)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'P01':
        return 'T2'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized Access'}), 403)

@call.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@call.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


#--------------------------Bridge-------------------------------

#GET Bridge
@call.route('/read/bridge/<bridge_id>', methods=['GET'])
@auth.login_required
def get_ovsvsctl(bridge_id):
	bridge = sub_hakim.get_ovsvsctl(bridge_id)
	return jsonify({'Bridge' :bridge.splitlines()})

#POST Bridge
@call.route('/write/bridge', methods=['POST'])
@auth.login_required
def create_input():
        bridge = request.json['bridge']
	sub_hakim.create_input(bridge)
	return jsonify({'Bridge' : bridge,
			'Port' : bridge,
			'Interface' : bridge,
			'Type' : "internal"
					}), 201

#DELETE Bridge on particular br
@call.route('/delete/bridge/<bridge_id>', methods=['DELETE'])
@auth.login_required
def delete_input(bridge_id):
        if len(bridge_id) > 0: #if the bride exist
                sub_hakim.delete_input(bridge_id)
        else:
                abort(404)
        return jsonify({'result':True})

#UPDATE Bridge on a particular br
@call.route('/update/bridge/<bridge_id>', methods=['PUT'])
@auth.login_required
def update_bridge(bridge_id):
        stp = request.json['stp_enable']
	sub_hakim.update_bridge(bridge_id,stp)
        return jsonify({'stp_enable' : stp.rstrip()
                                        }), 201

#------------------------Failmode------------------------

#GET Failmode on particular br
@call.route('/read/failmode/<bridge_id>', methods=['GET'])
@auth.login_required
def read_failmode(bridge_id):
       mode =  sub_hakim.read_failmode(bridge_id)
       return jsonify({'fail_mode' : mode.rstrip()})

#POST Failmode on particular br
@call.route('/write/failmode/<bridge_id>', methods=['POST'])
@auth.login_required
def create_failmode(bridge_id):
        mode = request.json['fail_mode']
        sub_hakim.create_failmode(bridge_id,mode)
        return jsonify({'fail_mode' : mode
			                      }), 201

#DELETE Failmode on particular br
@call.route('/delete/failmode/<bridge_id>', methods=['DELETE'])
@auth.login_required
def delete_mode(bridge_id):
        if len(bridge_id) > 0: #if the bride exist
                sub_hakim.delete_mode(bridge_id)
        else:
                abort(404)
        return jsonify({'result':True})

#UPDATE Failmode on particular br
@call.route('/update/failmode/<bridge_id>', methods=['PUT'])
@auth.login_required
def update_failmode(bridge_id):
        mode = request.json['fail_mode']
        sub_hakim.update_failmode(bridge_id,mode)
        return jsonify({'Bridge' : bridge_id,
                        'Port' : bridge_id,
                        'Interface' : bridge_id,
                        'Type' : "internal",
                        'fail_mode' : mode
                                              })


#----------------------Controller----------------------

#Get Controller
@call.route('/read/controller/<bridge_id>', methods=['GET'])
@auth.login_required
def read_controller(bridge_id):
       control =  sub_hakim.read_controller(bridge_id)
       return jsonify({'controller' : control.rstrip()})

#POST Controller on particular br
@call.route('/write/controller/<bridge_id>', methods=['POST'])
@auth.login_required
def create_controller(bridge_id):
        control = request.json['Controller']
        sub_hakim.create_controller(bridge_id,control)
        return jsonify({'Controller' : control
                                        }), 201

#DELETE Controller on particular br
@call.route('/delete/controller/<bridge_id>', methods=['DELETE'])
@auth.login_required
def delete_controller(bridge_id):
	if len(bridge_id) > 0: #if the bride exist
		sub_hakim.delete_controller(bridge_id)
	else:
		abort(404)
	return jsonify({'result':True})

#UPDATE Controller on particular br
@call.route('/update/controller/<bridge_id>', methods=['PUT'])
@auth.login_required
def update_controller(bridge_id):
        control = request.json['Controller']
        sub_hakim.update_controller(bridge_id,control)
        return jsonify({'Bridge' : bridge_id,
                        'Port' : bridge_id,
                        'Interface' : bridge_id,
                        'Type' : "internal",
                        'Controller' : control
                                              }), 201


#-------------------------Flow-------------------------

#Read flow of bridge
@call.route('/flow/read/<bridge>', methods=['GET'])
@auth.login_required
def getFlow(bridge):
    #if does not exist, cant get, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    flow = sub_remus.get_flow(bridge)
    return jsonify({'Flow':flow.splitlines()})

#Create flow for bridge
@call.route('/flow/post/<bridge>', methods=['POST'])
@auth.login_required
def addFlow(bridge):
    #if curl no -d, or -d not flow, abort 400
    if not request.json or not 'flow' in request.json or type(request.json['flow']) != unicode:
        abort(400)

    flow = request.json['flow']

    ##if bridge does not exist, cant post, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    sub_remus.add_flow(bridge,flow)

    return jsonify({'bridge': bridge,
                    'flow': flow}), 201

#Update all flow for bridge
@call.route('/flow/update/<bridge>', methods=['PUT'])
@auth.login_required
def updateAllFlow(bridge):
    #if curl no -d, or -d not flow, abort 400
    if not request.json or not 'flow' in request.json or type(request.json['flow']) != unicode:
        abort(400)

    flow = request.json['flow']

    #if bridge does not exist, cant delete, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    sub_remus.update_allflow(bridge,flow)
    return jsonify({'bridge': bridge,
                    'flow': flow})

#Update specific flow for bridge
@call.route('/flow/update/specific/<bridge>', methods=['PUT'])
@auth.login_required
def updateSpecificFlow(bridge):
    #if curl no -d, or -d not flow, abort 400
    if not request.json or not 'flow' in request.json or type(request.json['flow']) != unicode:
        abort(400)

    flow = request.json['flow']

    #if bridge does not exist, cant delete, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    sub_remus.update_specificflow(bridge,flow)
    return jsonify({'bridge': bridge,
                    'flow': flow})


#Delete all flow from bridge
@call.route('/flow/delete/<bridge>', methods=['DELETE'])
@auth.login_required
def deleteAllFlow(bridge):
    #if bridge does not exist, cant delete, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    sub_remus.delete_allflow(bridge)

    return jsonify({'result': True})

#Delete specific flow from bridge
@call.route('/flow/delete/specific/<bridge>', methods=['DELETE'])
@auth.login_required
def deleteSpecificFlow(bridge):
    #if curl no -d, or -d not flow, abort 400
    if not request.json or not 'flow' in request.json or type(request.json['flow']) != unicode:
        abort(400)

    flow = request.json['flow']

    #if bridge does not exist, cant delete, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    sub_remus.delete_specificflow(bridge,flow)
    return jsonify({'result': True})


#------------------------FlowTableFile----------------------

#Read the file
@call.route('/flow/flowtablefile/read/<flowtablefile>', methods=['GET'])
@auth.login_required
def getFlowTableFile(flowtablefile):
    #if flowtablefile does not exist, cant read, so abort 404
    if len(str(errorhandling_remus.get_flowtablefile_EH(flowtablefile))) == 0:
        abort(404)

    ftFile = sub_remus.get_flowtablefile(flowtablefile)
    return jsonify({'Flowtablefile': ftFile.splitlines()})

#Create a file    
@call.route('/flow/flowtablefile/post', methods=['POST'])
@auth.login_required
def createFlowTableFile():
    #if curl no -d, or -d not flowtablefile, abort 400
    if not request.json or not 'flowtablefile' in request.json or type(request.json['flowtablefile']) != unicode:
        abort(400)

    ftFile = request.json['flowtablefile']
    
    #if already exist, cant post, so abort 400
    if len(str(errorhandling_remus.get_flowtablefile_EH(ftFile))) != 0:
        abort(400)

    sub_remus.create_flowtablefile(ftFile)

    #check if successfully created
    if len(str(errorhandling_remus.get_flowtablefile_EH(ftFile))) == 0:
        abort(400)

    return jsonify({'flowtablefile': ftFile}), 201

#Add lines of flow into file
@call.route('/flow/flowtablefile/post/<flowtablefile>', methods=['POST'])
@auth.login_required
def addFlowintoTablefile(flowtablefile):
    #if curl no -d, or -d not flow, abort 400
    if not request.json or not 'flow' in request.json or type(request.json['flow']) != unicode:
        abort(400)

    flow = request.json['flow']
    
    #if flowtablefile does not exist, cant read, so abort 404
    if len(str(errorhandling_remus.get_flowtablefile_EH(flowtablefile))) == 0:
        abort(404)

    sub_remus.add_flowtablefile(flow, flowtablefile)

    #check if successfully created
    if len(str(errorhandling_remus.get_flowentry_flowtablefile_EH(flow, flowtablefile))) == 0:
        abort(400)

    return jsonify({'flowtablefile': flowtablefile,
                    'flow': flow}), 201

#Apply file consisting of flows to bridge
@call.route('/flow/flowtablefile/post/<bridge>/<flowtablefile>', methods=['POST'])
@auth.login_required
def addFlowTablieFileToBridge(bridge, flowtablefile):
    ##if bridge does not exist, cant post, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    #if flowtablefile does not exist, cant apply, so abort 404
    if len(str(errorhandling_remus.get_flowtablefile_EH(flowtablefile))) == 0:
        abort(404)

    sub_remus.apply_flowtablefile(bridge,flowtablefile)
    return jsonify({'bridge': bridge,
                    'flowtablefile': flowtablefile}), 201

#Apply updated file consisting of flows to bridge
@call.route('/flow/flowtablefile/update/<bridge>', methods=['PUT'])
@auth.login_required
def applyUpdatedFlowTableFile(bridge):
    #if curl no -d, or -d not flowtablefile, abort 400
    if not request.json or not 'flowtablefile' in request.json or type(request.json['flowtablefile']) != unicode:
        abort(400)

    ftFile = request.json['flowtablefile']

    #if flowtablefile does not exist, cant apply, so abort 404
    if len(str(errorhandling_remus.get_flowtablefile_EH(ftFile))) == 0:
        abort(404)

    ##if bridge does not exist, cant post, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    sub_remus.applyupdated_flowtablefile(bridge,ftFile)
    return jsonify({'bridge': bridge,
                    'flowtablefile': ftFile})
#Delete a file
@call.route('/flow/flowtablefile/delete/<flowtablefile>', methods=['DELETE'])
@auth.login_required
def deleteFlowTableFile(flowtablefile):
    #if flowtablefile does not exist, cant apply, so abort 404
    if len(str(errorhandling_remus.get_flowtablefile_EH(flowtablefile))) == 0:
        abort(404)

    sub_remus.delete_flowtablefile(flowtablefile)
    
    #check if successfully deleted
    if len(str(errorhandling_remus.get_flowtablefile_EH(flowtablefile))) != 0:
        abort(400)

    return jsonify({'result': True})


#-------------------------FlowGroup-------------------------

#Read flowgroup from bridge
@call.route('/flow/flowgroup/read/<openflowversion>/<bridge>', methods=['GET'])
@auth.login_required
def getFlowGroup(openflowversion, bridge):
    #if does not exist, cant get, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    flowgroup = sub_remus.get_flowgroup(openflowversion,bridge)
    return jsonify({'Flowgroup': flowgroup.splitlines()})

#Create flowgroup for bridge
@call.route('/flow/flowgroup/post/<openflowversion>/<bridge>', methods=['POST'])
@auth.login_required
def addFlowGroup(openflowversion, bridge):
    #if curl no -d, or -d not groupid/type/action, abort 400
    if not request.json or not 'groupid' in request.json or type(request.json['groupid']) != unicode or not 'type' in request.json or type(request.json['type']) != unicode or not 'action' in request.json or type(request.json['action']) != unicode:
        abort(400)

    groupid = request.json['groupid']
    type1 = request.json['type']
    action = request.json['action']

    #if does not exist, cant post, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    #if exist, cant post, so abort 400
    if len(str(errorhandling_remus.get_groupid_EH(openflowversion,bridge,groupid))) != 0:
        abort(400)

    sub_remus.add_flowgroup(openflowversion, bridge, groupid, type1, action)

    #check if successfully created
    if len(str(errorhandling_remus.get_groupid_EH(openflowversion,bridge,groupid))) == 0:
        abort(400)

    return jsonify({'bridge': bridge,
                    'groupid': groupid,
                    'type': type1,
                    'action': action}), 201

#Update flowgroup of bridge
@call.route('/flow/flowgroup/update/<openflowversion>/<bridge>/<groupid>', methods=['PUT'])
@auth.login_required
def updateFlowGroup(openflowversion,bridge,groupid):
    #if curl no -d, or -d not type/action, abort 400
    if not request.json or not 'type' in request.json or type(request.json['type']) != unicode or not 'action' in request.json or type(request.json['action']) != unicode:
        abort(400)

    type1 = request.json['type']
    action = request.json['action']

    #if does not exist, cant update, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    #if does not exist, cant update, so abort 404
    if len(str(errorhandling_remus.get_groupid_EH(openflowversion,bridge,groupid))) == 0:
        abort(404)

    sub_remus.update_flowgroup(openflowversion, bridge, groupid, type1, action)
    return jsonify({'bridge': bridge,
                    'groupid': groupid,
                    'type': type1,
                    'action': action})

#Delete all flow groups from bridge
@call.route('/flow/flowgroup/delete/<openflowversion>/<bridge>', methods=['DELETE'])
@auth.login_required
def deleteAllFlowGroup(openflowversion,bridge):
    #if does not exist, cant update, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    sub_remus.delete_allflowgroup(openflowversion,bridge)

    if len(str(errorhandling_remus.get_any_groupid_EH(openflowversion,bridge))) != 0:
        abort(400)

    return jsonify({'result': True})

#Delete specific flow group from bridge
@call.route('/flow/flowgroup/delete/specific/<openflowversion>/<bridge>/<groupid>', methods=['DELETE'])
@auth.login_required
def deleteSpecificFlowGroup(openflowversion,bridge,groupid):
    #if does not exist, cant update, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    #if does not exist, cant update, so abort 404
    if len(str(errorhandling_remus.get_groupid_EH(openflowversion,bridge,groupid))) == 0:
        abort(404)

    sub_remus.delete_specificflowgroup(openflowversion,bridge,groupid)

    #check if successfully deleted
    if len(str(errorhandling_remus.get_groupid_EH(openflowversion,bridge,groupid))) != 0:
        abort(400)

    return jsonify({'result': True})

#------------------------------Port----------------------------------

@call.route('/read/port/<bridge>', methods=['GET'])
@auth.login_required
def get_port(bridge):
	#check if bridge exists on pc
	if len(str(sub_sean.bridge_pc(bridge))) == 0:
		abort(404)

	return jsonify({'Port': sub_sean.get_ports(bridge).splitlines()})	

@call.route('/add/port/<bridge>', methods=['POST'])
@auth.login_required
def add_port(bridge):
      
	#check if bridge already exists
	if len(str(sub_sean.bridge_pc(bridge))) == 0:
		abort(404)

	if not request.json:
		abort(400)

	if not 'port' in request.json or type(request.json['port']) != unicode:
		abort(400)
	
	port = request.json['port']

        #check if interface already exists on pc
        if len(str(sub_sean.int_pc(port))) == 0:
                abort(404)

	sub_sean.add_ports(bridge, port)
	return jsonify({'Bridge': bridge,
			'Port': port}), 201

@call.route('/delete/port/<bridge>', methods=['DELETE'])
@auth.login_required
def del_port(bridge):
	
	#check if bridge exists
	if len(str(sub_sean.bridge_pc(bridge))) == 0:
		abort(404)

	if not request.json or not 'port' in request.json:
		abort(400)

	port = request.json['port']

	#check if port exists on bridge
	if len(str(sub_sean.port_bridge(bridge, port))) == 0:
		abort(404)		

	sub_sean.del_ports(bridge, port)
	
	#check if delete was successful
	if len(str(sub_sean.port_bridge(bridge, port))) != 0:
		abort(404)	

	return jsonify({'Result': True})

@call.route('/update/port/<bridge>/<port>', methods=['PUT'])
@auth.login_required
def update_port(bridge, port):

	#check if bridge exist
	if len(str(sub_sean.bridge_pc(bridge))) == 0:
		abort(404)
	
	#check if port exist on bridge
	if len(str(sub_sean.port_bridge(bridge, port))) == 0:
		abort(404)

	if not request.json or not 'action' in request.json:
		abort(400)

	action = request.json['action']
	sub_sean.update_ports(bridge, port, action)
	return jsonify({'Bridge': bridge,
			'Port': port,
			'Action': action})


#-----------------------------Port mirror---------------------------------

@call.route('/read/mirror/<mirror>', methods=['GET'])
@auth.login_required
def get_mirror(mirror):
	
	#check if mirror exists
	if len(str(sub_sean.check_mirror(mirror))) == 0:
		abort(404)

        return jsonify({'Mirror': sub_sean.get_mirror(mirror).splitlines()})
	
@call.route('/add/mirror/<bridge>', methods=['POST'])
@auth.login_required
def add_mirror(bridge):

        #check if bridge already exists
        if len(str(sub_sean.bridge_pc(bridge))) == 0:
                abort(404)
	
        if not request.json or not 'port1' in request.json:
                abort(400)

        if not request.json or not 'port2' in request.json:
                abort(400)
      
	if not request.json or not 'port3' in request.json:
                abort(400)

        if not request.json or not 'port4' in request.json:
                abort(400)

        if not request.json or not 'name' in request.json:
                abort(400)

        if not request.json or not 'dest' in request.json:
                abort(400)

        if not request.json or not 'source' in request.json:
                abort(400)

        if not request.json or not 'output' in request.json:
                abort(400)
	
        port1 = request.json['port1']
	port2 = request.json['port2']
	port3 = request.json['port3']
        port4 = request.json['port4']
        name = request.json['name']
        dest = request.json['dest']
        source = request.json['source']
        output = request.json['output']

        #check if port already exists
        if len(str(sub_sean.int_pc(port2))) == 0:
                abort(404)

        if len(str(sub_sean.int_pc(port4))) == 0:
                abort(404)

        #check if port exist on bridge
        if len(str(sub_sean.port_bridge(bridge, port2))) == 0:
                abort(404)

        if len(str(sub_sean.port_bridge(bridge, port4))) == 0:
                abort(404)
	
        if port2 == port4:
                abort(400)

        #check if mirror with same name already exists
        if len(str(sub_sean.check_mirror(name))) != 0:
                abort(400)

        sub_sean.add_mirror(bridge, port1, port2, port3, port4, name, dest, source, output)

        return jsonify({'Bridge': bridge,
			'Name': name,
			'Destination': dest,
			'Source': source,
			'Output': output}), 201


@call.route('/update/mirror/<bridge>', methods=['PUT'])
@auth.login_required
def update_mirror(bridge):

        #check if bridge already exists
        if len(str(sub_sean.bridge_pc(bridge))) == 0:
                abort(404)

        if not request.json or not 'port1' in request.json:
                abort(400)

        if not request.json or not 'port2' in request.json:
                abort(400)

        if not request.json or not 'port3' in request.json:
                abort(400)

        if not request.json or not 'port4' in request.json:
                abort(400)

        if not request.json or not 'name' in request.json:
                abort(400)

        if not request.json or not 'dest' in request.json:
                abort(400)

        if not request.json or not 'source' in request.json:
                abort(400)

        if not request.json or not 'output' in request.json:
                abort(400)

        port1 = request.json['port1']
        port2 = request.json['port2']
        port3 = request.json['port3']
        port4 = request.json['port4']
        name = request.json['name']
        dest = request.json['dest']
        source = request.json['source']
        output = request.json['output']

        #check if port already exists
        if len(str(sub_sean.int_pc(port2))) == 0:
                abort(404)

        if len(str(sub_sean.int_pc(port4))) == 0:
                abort(404)

        #check if port exist on bridge
        if len(str(sub_sean.port_bridge(bridge, port2))) == 0:
                abort(404)

        if len(str(sub_sean.port_bridge(bridge, port4))) == 0:
                abort(404)

        if port2 == port4:
                abort(400)

        sub_sean.add_mirror(bridge, port1, port2, port3, port4, name, dest, source, output)

        return jsonify({'Bridge': bridge,
                        'Name': name,
                        'Destination': dest,
                        'Source': source,
                        'Output': output})


@call.route('/delete/mirror/<bridge>/<mirror>', methods=['DELETE'])
@auth.login_required
def del_mirror(bridge, mirror):

        #check if bridge exists
        if len(str(sub_sean.bridge_pc(bridge))) == 0:
                abort(404)

        #check if mirror exists
        if len(str(sub_sean.check_mirror(mirror))) == 0:
                abort(404)

        sub_sean.del_mirror(bridge, mirror)

        #check if mirror gets deleted successfully
        if len(str(sub_sean.check_mirror(mirror))) != 0:
                abort(400)

        return jsonify({'Result': True})


#----------------------------NetFlow--------------------------------

@call.route('/read/netflow/<bridge>', methods=['GET'])
@auth.login_required
def get_netflow(bridge):
        #check if bridge exists on pc
        if len(str(sub_sean.bridge_pc(bridge))) == 0:
                abort(404)

        return jsonify({'Bridge': bridge,
                        'Netflow': sub_sean.get_netflow(bridge).splitlines()})


@call.route('/update/netflow/<bridge>', methods=['PUT'])
@auth.login_required
def update_netflow(bridge):
        #check if bridge exists on pc
        if len(str(sub_sean.bridge_pc(bridge))) == 0:
                abort(404)

	if not request.json or not 'options' in request.json:
		abort(400)

        options = request.json['options']

        sub_sean.update_netflow(bridge,options)

        return jsonify({'Bridge': bridge,
                        'Options': options})


@call.route('/add/netflow/<bridge>', methods=['POST'])
@auth.login_required
def add_netflow(bridge):
        #check if bridge exists on pc
        if len(str(sub_sean.bridge_pc(bridge))) == 0:
                abort(404)

        if not request.json or not 'target' in request.json:
                abort(400)
        if not request.json or not 'timeout' in request.json:
                abort(400)
	
	target = request.json['target']
        timeout = request.json['timeout']

        sub_sean.add_netflow(bridge, target, timeout)

        return jsonify({'Bridge': bridge,
                        'Target': target,
			'Timeout': timeout})


@call.route('/delete/netflow/<bridge>', methods=['DELETE'])
@auth.login_required
def del_netflow(bridge):
        #check if bridge exists on pc
        if len(str(sub_sean.bridge_pc(bridge))) == 0:
                abort(404)

        sub_sean.del_netflow(bridge)

        return jsonify({'Result': True})


#-------------------------VLAN----------------------------

@call.route('/addvlan', methods=['POST'])
@auth.login_required
def addvlan():
	bridge = request.json['bridge']
	interface = request.json['interface']
	tag = request.json['tag']
	sub_joey.add_vlan(bridge,interface,tag)
	return jsonify ({'bridge' : bridge,
			'interface' : interface,
			'tag' : tag}), 201

@call.route('/delvlan/<interface>', methods=['DELETE'])
@auth.login_required
def delvlan(interface):
	sub_joey.del_vlan(interface)
	return jsonify({'VLAN Deleted' : interface}),201

@call.route('/updatevlan/<interface>', methods=['PUT'])
@auth.login_required
def updatevlan(interface):
	tag = request.json['tag']
	sub_joey.update_vlan(interface, tag)
	return jsonify({'VLAN Updated' : interface ,
			'tag' : tag}), 201

@call.route('/showvlan', methods=['GET'])
@auth.login_required
def showvlan():
        bridge = sub_joey.show_bridge()
        return jsonify ({'bridge' : bridge.splitlines()})


#---------------------------Trunk---------------------------

@call.route('/showtrunk', methods=['GET'])
@auth.login_required
def showtrunk():
	bridge = sub_joey.show_bridge()
	return jsonify ({'bridge' : bridge.splitlines()})

@call.route('/addtrunk', methods=['POST'])
@auth.login_required
def addtrunk():
        interface = request.json['interface']
        trunk = request.json['trunk']
        sub_joey.add_trunk(interface,trunk)
        return jsonify ({'interface' : interface,
                        'trunk' : trunk}), 201

@call.route('/updatetrunk/<interface>', methods=['PUT'])
@auth.login_required
def updatetrunk(interface):
        trunk = request.json['trunk']
        sub_joey.update_trunk(interface, trunk)
        return jsonify({'Trunk Updated' : interface ,
                        'trunk' : trunk}), 201

@call.route('/deltrunk/<interface>', methods=['DELETE'])
@auth.login_required
def deltrunk(interface):
        sub_joey.del_trunk(interface)
        return jsonify({'Trunk Deleted' : interface}),201


#----------------------------QoS-------------------------------

#Add a qos configuration for the particular interface
@call.route('/addqos/<interface>', methods=['POST'])
@auth.login_required
def add_qos(interface):
	qos = request.json['qos']
	sub_abdullah.add_qos(interface,qos)
	return jsonify({'Interface': interface,
			'QoS': qos}),201

#Update QoS configuration for the particular interface
@call.route('/updateqos/<interface>', methods=['PUT'])
@auth.login_required
def update_qos(interface):
	qos = request.json['qos']
	sub_abdullah.update_qos(interface,qos)
	return jsonify({'Interface': interface,
			'QoS': qos}), 201

#Get QoS configuration for the particular interface
@call.route('/showqos/<interface>', methods=['GET'])
@auth.login_required
def get_qos(interface):
	return jsonify({'Information about the interface':sub_abdullah.show_qos(interface).splitlines()})

#Get QoS ingress_policing_rate for the interface
@call.route('/showqosrate/<interface>', methods=['GET'])
@auth.login_required
def get_qosrate(interface):
	return jsonify({'Ingress_policing_rate':sub_abdullah.show_qosrate(interface)})

#Get QoS ingress_policing_burst for the interface
@call.route('/showqosburst/<interface>', methods=['GET'])
@auth.login_required
def get_qosburst(interface):
        return jsonify({'Ingress_policing_burst':sub_abdullah.show_qosburst(interface)})


#Delete QoS configuration for the particular interface
@call.route('/deleteqos/<interface>', methods=['DELETE'])
@auth.login_required
def del_qos(interface):
	sub_abdullah.del_qosrate(interface)
	sub_abdullah.del_qosburst(interface)
	return jsonify ({"Interface": interface,
			'QoS Ingress_policing_rate': '0',
			'QoS Ingress_policing_burst': '0'}),201


#------------------------------SSL----------------------------------

#Add SSL Configuration
@call.route('/addssl', methods=['POST'])
@auth.login_required
def add_ssl():
	privatekey = request.json['Private Key']
	certificate = request.json['Certificate']
	cacert = request.json['CA Certificate']
	sub_abdullah.add_ssl(privatekey,certificate,cacert)
	return jsonify ({"Private Key" : privatekey,
			"Certificate" : certificate,
			"CA Certificate" : cacert}),201

#Get SSL Configuration
@call.route('/getssl', methods=['GET'])
@auth.login_required
def get_ssl():
	return jsonify({'SSL COnfiguration':sub_abdullah.get_ssl().splitlines()})

#Update SSL Configuration
@call.route('/updatessl', methods=['PUT'])
@auth.login_required
def update_ssl():
	privatekey = request.json['Private Key']
        certificate = request.json['Certificate']
        cacert = request.json['CA Certificate']
	sub_abdullah.update_ssl(privatekey,certificate,cacert)
        return jsonify ({"Private Key" : privatekey,
                        "Certificate" : certificate,
                        "CA Certificate" : cacert}),201

#Delete SSL Configuration
@call.route('/deletessl', methods=['DELETE'])
@auth.login_required
def del_ssl():
	sub_abdullah.del_ssl()
	return jsonify ({"SSL Configuration": "Cleared" }),201


#-------------------------------STP----------------------------------

#Add STP Configuration for Bridge
@call.route('/addstppriority/<bridge>', methods=['POST'])
@auth.login_required
def add_stpp(bridge):
	sub_abdullah.en_stp(bridge)
	priority = request.json['priority']
	sub_abdullah.add_stppri(bridge,priority)
	return jsonify ({'STP Enabled on bridge': bridge,
			'STP Priority': priority}),201

#Add STP Configuration for Port
@call.route('/addstpcost/<port>', methods=['POST'])
@auth.login_required
def add_stpc(port):
	cost = request.json['cost']
	sub_abdullah.add_stpcost(port,cost)
	return jsonify ({'Port': port,
			'STP Cost': cost}),201


#Update STP Configuration for Bridge
@call.route('/updatestppriority/<bridge>', methods=['PUT'])
@auth.login_required
def update_stpp(bridge):
	priority = request.json['priority']
	sub_abdullah.update_stppri(bridge,priority)
	return jsonify({'Bridge': bridge,
			'STP Priority Updated': priority}),201

#Update STP Configuration for Port
@call.route('/updatestpcost/<port>', methods=['PUT'])
@auth.login_required
def update_stpcost(port):
	cost = request.json['cost']
	sub_abdullah.update_stpcost(port,cost)
	return jsonify({'Port': port,
			'STP Cost Updated': cost}),201

#Get STP Configuration for Bridge Priority
@call.route('/getstppriority/<bridge>', methods=['GET'])
@auth.login_required
def get_stppri(bridge):
	return jsonify({'STP Priority':sub_abdullah.get_stppriority(bridge)})

#Get STP Configuration for Port Cost
@call.route('/getstpcost/<port>', methods=['GET'])
@auth.login_required
def get_stpcost(port):
	return jsonify({'STP Cost': sub_abdullah.get_stpcost(port)})

#Delete STP Configuraton for Birdge
@call.route('/deletestppriority/<bridge>', methods=['DELETE'])
@auth.login_required
def del_stppri(bridge):
	sub_abdullah.del_stpbridge(bridge)
	return jsonify({'STP Config(Priority) for Bridge': 'Cleared',
			'Bridge': bridge}),201

#Delete STP Configruation for Port
@call.route('/deletestpcost/<port>', methods=['DELETE'])
@auth.login_required
def del_stpcost(port):
	sub_abdullah.del_stpport(port)
	return jsonify({'STP Config(Cost) for Port': 'Cleared',
			'Port': port}),201


#-------------------------OpenFlowVersion--------------------------------

#Add OpenFlowVersion
@call.route('/addopenflowversion/<bridge>', methods=['POST'])
@auth.login_required
def add_openflowversion(bridge):
	protocol = request.json['protocol']
	sub_abdullah.add_openflowv(bridge,protocol)
	return jsonify({'Bridge': bridge,
			'OpenFlow Version Added':protocol}),201

#Update OpenFlowVersion
@call.route('/updateopenflowversion/<bridge>', methods=['PUT'])
@auth.login_required
def update_openflowversion(bridge):
        protocol = request.json['protocol']
        sub_abdullah.add_openflowv(bridge,protocol)
        return jsonify({'Bridge': bridge,
                        'OpenFlow Version Updated':protocol}),201

#Delete OpenFlow Version
@call.route('/delopenflowversion/<bridge>', methods=['DELETE'])
@auth.login_required
def delete_openflowversion(bridge):
	sub_abdullah.del_openflowv(bridge)
	return jsonify ({'Bridge':bridge,
			'OpenFlow  Version': 'CLEARED'}),201

#Get OpenFlow Version
@call.route('/getopenflowversion/<bridge>', methods=['GET'])
@auth.login_required
def get_openflowversion(bridge):
	return jsonify({'OpenFlow Version':sub_abdullah.get_openflowv(bridge)})

if __name__ == '__main__':
    call.run(debug=True)
