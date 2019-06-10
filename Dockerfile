FROM python:3-alpine

ARG PROJECT_NAME=dynamic-ip-updater-google-domains

RUN mkdir /$PROJECT_NAME
WORKDIR /$PROJECT_NAME

# Install Requirements
ADD requirements.txt /$PROJECT_NAME
RUN pip3 install -r /$PROJECT_NAME/requirements.txt

#Deploy of code
ADD . /$PROJECT_NAME

CMD python3 ./app.py
