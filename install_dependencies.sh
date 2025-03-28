#!/bin/bash

# Wireshark 
sudo add-apt-repository -y ppa:wireshark-dev/stable
sudo apt update
sudo apt install -y wireshark

# Docker & Docker Compose 
sudo apt update
sudo apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce=5:19.03.9~3-0~ubuntu-$(lsb_release -cs) docker-ce-cli=5:19.03.9~3-0~ubuntu-$(lsb_release -cs) containerd.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

# oai network config
sudo sysctl net.ipv4.conf.all.forwarding=1
sudo iptables -P FORWARD ACCEPT

# docker config
sudo groupadd docker
sudo usermod -aG docker $USER

# docker image
sudo docker pull oaisoftwarealliance/oai-amf:v2.0.0
sudo docker pull oaisoftwarealliance/oai-nrf:v2.0.0
sudo docker pull oaisoftwarealliance/oai-upf:v2.0.0
sudo docker pull oaisoftwarealliance/oai-smf:v2.0.0
sudo docker pull oaisoftwarealliance/oai-udr:v2.0.0
sudo docker pull oaisoftwarealliance/oai-udm:v2.0.0
sudo docker pull oaisoftwarealliance/oai-ausf:v2.0.0
sudo docker pull oaisoftwarealliance/oai-upf-vpp:v2.0.0
sudo docker pull oaisoftwarealliance/oai-nssf:v2.0.0
sudo docker pull oaisoftwarealliance/oai-pcf:v2.0.0
sudo docker pull oaisoftwarealliance/oai-lmf:v2.0.0
sudo docker pull oaisoftwarealliance/trf-gen-cn5g:latest
sudo docker pull oaisoftwarealliance/oai-gnb:v2.1.0
sudo docker pull oaisoftwarealliance/oai-nr-ue:v2.1.0
docker pull onehouwong/oai-nr-ue:nr.attack.v2.1.0


# Python
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev
sudo apt install -y python3-pip
pip3 install Flask

#Pyxterm
git clone https://github.com/cs01/pyxtermjs.git
pip3 install \
    bidict==0.21.2 \
    click==8.0.1 \
    flask==2.0.1 \
    flask-socketio==5.1.1 \
    itsdangerous==2.0.1 \
    jinja2==3.0.1 \
    markupsafe==2.0.1 \
    python-engineio==4.2.1 \
    python-socketio==5.4.0 \
    werkzeug==2.0.1

#5G-Spector

#5Greplay
sudo apt update && sudo apt install gcc make git libxml2-dev libpcap-dev libconfuse-dev libsctp-dev
wget https://github.com/Montimage/mmt-dpi/releases/download/v1.7.9/mmt-dpi_1.7.9_8694eaa_Linux_x86_64.deb && sudo dpkg -i ./mmt-dpi*.deb && sudo ldconfig










echo "Install Seccessed."



