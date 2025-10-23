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
	docker compose up $* --watch

restart-%: 
	docker compose restart $*

logs-%:
	docker compose logs $*

migrations: build
	$(DOCKER_RUN) uv run alembic revision --autogenerate
	
migrate:
	$(DOCKER_RUN) uv run alembic upgrade head

auto_migrate: migrations migrate




dockershell-%:
	$(DOCKER_EXEC) $* bash

