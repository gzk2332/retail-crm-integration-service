IMAGE_NAME=retail_crm_integration
CONTAINER_NAME=retail_crm_integration_app

build:
	docker compose build

run:
	docker compose up -d --build

stop:
	docker compose stop

down:
	docker compose down -v

log:
	docker compose logs -f

lint:
	poetry run task format-and-lint

docker-build:
	docker build -t $(IMAGE_NAME) .

docker-run:
	docker run -d \
		--name $(CONTAINER_NAME) \
		--env-file .env \
		-p 8000:8000 \
		$(IMAGE_NAME)

docker-stop:
	docker stop $(CONTAINER_NAME)

docker-rm:
	docker rm $(CONTAINER_NAME)

docker-logs:
	docker logs -f $(CONTAINER_NAME)