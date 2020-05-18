# jukebox




## Development

```sh
docker-compose up --build
```
then
```
docker-compose down -v
```
some items differ in development and testing. To run the app in staging /
production mode try

```sh
docker-compose -f docker-compose.prod.yml up --build
```

once the app is running, 

- Vist localhost
