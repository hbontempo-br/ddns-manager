FROM python:3-alpine

WORKDIR /
ARG PROJECT_NAME=ddns_manager
RUN mkdir /$PROJECT_NAME

# Setup config dir
RUN mkdir /config
ENV YAML /config/config.yml

# Install Requirements
ADD requirements.txt /$PROJECT_NAME
RUN pip3 install -r /$PROJECT_NAME/requirements.txt

# Deploy of code
ADD ddns_manager /$PROJECT_NAME

# Loop execution
CMD python3 -m ddns_manager loop $YAML
