FROM python:3.7
WORKDIR /opt/app
RUN pip install pip install fastapi uvicorn agraph-python six faker
#COPY . /app
COPY . .
ENV WAIT_VERSION 2.7.3
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait
EXPOSE 7000
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]
#CMD ["ls", "/opt/app"] 

CMD /wait && uvicorn app:app --host 0.0.0.0 --port 7000 --reload
