MQ_SERVICE_NAME = kafka
DOCKER_RUN = docker compose run
DOCKER_EXEC = docker compose exec -it

.PHONY: service_names


build:
	docker compose build

clean:
	docker image prune -f

up: build
	docker compose up --watch

down:
	docker compose down --remove-orphans
	$(MAKE) clean

reload: down up

build-%:
	docker compose build $*

up-%: build-%
	docker compose up $*

restart-%: 
	docker compose restart $*

logs-%:
	docker compose logs $*




docker_shell-%:
	$(DOCKER_EXEC) $* bash

