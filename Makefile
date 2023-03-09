install:
	docker-compose up -d --build

test:
	docker-compose exec api python -m pytest

psql:
	docker-compose exec postgresql_db /bin/bash -c "psql -U docker -d docker"

clean:
	docker-compose down
	docker-compose rm -f
	docker rmi -f api db 
