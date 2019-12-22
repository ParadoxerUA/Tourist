docker network create tourist-network;

docker run -d --name postgres --network=tourist-network postgres:latest 
#    ports:
#      - 5432:5432
docker run -d --network=tourist-network --name redis redis:latest
#    ports:
#      - 6379:6379
docker run -d --network=tourist-network tourist-celery:latest
#    depends_on:
#      - server
#      - redis
# Ports?
docker run -d --network=tourist-network --name tourist-fe tourist-fe:latest

docker run -d --network=tourist-network --name tourist-be tourist-be:latest

#DEPENDS ON  tourist-fe, tourist-be
docker run -d -p 7000:80 --network=tourist-network --name tourist-nginx tourist-nginx:latest