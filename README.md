# Структура

Для упрощения все микросервисы в одном проекте.
Единственная зависимость между ними - это общий redis контейнер

-   [Orders](./orders/) - микросервис создания заказов

## POST

[/orders/]

[Producer logic file](./orders/src/application/orders/services.py)

-   Принимает информацию о заказе, сразу (не совсем) отдаёт ответ с id заказа
-   Добавляет заказ и его статус в бд (redis для простоты)

-   Сериализует данные о заказе через confluent schema registry

-   Отправляет в kafka topic. Exponential retry через tenacity (Четкое понимание времени ретраев отсутствует, <br> поэтому на глаз)
    Retry срабатывает при BufferError и всех "retriable" исключениях. Возможно не учел еще важные кейсы.

-   Логирование через logger и в redis stream.
    В delivery callback'е логирование и обновление статуса через run_coroutine_threadsafe т.к. асинхронный редис.

## GET

[/orders/{order_id}]

-   Возвращает текущий статус заказа <br>
    Изначально pending -> после отправки сообщения в топик либо accepted либо failed

-   Возвращает 404 если неверный order_id
