FROM python:3.7
RUN pip install fastapi uvicorn
COPY . /app
EXPOSE 7000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]