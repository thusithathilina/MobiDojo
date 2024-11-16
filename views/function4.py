import os
import pty
import select
import subprocess
import termios
import struct
import fcntl
import logging
from flask import Blueprint, render_template
from flask_socketio import emit

function4_bp = Blueprint('function4', __name__)

logging.getLogger("werkzeug").setLevel(logging.ERROR)

def set_winsize(fd, row, col, xpix=0, ypix=0):
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)

def read_and_forward_pty_output(fd, socket):
    max_read_bytes = 1024 * 20
    while True:
        socket.sleep(0.01)
        if fd:
            timeout_sec = 0
            (data_ready, _, _) = select.select([fd], [], [], timeout_sec)
            if data_ready:
                output = os.read(fd, max_read_bytes).decode(errors="ignore")
                socket.emit("pty-output", {"output": output}, namespace="/pty")

@function4_bp.route("/")
def index():
    return render_template("function4.html")

def init_function4(app, socketio):
    @socketio.on("pty-input", namespace="/pty")
    def pty_input(data):
        if app.config.get("fd"):
            os.write(app.config["fd"], data["input"].encode())

    @socketio.on("resize", namespace="/pty")
    def resize(data):
        if app.config.get("fd"):
            set_winsize(app.config["fd"], data["rows"], data["cols"])

    @socketio.on("connect", namespace="/pty")
    def connect():
        if app.config.get("child_pid"):
            return

        (child_pid, fd) = pty.fork()
        if child_pid == 0:
            subprocess.run(app.config.get("cmd", ["bash"]))
        else:
            app.config["fd"] = fd
            app.config["child_pid"] = child_pid
            set_winsize(fd, 50, 50)
            socketio.start_background_task(target=read_and_forward_pty_output, fd=fd, socket=socketio)

    return socketio