FROM ubuntu:18.04

# When docker will be implemented branch must be changed to origin/develompent
ARG GIT_BRANCH=origin/feature/docker

RUN apt update
RUN apt-get update
RUN apt install -y git
RUN apt install -y python3.7
RUN apt-get -y install python3-pip

# Copy SSH key for git private repos
COPY .ssh/id_rsa /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa


RUN mkdir /opt/tourist/
RUN mkdir /opt/tourist/fe
RUN mkdir /opt/tourist/be

RUN ssh-keyscan -t rsa gitlab.com >> ~/.ssh/known_hosts

RUN cd /opt/tourist/be && git init && git remote add origin git@gitlab.com:Kv056Python/tourist.git

RUN cd /opt/tourist/be && git fetch && git checkout $GIT_BRANCH

# WORKAROUND. Not possible to install psycopg2 from sources in docker. So installing it as a binary instead
RUN pip3 install psycopg2-binary
RUN sed  -i "/psycopg2/d" /opt/tourist/be/requirements/requirements.txt

RUN pip3 install -r /opt/tourist/be/requirements/requirements.txt

COPY config.py /opt/tourist/be/api/config.py

WORKDIR /opt/tourist/be/api
CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "wsgi:app"]