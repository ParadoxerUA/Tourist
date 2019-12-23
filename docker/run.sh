#docker network create tourist-network

docker run -d --network=tourist-network --name redis redis:latest
docker run -d --network=tourist-network --name tourist-celery tourist-celery:latest

docker run -d --network=tourist-network --name tourist-fe tourist-fe:latest
docker run -d --network=tourist-network --name tourist-be --add-host=host.docker.internal:172.17.0.1 tourist-be:latest
#DEPENDS ON  tourist-fe, tourist-be
docker run -d -p 7000:80 --network=tourist-network --name tourist-nginx tourist-nginx:latest