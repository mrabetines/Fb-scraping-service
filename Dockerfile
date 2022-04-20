FROM python:3.9.10

#RUN mkdir /app
#WORKDIR /app
#RUN cd /app

WORKDIR /fastapi

COPY ./requirements.txt /fastapi/requirements.txt

RUN pip install -r /fastapi/requirements.txt

COPY ./app /fastapi/app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]