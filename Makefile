dev:
	docker build -t camper .
	#docker build -t camper-frontend ./frontend
	docker-compose up

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

