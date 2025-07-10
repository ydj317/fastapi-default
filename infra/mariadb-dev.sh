docker run -d \
  --name mariadb-dev \
  -e MYSQL_ROOT_PASSWORD=myrootpass \
  -e MYSQL_DATABASE=devdb \
  -e MYSQL_USER=devuser \
  -e MYSQL_PASSWORD=devpass \
  -p 3306:3306 \
  mariadb:10.3.39