FROM python:3.9.1-slim-buster

# File Author / Maintainer
LABEL maintainer="jairocuartas@gmail.com"

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
# set environment variables
# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1


ENV USER=desarrollo
ENV HOME_DIR=/home/desarrollo
ENV PROJECT_DIR=/home/desarrollo/EmployeeData

# Create home user
# Create the user desarrollo.
# Create required folder for project.
# Set user desarrollo the owner for HOME

RUN useradd -m $USER \
    && mkdir $HOME_DIR/static \
    && mkdir $HOME_DIR/logs \
    && mkdir $HOME_DIR/sock

# Copy required files
COPY ./requirements.txt $HOME_DIR

RUN apt-get update \
    && apt-get -y install libpq-dev python3-dev gcc \
    && mkdir -p $HOME_DIR/.cache/pip \
    && pip install --upgrade pip \
    && pip install -r $HOME_DIR/requirements.txt

COPY ./EmployeeData $PROJECT_DIR
RUN chown -R $USER:$USER $HOME_DIR

USER $USER
WORKDIR $PROJECT_DIR