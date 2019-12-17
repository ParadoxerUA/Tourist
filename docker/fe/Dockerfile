FROM node:12.13.1

RUN apt update
RUN apt-get update
RUN apt install -y git

# Copy SSH key for git private repos
COPY .ssh/id_rsa /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa

RUN mkdir /opt/tourist/
RUN mkdir /opt/tourist/fe

RUN ssh-keyscan -t rsa gitlab.com >> ~/.ssh/known_hosts

WORKDIR /opt/tourist/fe
RUN git init && git remote add origin git@gitlab.com:Kv056Python/touristfe.git
RUN git fetch
RUN git checkout origin/development

RUN npm install
RUN npm install -g @angular/cli@8.3.8

CMD ["ng"  , "serve", "--host", "0.0.0.0"]