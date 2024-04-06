#!/bin/bash

# Creates venv
python3 -m venv website_venv --system-site-packages
echo "Venv created, installing tools"

# Checks if dir exists or not
if ! test -d static/history/; then
  mkdir static/history
fi

# Installs tools
source website_venv/bin/activate
pip3 install -r requirements.txt --no-deps plip
cd website_venv
wget http://www.lephar.com/download/ledock_linux_x86 http://www.lephar.com/download/lepro_linux_x86
chmod +x ledock_linux_x86 lepro_linux_x86