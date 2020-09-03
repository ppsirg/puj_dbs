FROM python:3.8
WORKDIR /opt/app
RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y
RUN apt-get -y install libaio1 python-pip
RUN python -m pip install cx_Oracle --upgrade

COPY . .
ENV WAIT_VERSION 2.7.3
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

RUN mkdir /opt/oracle/
RUN wget https://download.oracle.com/otn_software/linux/instantclient/19600/instantclient-basic-linux.x64-19.6.0.0.0dbru.zip
RUN apt-get -y install unzip
RUN unzip instantclient-basic-linux.x64-19.6.0.0.0dbru.zip
RUN cp -vr instantclient_19_6/ /opt/oracle/
RUN export LD_LIBRARY_PATH=/opt/oracle/instantclient_19_6/:$LD_LIBRARY_PATH
RUN sh -c "echo /opt/oracle/instantclient_19_6 > /etc/ld.so.conf.d/oracle-instantclient.conf"
RUN ldconfig



RUN pip install --ignore-installed -r requirements.txt

EXPOSE 8000
CMD /wait && uvicorn app:app
#CMD ["uvicorn", "app:app"]