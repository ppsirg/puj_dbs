sudo apt-get install libaio1 python-pip
#instant client installation
sudo mkdir /opt/oracle/
unzip instantclient-basic-linux.x64-19.6.0.0.0dbru.zip
sudo scp -vr instantclient_19_6/ /ospt/oracle/
export LD_LIBRARY_PATH=/opt/oracle/instantclient_19_6/:$LD_LIBRARY_PATH
#python libs installation
pip install virtualenv
virtualenv -p /usr/bin/python3 env
source env/bin/activate
pip install -r requirements.txt
#must have access to database with credentials described in
#connection.py, run in 127.127.0.1:8000
uvicorn app:app --reload
