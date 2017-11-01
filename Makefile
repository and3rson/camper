ECS_URL = 193635214029.dkr.ecr.eu-central-1.amazonaws.com/dunai

dev:
	docker build -t camper .
	docker build -t camper-frontend ./frontend
	docker-compose -f ops/dev/docker-compose.yml -p camper up app worker postgres

frontend-dev:
	docker build -t camper-frontend ./frontend
	docker-compose -f ops/dev/docker-compose.yml -p camper up frontend

run:
	docker-compose -f ops/prod/docker-compose -p camper up -d

shell:
	docker exec -it camper_app_1 ./manage.py shell

bash:
	docker exec -it camper_app_1 bash

reinit:
	rm camper/channels/migrations/0001_initial.py camper/things/migrations/0001_initial.py -f
	docker exec -it camper_app_1 ./manage.py makemigrations
	docker exec -it camper_postgres_1 psql -U camper camper -c "DROP SCHEMA public CASCADE"
	docker exec -it camper_postgres_1 psql -U camper camper -c "CREATE SCHEMA public"
	docker exec -it camper_app_1 ./manage.py migrate
	make loaddata

loaddata:
	docker exec -it camper_app_1 ./manage.py loaddata general

upload:
	aws-login-archer
	docker tag camper ${ECS_URL}:camper
	docker tag camper-frontend ${ECS_URL}:camper-frontend
	docker push ${ECS_URL}:camper
	docker push ${ECS_URL}:camper-frontend

livehtml:
	sphinx-autobuild -b html -H 0.0.0.0 -p 9000 docs/source docs/build/html

