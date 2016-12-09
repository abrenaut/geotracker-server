FROM python:3.5.2-slim

MAINTAINER Arthur Brenaut "arthur.brenaut@gmail.com"

ENV PYTHONPATH /app/

# Setup the locales in the Dockerfile
RUN set -x \
    && apt-get update \
    && apt-get install locales -y \
    && locale-gen en_US.UTF-8

COPY requirements /tmp/requirements

# Install Python dependencies
RUN set -x \
    && pip install -U pip setuptools \
    && pip install -r /tmp/requirements/main.txt \
    && find /usr/local -type f -name '*.pyc' -name '*.pyo' -delete \
    && rm -rf ~/.cache/

# Set our work directory to our app directory
WORKDIR /app/
