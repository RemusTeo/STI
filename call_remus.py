#!flask/bin/python
import sub_remus
import errorhandling_remus
from flask import Flask, jsonify, abort, request, make_response
from flask_httpauth import HTTPBasicAuth
import json


call = Flask(__name__)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'remus':
        return 'teo'
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

#Read bridge
@call.route('/bridge/read/<bridge>', methods=['GET'])
@auth.login_required
def getBridge(bridge):
    #if does not exist, cant get, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    bridge = sub_remus.get_bridge(bridge)
    return jsonify({'Bridge':bridge.splitlines()})

#Create bridge
@call.route('/bridge/post', methods=['POST'])
@auth.login_required
def addBridge():
    #if curl no -d, or -d not bridge, abort 400
    if not request.json or not 'bridge' in request.json or type(request.json['bridge']) != unicode:
        abort(400)

    bridge = request.json['bridge']

    #if already exist, cant post, so abort 400
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) != 0:
        abort(400)

    sub_remus.add_bridge(bridge)
    
    #check if added successfully
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(400)

    return jsonify({'bridge': bridge}), 201

#Update bridge
@call.route('/bridge/update/<bridge>', methods=['PUT'])
@auth.login_required
def updateBridge(bridge):
    #if curl no -d, or -d not options, abort 400
    if not request.json or not 'options' in request.json or type(request.json['options']) != unicode:
        abort(400)

    options = request.json['options']

    #if does not exist, cant update, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    sub_remus.update_bridge(bridge, options)
    
    return jsonify({'bridge': bridge,
                    'options': options})

#Delete bridge
@call.route('/bridge/delete/<bridge>', methods=['DELETE'])
@auth.login_required
def deleteBridge(bridge):    
    #if does not exist, cant delete, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    sub_remus.delete_bridge(bridge)

    if len(str(errorhandling_remus.get_bridge_EH(bridge))) != 0:
        abort(400)

    return jsonify({'result': True})



#--------------------------Flow---------------------------

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
@call.route('/flow/flowgroup/read/<bridge>', methods=['GET'])
@auth.login_required
def getFlowGroup(bridge):
    #if does not exist, cant get, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    flowgroup = sub_remus.get_flowgroup(bridge)
    return jsonify({'Flowgroup': flowgroup.splitlines()})

#Create flowgroup for bridge
@call.route('/flow/flowgroup/post/<bridge>', methods=['POST'])
@auth.login_required
def addFlowGroup(bridge):
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
    if len(str(errorhandling_remus.get_groupid_EH(bridge,groupid))) != 0:
        abort(400)

    sub_remus.add_flowgroup(bridge, groupid, type1, action)
    
    #check if successfully created
    if len(str(errorhandling_remus.get_groupid_EH(bridge,groupid))) == 0:
        abort(400)

    return jsonify({'bridge': bridge,
                    'groupid': groupid,
                    'type': type1,
                    'action': action}), 201

#Update flowgroup of bridge
@call.route('/flow/flowgroup/update/<bridge>/<groupid>', methods=['PUT'])
@auth.login_required
def updateFlowGroup(bridge,groupid):
    #if curl no -d, or -d not type/action, abort 400
    if not request.json or not 'type' in request.json or type(request.json['type']) != unicode or not 'action' in request.json or type(request.json['action']) != unicode:
        abort(400)

    type1 = request.json['type']
    action = request.json['action']

    #if does not exist, cant update, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    #if does not exist, cant update, so abort 404
    if len(str(errorhandling_remus.get_groupid_EH(bridge,groupid))) == 0:
        abort(404)

    sub_remus.update_flowgroup(bridge, groupid, type1, action)
    return jsonify({'bridge': bridge,
                    'groupid': groupid,
                    'type': type1,
                    'action': action})

#Delete all flow groups from bridge
@call.route('/flow/flowgroup/delete/<bridge>', methods=['DELETE'])
@auth.login_required
def deleteAllFlowGroup(bridge):
    #if does not exist, cant update, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    sub_remus.delete_allflowgroup(bridge)

    if len(str(errorhandling_remus.get_any_groupid_EH(bridge))) != 0:
        abort(400)

    return jsonify({'result': True})

#Delete specific flow group from bridge
@call.route('/flow/flowgroup/delete/specific/<bridge>/<groupid>', methods=['DELETE'])
@auth.login_required
def deleteSpecificFlowGroup(bridge,groupid):
    #if does not exist, cant update, so abort 404
    if len(str(errorhandling_remus.get_bridge_EH(bridge))) == 0:
        abort(404)

    #if does not exist, cant update, so abort 404
    if len(str(errorhandling_remus.get_groupid_EH(bridge,groupid))) == 0:
        abort(404)

    sub_remus.delete_specificflowgroup(bridge,groupid)

    #check if successfully deleted
    if len(str(errorhandling_remus.get_groupid_EH(bridge,groupid))) != 0:
        abort(400)

    return jsonify({'result': True})
    
if __name__ == '__main__':
    call.run(debug=True)
