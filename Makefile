run:
	docker compose up -d
	
stop:
	docker-compose stop

down:
	docker-compose down --remove-orphans
