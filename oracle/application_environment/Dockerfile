FROM python/3-alpine

WORKDIR /opt/app

COPY . .

RUN mkdir /opt/oracle/
RUN wget https://download.oracle.com/otn_software/linux/instantclient/19600/instantclient-basic-linux.x64-19.6.0.0.0dbru.zip
RUN unzip instantclient-basic-linux.x64-19.6.0.0.0dbru.zip
RUN scp -vr instantclient_19_6/ /ospt/oracle/
RUN export LD_LIBRARY_PATH=/opt/oracle/instantclient_19_6/:$LD_LIBRARY_PATH

#python libs installation
RUN pip install virtualenv
RUN virtualenv -p /usr/bin/python3 env
RUN source env/bin/activate
RUN pip install -r requirements.txt
#must have access to database with credentials described in
#connection.py
#uvicorn app:app --reload

EXPOSE 80
CMD ["uvicorn", "app:app"]