all:
	-make network
	make hadoop
	make spark
	make services
	make web
	make kafka

network:
	docker network create scac-network-2019

# TODO: Setup properly traefik
# traefik:
# add --constraint node.hostname==frontend.com to deploy on particular server
# docker service create --name traefik --publish 80:80 --publish 8080:8080 --mount type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock --network workbench traefik --docker --docker.swarmmode --docker.domain=local.host --docker.watch --web --logLevel=DEBUG

hadoop:
	docker-compose -f docker-compose-hadoop.yml up -d

spark:
	docker-compose -f docker-compose-spark.yml up -d

services:
	docker-compose -f docker-compose-services.yml up -d

kafka:
	docker-compose -f docker-compose-kafka.yml up -d

web:
	docker-compose -f docker-compose-web.yml up -d

# Stop all the services

stop:
	docker-compose -f docker-compose-hadoop.yml down
	docker-compose -f docker-compose-spark.yml down
	docker-compose -f docker-compose-services.yml down
	docker-compose -f docker-compose-web.yml down
	docker-compose -f docker-compose-kafka.yml down
# Delete all the services volumes and networks
#make stop && 	# && docker network rm scac-network-2019 && docker volumes rm datanode namenode

clean:
	-make stop
	-docker rm $(docker ps -aq)
	-docker network rm scac-network-2019
	-docker volume rm datanode namenode


sysprune:
	-docker system prune --volumes -f