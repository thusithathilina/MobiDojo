from flask import Blueprint, render_template, jsonify
import subprocess

function1_bp = Blueprint('function1', __name__, template_folder='/')

@function1_bp.route('/')
def show():
    return render_template('function1.html')

@function1_bp.route('/check_status')
def check_status():
    try:
        result = subprocess.run(['docker', 'ps', '-a'], capture_output=True, text=True)
        containers = result.stdout.split('\n')[1:-1]

        container_status = []

        for container in containers:
            parts = container.split()
            name = parts[-1]
            status = 'healthy' if '(healthy)' in container else 'unhealthy'
                       
            if 'ue' in name.lower():
                group = 'UE'
            elif 'gnb' in name.lower():
                group = 'Base Station'
            else:
                group = 'Core Network'

            container_info = {
                'name': name,
                'status': status,
                'group': group
            }
            container_status.append({
                'name': name,
                'status': status,
                'group': group
            })

        return jsonify(container_status)

    except Exception as e:
        return jsonify({'error': str(e)})
@function1_bp.route('/check_dn')
def check_dn():
    print("Entering check_dn function")
    try:
        docker_cmd = ['docker', 'exec', '-i', 'rfsim5g-oai-nr-ue1', '/bin/bash', '-c', 'ping -I oaitun_ue1 -c 5 www.google.com']
        print(f"Executing command: {' '.join(docker_cmd)}")
        
        result = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=30)
        print(f"Command executed. Return code: {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        
        success = "0% packet loss" in result.stdout
        print(f"Ping success: {success}")
        
        return jsonify({'status': success, 'output': result.stdout})
    except subprocess.TimeoutExpired as te:
        print(f"Timeout error: {str(te)}")
        return jsonify({'status': False, 'error': 'Ping command timed out', 'details': str(te)})
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return jsonify({'status': False, 'error': str(e), 'type': type(e).__name__})
  