# Hacker News


#### Developer mode

```
pipenv install --dev

pipenv run python manage.py migrate
```

```
# Download and save the first 30 entries from Hacker News

pipenv run python manage.py download_and_save
```

```
pipenv run python manage.py test

pipenv run python manage.py runserver
``` 


#### Production mode
```
# Create file .env

DJANGO_SECRET_KEY=
DJANGO_ALLOWED_HOSTS=
DJANGO_DB=
DJANGO_DEBUG=False
```

```
docker-compose build

docker-compose run web python manage.py migrate
```

```
docker-compose up -d
```
