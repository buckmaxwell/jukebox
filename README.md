# jukebox

![](https://github.com/buckmaxwell/jukebox/workflows/build/badge.svg)


## Development

```sh
docker-compose -f docker-compose.dev.yml up --build
```
then
```
docker-compose -f docker-compose.dev.yml down -v
```
some items differ in development and testing. To run the app in staging /
production mode try

```sh
docker-compose -f docker-compose.prod.yml up --build
```

once the app is running, 

- Vist localhost, you're not in a room yet so you'll see
![not_in_room](https://user-images.githubusercontent.com/6210452/82165593-a7b4c080-9883-11ea-8fc5-43c3e310fd52.png)

- To get the code, visit /host
![host_page](https://user-images.githubusercontent.com/6210452/82165583-9c619500-9883-11ea-96be-0fcf8f6c2e8c.png)

- After sign in you should see a search page. You'll be able to search for and then queue songs
![song_search](https://user-images.githubusercontent.com/6210452/82165591-a4b9d000-9883-11ea-95f8-41225ec92dfc.png)


## Troubleshooting
- Visit localhost:15672 and sign in as guest / guest to observe the queues
![queues](https://user-images.githubusercontent.com/6210452/82165589-a2f00c80-9883-11ea-9cc5-d0748320027b.png)
