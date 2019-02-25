all:
	network && hadoop && spark && services

network:
	docker network create scac-network-2019

# TODO: Setup properly traefik
# traefik:
	# add --constraint node.hostname==frontend.com to deploy on particular server
	#docker service create --name traefik --publish 80:80 --publish 8080:8080 --mount type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock --network workbench traefik --docker --docker.swarmmode --docker.domain=local.host --docker.watch --web --logLevel=DEBUG

hadoop:
	docker-compose-hadoop.yml hadoop up -d

spark:
	docker-compose-spark.yml up -d

services:
	docker-compose-services.yml services up -d

# Stop all the services

stop:
	docker-compose-hadoop.yml down && docker-compose-spark.yml down && docker-compose-services.yml down

# Delete all the services volumes and networks

clean:
	stop && docker rm $(docker ps -aq) && docker network rm scac-network-2019 && docker volumes rm datanode namenode


