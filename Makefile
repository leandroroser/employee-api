start:
	docker-compose up --build

stop:
	docker-compose down

test:
	docker-compose exec api python -m pytest

clean:
	docker-compose down
	docker-compose rm -f
