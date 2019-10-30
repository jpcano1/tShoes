# Base Image
FROM python:3.6

ARG FLASK_ENV

ENV WEBAPP_DIR /auth_app

# create and set working directory
RUN mkdir $WEBAPP_DIR
WORKDIR $WEBAPP_DIR

# Add Current directory to working directory
ADD tShoes-main $WEBAPP_DIR
ADD requirements/base.txt $WEBAPP_DIR
ADD requirements/$FLASK_ENV.txt $WEBAPP_DIR

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

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
RUN pip3 install -r $FLASK_ENV.txt