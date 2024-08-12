PROJECT_NAME=quix-n-redis-template
service=consumer
worker=example.app
partitions=4

localup:
	docker compose -f docker-compose.local.yml up --remove-orphans
localbuild:
	docker compose -f docker-compose.local.yml build --no-cache
developup:
	docker compose -f docker-compose.develop.yml up --remove-orphans
developbuild:
	docker compose -f docker-compose.develop.yml build --no-cache
test:
	docker exec -it $(PROJECT_NAME)-consumer pytest .
flake8:
	docker exec -it $(PROJECT_NAME)-consumer flake8 .
mypy:
	docker exec -it $(PROJECT_NAME)-consumer mypy .
black:
	docker exec -it $(PROJECT_NAME)-consumer black .
isort:
	docker exec -it $(PROJECT_NAME)-consumer isort . --profile black --filter-files

# Kafka related
create-topic:
	docker-compose exec kafka kafka-topics --zookeeper zookeeper:32181 \
	--create ${topic-name} --if-not-exists \
	--partitions ${partitions} --topic ${topic-name} --replication-factor 1
create-page-view-topic:
	@$(MAKE) create-topic topic-name=page_views
list-topics:
	docker-compose exec kafka kafka-topics --list --zookeeper zookeeper:32181
