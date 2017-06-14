#!flask/bin/python
import sub_hakim
from flask import Flask, jsonify, request, make_response
from flask_httpauth import HTTPBasicAuth

read = Flask(__name__)
auth = HTTPBasicAuth()

#GET Bridge
@read.route('/read', methods=['GET'])
@auth.login_required
def get_ovsvsctl():
	bridge = sub_hakim.get_ovsvsctl()
	return jsonify({'Bridge' :bridge.splitlines()})

#POST Bridge
@read.route('/write', methods=['POST'])
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
@read.route('/delete/<bridge_id>', methods=['DELETE'])
@auth.login_required
def delete_input(bridge_id):
        if len(bridge_id) > 0: #if the bride exist
                sub_hakim.delete_input(bridge_id)
        else:
                abort(404)
        return jsonify({'result':True})

#UPDATE Bridge on a particular br
@read.route('/updatebridge/<bridge_id>', methods=['PUT'])
@auth.login_required
def update_bridge(bridge_id):
        stp = request.json['stp_enable']
	sub_hakim.update_bridge(bridge_id,stp)
        return jsonify({'stp_enable' : stp.rstrip()
                                        }), 201

#GET Failmode on particular br
@read.route('/read/<bridge_id>', methods=['GET'])
@auth.login_required
def read_failmode(bridge_id):
       mode =  sub_hakim.read_failmode(bridge_id)
       return jsonify({'fail_mode' : mode.rstrip()})

#POST Failmode on particular br
@read.route('/write/<bridge_id>', methods=['POST'])
@auth.login_required
def create_failmode(bridge_id):
        mode = request.json['fail_mode']
        sub_hakim.create_failmode(bridge_id,mode)
        return jsonify({'fail_mode' : mode
			                      }), 201

#DELETE Failmode on particular br
@read.route('/deletemode/<bridge_id>', methods=['DELETE'])
@auth.login_required
def delete_mode(bridge_id):
        if len(bridge_id) > 0: #if the bride exist
                sub_hakim.delete_mode(bridge_id)
        else:
                abort(404)
        return jsonify({'result':True})

#UPDATE Failmode on particular br
@read.route('/updatemode/<bridge_id>', methods=['PUT'])
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

#Get Controller
@read.route('/get/<bridge_id>', methods=['GET'])
@auth.login_required
def read_controller(bridge_id):
       control =  sub_hakim.read_controller(bridge_id)
       return jsonify({'controller' : control.rstrip()})

#POST Controller on particular br
@read.route('/create/<bridge_id>', methods=['POST'])
@auth.login_required
def create_controller(bridge_id):
        control = request.json['Controller']
        sub_hakim.create_controller(bridge_id,control)
        return jsonify({'Controller' : control
                                        }), 201

#DELETE Controller on particular br
@read.route('/deletecontroller/<bridge_id>', methods=['DELETE'])
@auth.login_required
def delete_controller(bridge_id):
	if len(bridge_id) > 0: #if the bride exist
		sub_hakim.delete_controller(bridge_id)
	else:
		abort(404)
	return jsonify({'result':True})

#UPDATE Controller on particular br
@read.route('/updatecontroller/<bridge_id>', methods=['PUT'])
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

#Error handling
@auth.get_password
def get_password(username):
        if username == 'nur':
                return 'hakim'
        return None

@auth.error_handler
def unauthorised():
        return make_response(jsonify({'error': 'Unauthorised access'}), 403)

@read.errorhandler(400)
def not_found(error):
        return make_response(jsonify({'error' : 'Bad request'}), 400)

@read.errorhandler(404)
def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	read.run(debug=True)