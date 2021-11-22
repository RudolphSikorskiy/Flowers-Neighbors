### Development

Uses the default Django development server.

1. Rename *.env.dev_* to *.env.dev*.
2. Update the environment variables in the *docker-compose.yml* and *.env.dev* files.
3. Build the images and run the containers:
```sh
    docker-compose up -d --build
    docker-compose exec web python manage.py migrate --noinput
    docker-compose exec web python manage.py collectstatic --no-input --clear
    docker-compose exec web python manage.py createsuperuser --username Sikorskiy --email numbern19@gmail.com
```
Test it out at [http://localhost:8000](http://localhost:8000). The "app" folder is mounted into the container and your code changes apply automatically.

### Production
Uses gunicorn + nginx.
1. Rename *.env.prod_* to *.env.prod* and *.env.prod.db_* to *.env.prod.db*. 
2. Update the environment variables.
3. Build the images and run the containers:
```sh
    docker-compose -f docker-compose.prod.yml up -d --build
    docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations --noinput
    docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
    docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
    docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser --username sikorskiy --email numbern19@gmail.com
```
Test it out at [http://localhost:1337](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.

### Save via .tar 
```sh
    docker images
    name_v{models_number_version}.{models_app_version}.{models_fix_version}
    docker save fcb95211b8a8 > web_bot_v2.1.0.tar
```
### Load and Deploy via .tar 
```sh
    docker load --input postgres.tar
    docker load --input flowers-neighbors_bot.tar
    docker load --input flowers-neighbors_web.tar
    docker load --input flowers-neighbors_nginx.tar
    
    docker tag e7a27c1ba758 nginx:v1
    docker tag 4ab1311f73e0 web_bot:v1
    docker tag 700e581c202e postgres:v1
```
### TAG and Push to DockerHUB 
```sh
    docker login
    docker tag IMAGE_ID_bb38976d03cf softhardsolutions/web:version
    docker push softhardsolutions/web
```
### Clear
```sh
    docker-compose down --volumes
    docker system prune --all
    docker system df
```

### dump and refuse database from docker container
```sh
    - Создание дампа 
    - только данные и в виде инсертов
    docker exec -t flowers_db_1 pg_dumpall -a --column-inserts -U sikorskiy > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql
    - Показать созданные базы данных в контейнере
    docker exec flowers-neighbors_db_1 psql -U sikorskiy -l
    - интерактивный psql в контейнере
    docker exec -i flowers-neighbors_db_1 psql -U sikorskiy --dbname=db_dev

    - проброс архива с дампом в контейнер
    docker cp dump_27-10-2021_17_55_24.tar flowers-neighbors_db_1:/var/lib/postgresql/data

    - заливаем дамп через psql
    docker exec flowers-neighbors_db_1 psql -U sikorskiy --dbname=db_dev -f /var/lib/postgresql/data/dump_27-10-2021_17_55_24.sql
    - копируем все медиа файлы
    docker cp flowers_img flowers-neighbors_web_1:/home/app/web/mediafiles/
```

### Temporary environment
```sh
    SET DEBUG=1
    SET SECRET_KEY=my_key
    SET DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    SET SQL_ENGINE=django.db.backends.postgresql
    SET SQL_DATABASE=db_dev
    SET SQL_USER=postgres
    SET SQL_PASSWORD=my_password
    SET SQL_HOST=localhost
    SET SQL_PORT=5432
    SET DATABASE=postgres
    SET BOT_TOKEN=bot_token
    SET ADMIN_ID=my_admin
```
### Show Temporary environment
```sh
    ECHO %DEBUG%
    ECHO %SECRET_KEY%
    ECHO %DJANGO_ALLOWED_HOSTS%
    ECHO %SQL_ENGINE%
    ECHO %SQL_DATABASE%
    ECHO %SQL_USER%
    ECHO %SQL_PASSWORD%
    ECHO %SQL_HOST%
    ECHO %SQL_PORT%
    ECHO %DATABASE%
    ECHO %BOT_TOKEN%
    ECHO %ADMIN_ID% 
```