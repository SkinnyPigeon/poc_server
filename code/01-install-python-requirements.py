import os
os.system('apt update')
os.system('apt install python3-pip -y')
os.system('apt-get install libpq-dev python-dev -y')
os.system('pip3 install flask flask-cors flask-restplus gunicorn python-dotenv mailjet_rest')
os.system('pip3 uninstall --yes Werkzeug')
os.system('pip3 install Werkzeug==0.16.1')