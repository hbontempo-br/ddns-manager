FROM python:3-alpine

ARG PROJECT_NAME=dynamic-ip-updater-google-domains

RUN mkdir /$PROJECT_NAME
WORKDIR /$PROJECT_NAME

# Install Requirements
ADD requirements.txt /$PROJECT_NAME
RUN pip3 install -r /$PROJECT_NAME/requirements.txt

#Deploy of code
ADD ddns_manager /$PROJECT_NAME

ENV YAML /config/config.yml
CMD python3 -m ddns_manager loop $YAML
