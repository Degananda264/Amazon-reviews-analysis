FROM python:3.7

RUN pip install virtualenv
ENV VIRTUAL_ENV=/venv
RUN virtualenv venv -p python3
ENV PATH="VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
ADD . /app
#Install Dependencies
RUN pip install tensorflow==2.0.0 tensorflow-datasets Flask gunicorn healthcheck 

# Expose port 
ENV PORT 8080

# Run the application:
CMD ["gunicorn", "app:app", "--config=config.py"]