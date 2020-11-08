FROM python:3.7
RUN pip install fastapi uvicorn agraph-python six
COPY . /app
EXPOSE 7000
CMD ['PWD']
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]