from flask import Blueprint, render_template, request, jsonify
import subprocess
import os

function5_bp = Blueprint('function5', __name__)

@function5_bp.route('/')
def function5():
    return render_template('function5.html')

@function5_bp.route('/launch_spector', methods=['POST'])
def launch_spector():
    attack_type = request.form.get('attack_type')
    val1 = request.form.get('val1')
    val2 = request.form.get('val2')
    addon = request.form.get('addon')

    base_command = "sudo ./nr-uesoftmodem -O nr-ue.conf -E --sa --rfsim -r 106 --numerology 1 -C 3619200000 --sa --rfsim --rfsimulator.serveraddr 192.168.70.153"
    
    command_map = {
        '1': f"{base_command} --bts-attack {val1} --bts-delay {val2}",
        '2': f"{base_command} --blind-dos-attack {val1} --RRC-TMSI {val2}",
        '3': f"{base_command} --dnlink-dos-attack {val1}",
        '4': f"{base_command} --dnlink-imsi-extr {val1}",
        '5': f"{base_command} --uplink-dos-attack {val1}",
        '6': f"{base_command} --uplink-imsi-extr {val1}",
        '7': f"{base_command} --null-cipher-integ {val1}"
    }

    # Validate input
    if attack_type in ['1', '2']:
        if not val1.isdigit() or not 1 <= int(val1) <= 999:
            return jsonify({"status": "error", "message": "Invalid val_1. Must be between 1 and 999."})
    elif attack_type == '3':
        if not val1.isdigit() or not 1 <= int(val1) <= 999:
            return jsonify({"status": "error", "message": "Invalid val_1. Must be between 1 and 999."})
    elif attack_type == '4':
        if not val1.isdigit() or not 1 <= int(val1) <= 4:
            return jsonify({"status": "error", "message": "Invalid val_1. Must be between 1 and 4."})
    elif attack_type in ['5', '6']:
        if not val1.isdigit() or not 1 <= int(val1) <= 999:
            return jsonify({"status": "error", "message": "Invalid val_1. Must be between 1 and 999."})
    elif attack_type == '7':
        if not val1.isdigit() or not 1 <= int(val1) <= 2:
            return jsonify({"status": "error", "message": "Invalid val_1. Must be 1 or 2."})

    command = command_map.get(attack_type)
    if command:
        if addon == 'emergency':
            command += " --rrc-911"

        try:
            build_dir = os.path.expanduser('~/MobiDojo/OAI-5G-nr.attack.v2.1.0/cmaketargets/ranbuild/build')
            gnome_terminal_command = f"gnome-terminal -- bash -c 'cd {build_dir} && {command}; exec bash'"
            subprocess.Popen(gnome_terminal_command, shell=True)
            return jsonify({"status": "success", "message": "Attack launched successfully in a new terminal"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return jsonify({"status": "error", "message": "Invalid attack type"})

@function5_bp.route('/launch_replay', methods=['POST'])
def launch_replay():
    pcap_file = request.form.get('pcap_file')
    if pcap_file:
        try:
            replay_dir = os.path.expanduser('~/MobiDojo/5greplay')
            command = f"sudo ./5greplay replay -t pcap/{pcap_file}"
            gnome_terminal_command = f"gnome-terminal -- bash -c 'cd {replay_dir} && {command}; exec bash'"
            subprocess.Popen(gnome_terminal_command, shell=True)
            return jsonify({"status": "success", "message": "Replay launched successfully in a new terminal"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        return jsonify({"status": "error", "message": "No PCAP file selected"})

@function5_bp.route('/manual_modify', methods=['POST'])
def manual_modify():
    try:
        modify_dir = os.path.expanduser('~/MobiDojo/pcap_modifier')
        command = "python3 build.py"
        subprocess.Popen(command, cwd=modify_dir, shell=True)
        return jsonify({"status": "success", "message": "Manual Modify launched successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@function5_bp.route('/auto_modify', methods=['POST'])
def auto_modify():
    try:
        modify_dir = os.path.expanduser('~/MobiDojo/pcap_modifier')
        command = "python3 mutator.py"
        gnome_terminal_command = f"gnome-terminal -- bash -c 'cd {modify_dir} && {command}; exec bash'"
        subprocess.Popen(gnome_terminal_command, shell=True)
        return jsonify({"status": "success", "message": "Auto Modify launched successfully in a new terminal"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def init_function5(app, socketio):
    pass
