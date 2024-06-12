help: ## Show help message
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make <app> [app] [app]...\n\nApps: \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
 : ##

build: ## Build application
	docker compose --env-file .env.local -f docker-compose.yml build --no-cache

run: ## Run API and PostgreSQL
	docker compose --env-file .env.local -f docker-compose.yml up -d

stop: ## Stop API and PostgreSQL
	docker compose stop

migrations-downgrade: ## Migrations downgrade base
	docker exec ksf_test-public-api-cinema-1 bash -c "cd src && alembic downgrade base"

migrations-upgrade: ## Migrations upgrade head
	docker exec ksf_test-public-api-cinema-1 bash -c "cd src && alembic upgrade head"

format: ## Code formating
	docker exec ksf_test-public-api-cinema-1 bash -c "find src -name '*.py' -print0 | xargs -0 isort" || true; \
	docker exec ksf_test-public-api-cinema-1 bash -c "find src -name '*.py' -print0 | xargs -0 autopep8 --in-place" || true; \