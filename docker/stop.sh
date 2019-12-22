
docker stop redis
docker stop tourist-celery
docker stop tourist-fe
docker stop tourist-be
docker stop tourist-nginx

docker rm redis
docker rm tourist-celery
docker rm tourist-fe
docker rm tourist-be
docker rm tourist-nginx
