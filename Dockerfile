# light weight python
FROM python:3.7-slim

#copy local to container image
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
#Install Dependencies
RUN pip install tensorflow==2.0.0 tensorflow-datasets Flask gunicorn healthcheck 

#Run the flask service on container startip
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 SAGunicorn:app