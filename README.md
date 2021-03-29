## Второе вступительное задание в Школу бэкенд-разработки Яндекс 2021

Чтобы немного скрасить жизнь людей на самоизоляции, вы решаете открыть
интернет-магазин по доставке конфет "Сласти от всех напастей".
Ваша задача — разработать на python REST API сервис, который позволит нанимать курьеров на работу,
принимать заказы и оптимально распределять заказы между курьерами, попутно считая их рейтинг и заработок.
Сервис необходимо развернуть на предоставленной виртуальной машине на
0.0.0.0:8080.

### Развертывание и запуск

Задание выполнено с помощью веб-фреймворков Django и Django Rest Framework и СУБД PostgreSQL. Для развертывания требуется установленные `git`, `docker` и `docker-compose` 

- Склонировать содержимое репозитория в папку на удаленной машине
- В терминале перейти внутрь полученной директории
- Запустить сборку докер контейнера `docker-compose up -d`
- Провести миграции `docker-compose exec web python manage.py migrate --noinput`
- При наличии проблем с хостом в файле `.env` ввести нужные параметры ALLOWED_HOSTS

Готовое решение будет доступно по адресу `0.0.0.0:8080`

### Тесты

Для запуска тестов введите в терминале команду `docker-compose exec web python manage.py test`
