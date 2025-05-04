# Ansible Role: Docker Install (Ubuntu)

## Установка

```sh
ansible-galaxy role install Alvald1.docker_role
```

## Описание

- Удаляет конфликтующие пакеты и старые файлы Docker.
- Добавляет официальный репозиторий Docker.
- Устанавливает необходимые пакеты Docker.
- Гарантирует запуск и автозапуск сервиса Docker.
- Добавляет пользователя в группу `docker`.

## Переменные

- `prev_packages`: Список пакетов, которые будут удалены перед установкой Docker.
- `prev_files`: Список файлов/директорий, которые будут удалены.
- `docker_apt_repo`: Строка репозитория Docker.
- `required_packages`: Пакеты, необходимые для добавления репозитория.
- `docker_packages`: Список пакетов Docker для установки.

Все переменные определены в `vars/main.yml`.

## Использование

```yaml
- hosts: all
  become: true
  roles:
    - role: docker_role
```

## Требования

- Ubuntu 20.04/22.04
- Ansible >= 2.1

## Тестирование

Пример инвентаря и тестового плейбука находятся в директории `tests/`.

## Лицензия

MIT-0

## Автор

your name
