# Kubernetes-манифесты и Helm-чарт для echo-server

## Описание

В этой директории представлены манифесты и Helm-чарт для деплоя приложения **echo-server** в Kubernetes-кластере. Приложение реализует три эндпоинта:
- `/host` — возвращает имя хоста (hostname контейнера)
- `/ip` — возвращает IP-адрес хоста
- `/author` — возвращает имя автора из переменной окружения `AUTHOR`

Также реализованы readiness- и liveness-пробы, проброс переменной окружения, использование приватного Docker Registry и опциональный Ingress.

---

## Структура

- `echo-server.yaml` — raw-манифесты для Namespace, Deployment, Service и Ingress.
- `echo-server-chart/` — Helm-чарт для деплоя приложения с параметризацией.
- `playbook.yml` — Ansible playbook для автоматизированного деплоя Helm-чарта и создания необходимых секретов.
- `vault.yml` — секреты для доступа к приватному Docker Registry.
- `inventory.ini`, `ansible.cfg` — пример инвентаря и конфигурации Ansible.

---

## Переменные окружения

- `AUTHOR` — имя автора, пробрасывается в контейнер через переменную окружения.

---

## Readiness и Liveness пробы

В Deployment реализованы следующие пробы:
- **Readiness:** `/health/ready` — возвращает 200, если переменная `AUTHOR` задана.
- **Liveness:** `/health/live` — возвращает 200, если контейнер может получить свой IP.

---

## Использование приватного Docker Registry

Для доступа к приватному реестру используется секрет типа `kubernetes.io/dockerconfigjson` с именем `regcred`. Он создаётся автоматически через Ansible playbook (`playbook.yml`) на основе переменных из `vault.yml`.

---

## Деплой через Helm-чарт

### 1. Создание секрета для приватного реестра

Если не используете Ansible, создайте секрет вручную:

```bash
kubectl create namespace echo-server
kubectl create secret docker-registry regcred \
  --docker-username=<username> \
  --docker-password=<password> \
  --docker-email=<email> \
  --namespace=echo-server
```

### 2. Установка Helm-чарта

```bash
helm install echo-server ./echo-server-chart -n echo-server --set env.AUTHOR="Ваше Имя"
```

---

## Деплой через raw-манифесты

```bash
kubectl apply -f echo-server.yaml
```

---

## Проверка работы приложения

### Получить список Pod'ов

```bash
kubectl get pods -n echo-server -o wide
```

### Проверить доступность сервисов

```bash
kubectl port-forward svc/echo-server 8000:8000 -n echo-server
curl http://localhost:8000/host
curl http://localhost:8000/ip
curl http://localhost:8000/author
```

### Проверить работу readiness/liveness

```bash
curl http://localhost:8000/health/ready
curl http://localhost:8000/health/live
```

---

## Проверка балансировки через Ingress

Если настроен Ingress и DNS/hosts для `echo-server.local` указывает на VIP (например, 192.168.62.200):

```bash
for i in {1..100}; do
  curl -s -H "Host: echo-server.local" http://192.168.62.200/ip
done | grep -oP '"ip":"\K[0-9.]+' | sort | uniq -c
```

---

## Использование Ansible для деплоя

**Перед запуском playbook необходимо установить роль:**

```bash
ansible-galaxy role install Alvald1.k8s_cluster_role
```

1. Заполните `vault.yml` с данными для приватного реестра.
2. Запустите playbook:
  ```bash
  ansible-playbook -i inventory.ini playbook.yml --ask-vault-pass
  ```

---

## Примечания

- Все параметры можно переопределять через `values.yaml` Helm-чарта.
- Для доступа к приватному реестру используйте корректные креденшелы.

---

## Авторы

- alvald1
