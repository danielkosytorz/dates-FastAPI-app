### Variables ###

containers-tool = docker-compose
dev-dockerfile = -f docker-compose.yml
backend = backend
tortoise_settings = src.settings.settings.TORTOISE_ORM

### Development ###

.PHONY: build
build:
	$(containers-tool) $(dev-dockerfile) build
	make dev

.PHONY: rebuild
rebuild:
	$(containers-tool) $(dev-dockerfile) build --no-cache
	make dev

.PHONY: dev
dev:
	$(containers-tool) $(dev-dockerfile) up --remove-orphans

.PHONY: init-migration
init-migration:
	$(containers-tool) $(dev-dockerfile) exec $(backend) aerich init -t $(tortoise_settings)
.PHONY: init-db
init-db:
	$(containers-tool) $(dev-dockerfile) exec $(backend) aerich init-db

.PHONY: migrate
migrate:
	$(containers-tool) $(dev-dockerfile) exec $(backend) aerich migrate

.PHONY: upgrade
upgrade:
	$(containers-tool) $(dev-dockerfile) exec $(backend) aerich upgrade

.PHONY: downgrade
downgrade:
	$(containers-tool) $(dev-dockerfile) exec $(backend) aerich downgrade