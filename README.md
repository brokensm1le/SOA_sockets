# SOA_sockets

Ссылка на DockerHub: https://hub.docker.com/repository/docker/adakimov/sockets

## Тест

Чтобы протестировать приложение :

### Шаг 1

Скачать себе Docker образ серверной части на компьютер.

```
docker push adakimov/sockets:tagname
```

Скачать файл `client.py`.

### Шаг 2

Запускаем сначала server:

```
docker run -it adakimov/sockets
```

Далее заупскаем 2-ух client-ов из разных консолей:

```
pip3 install pyaudio
pip3 install opencv-python

python client.py 
```
Вводим ip сервера.

## Интерфейс


### Mute

Чтобы выключить микрофон, нажмите `p`.

### Unmute

Чтобы включить микрофон, нажмите `c`.

### Exit 
Чтобы выйти, нажмите `q`.



