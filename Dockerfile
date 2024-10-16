FROM python:3.9.5

ENV PYTHONPATH /usr/src/app

RUN mkdir -p $PYTHONPATH

# where the code lives
WORKDIR $PYTHONPATH

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN apt-get update \
#    && apt-get -y install netcat gcc postgresql \
#    && apt-get clean
# Install apt packages
#RUN apt-get update && apt-get install --no-install-recommends -y \
#  # model translatios \
#  gettext \
#  # dependencies for building Python packages
#  build-essential \
#  # psycopg2 dependencies
#  libpq-dev \
#  binutils libproj-dev gdal-bin python-gdal peython3-gdal \

RUN apt-get update && apt-get install -y  binutils libproj-dev gdal-bin python3-gdal libheif-examples \
    # model translatios \
    gettext

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

# install app
COPY . .

