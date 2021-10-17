### Development

Uses the default Django development server.

1. Rename *.env.dev_* to *.env.dev*.
2. Update the environment variables in the *docker-compose.yml* and *.env.dev* files.
3. Build the images and run the containers:
    ```sh
    docker-compose up -d --build
    ```
4. Make migration:
    ```sh
    docker-compose exec web python manage.py migrate --noinput
    ```
5. Make collectstatic
    ```sh
    docker-compose exec web python manage.py collectstatic --no-input --clear
    ```
6. Create createsuperuser
    ```sh
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
    ```
4. Make migration:
    ```sh
    docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
    ```
5. Make collectstatic
    ```sh
    docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
    ```
6. Create createsuperuser
    ```sh
    docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser --username Sikorskiy --email numbern19@gmail.com
    ```
Test it out at [http://localhost:1337](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.

### Save and Load via .tar 
```sh
    docker save 34fb1b2429d9 > bot.tar
    docker load --input verse_gapminder.tar
```
### TAG and Push to DockerHUB 
```sh
    docker images
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
