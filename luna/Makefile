PYTHON := python
ifeq ($(shell command -v python3 2> /dev/null),)
	PYTHON := python
else
	PYTHON := python3
endif

runserver:
	$(PYTHON) manage.py runserver

makemigrations:
	$(PYTHON) manage.py makemigrations

migrate:
	$(PYTHON) manage.py migrate

createsuperuser:
	$(PYTHON) manage.py createsuperuser

shell:
	$(PYTHON) manage.py shell