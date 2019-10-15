# Base Image
FROM python:3.6

ARG DJANGO_ENV

ENV WEBAPP_DIR /app

# create and set working directory
RUN mkdir $WEBAPP_DIR
WORKDIR $WEBAPP_DIR

# Add current directory code to working directory
ADD . $WEBAPP_DIR
ADD requirements/base.txt $WEBAPP_DIR
ADD requirements/$DJANGO_ENV.txt $WEBAPP_DIR

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# set project environment variables
# grab these via Python's os.environ
# these are 100% optional here
#ENV PORT=8888

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        apt-utils \
        git \
        && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*

# install environment dependencies
RUN pip3 install --upgrade pip

# Install project dependencies
RUN pip3 install -r $DJANGO_ENV.txt

#RUN python3 manage.py makemigrations
#RUN python3 manage.py migrate