# Отключение интернета в контейнере

В этом документе описаны различные способы ограничения или отключения доступа к интернету внутри контейнера.

## Структура

- Описание трёх способов ограничения сетевого доступа:
  1. Удаление DNS-сервера
  2. Подмена доменов в `/etc/hosts`
  3. Использование прокси для блокировки трафика

## 1. Удаление DNS-сервера

Удалите содержимое файла `resolv.conf`, чтобы контейнер не мог преобразовывать доменные имена в IP-адреса:

```bash
echo "" > /etc/resolv.conf
```

После выполнения этой команды контейнер не сможет обращаться к DNS-серверу, и разрешение доменных имен работать не будет.

### Пример

```bash
user@ubuntu:~$ sudo docker run -it --rm ubuntu bash
root@a860cb70f655:/# apt update
Get:1 http://archive.ubuntu.com/ubuntu noble InRelease [256 kB]
Get:2 http://security.ubuntu.com/ubuntu noble-security InRelease [126 kB]
Get:3 http://archive.ubuntu.com/ubuntu noble-updates InRelease [126 kB]
0% [Waiting for headers] [2 InRelease 79.7 kB/126 kB 63%]^C
root@a860cb70f655:/# echo "" > /etc/resolv.conf
root@a860cb70f655:/# apt update
Ign:1 http://security.ubuntu.com/ubuntu noble-security InRelease
Ign:2 http://archive.ubuntu.com/ubuntu noble InRelease
Ign:3 http://archive.ubuntu.com/ubuntu noble-updates InRelease
Ign:4 http://archive.ubuntu.com/ubuntu noble-backports InRelease
Ign:1 http://security.ubuntu.com/ubuntu noble-security InRelease
Ign:2 http://archive.ubuntu.com/ubuntu noble InRelease
Ign:3 http://archive.ubuntu.com/ubuntu noble-updates InRelease
Ign:4 http://archive.ubuntu.com/ubuntu noble-backports InRelease
0% [Working]^C
```

---

## 2. Подмена доменов в `/etc/hosts`

Можно "сломать" работу пакетного менеджера (например, `apt update`), подменив доменные имена репозиториев на localhost:

```bash
echo "127.0.0.1 archive.ubuntu.com 127.0.0.1 security.ubuntu.com" > /etc/hosts
```

Теперь обращения к этим доменам будут перенаправляться на локальный адрес, и загрузка пакетов станет невозможной.

### Пример

```bash
user@ubuntu:~$ sudo docker run -it --rm ubuntu bash
root@82d28f6916ab:/# apt update
Get:1 http://archive.ubuntu.com/ubuntu noble InRelease [256 kB]
Get:2 http://security.ubuntu.com/ubuntu noble-security InRelease [126 kB]
Get:3 http://archive.ubuntu.com/ubuntu noble-updates InRelease [126 kB]
Get:4 http://archive.ubuntu.com/ubuntu noble-backports InRelease [126 kB]
0% [Working]^C
root@82d28f6916ab:/# echo "127.0.0.1 archive.ubuntu.com 127.0.0.1 security.ubuntu.com" > /etc/hosts
root@82d28f6916ab:/# apt update
Ign:1 http://archive.ubuntu.com/ubuntu noble InRelease
Ign:2 http://security.ubuntu.com/ubuntu noble-security InRelease
Ign:3 http://archive.ubuntu.com/ubuntu noble-updates InRelease
Ign:4 http://archive.ubuntu.com/ubuntu noble-backports InRelease
Ign:2 http://security.ubuntu.com/ubuntu noble-security InRelease
Ign:1 http://archive.ubuntu.com/ubuntu noble InRelease
Ign:3 http://archive.ubuntu.com/ubuntu noble-updates InRelease
Ign:4 http://archive.ubuntu.com/ubuntu noble-backports InRelease
0% [Working]^C
```

---

## 3. Использование прокси для блокировки трафика

Можно перенаправить весь HTTP/HTTPS-трафик на несуществующий прокси-сервер:

```bash
export http_proxy=http://127.0.0.1:9999
export https_proxy=http://127.0.0.1:9999
```

В результате все сетевые запросы будут уходить на локальный порт, где прокси-сервер не запущен, и интернет станет недоступен.

### Пример

```bash
root@63b34860b295:/# apt update
Get:1 http://security.ubuntu.com/ubuntu noble-security InRelease [126 kB]
Get:2 http://archive.ubuntu.com/ubuntu noble InRelease [256 kB]
Get:3 http://archive.ubuntu.com/ubuntu noble-updates InRelease [126 kB]
Get:4 http://archive.ubuntu.com/ubuntu noble-backports InRelease [126 kB]
0% [Working]^C
root@63b34860b295:/# export http_proxy=http://127.0.0.1:9999
export https_proxy=http://127.0.0.1:9999
root@63b34860b295:/# apt update
Ign:1 http://archive.ubuntu.com/ubuntu noble InRelease
Ign:2 http://archive.ubuntu.com/ubuntu noble-updates InRelease
Ign:3 http://archive.ubuntu.com/ubuntu noble-backports InRelease
Ign:4 http://security.ubuntu.com/ubuntu noble-security InRelease
Ign:1 http://archive.ubuntu.com/ubuntu noble InRelease
Ign:2 http://archive.ubuntu.com/ubuntu noble-updates InRelease
Ign:3 http://archive.ubuntu.com/ubuntu noble-backports InRelease
Ign:4 http://security.ubuntu.com/ubuntu noble-security InRelease
0% [Working]^C
```

---

