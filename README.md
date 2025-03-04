# Тестовое задание для Python разработчика
## Описание
Приложение представляет собой простой сервер для создания платежных форм, используя Stripe
Содержит следующие модели:
- Item(поля name, description, price, currency) - модель товара c поддержкой разных валют(в проекте используются USD(по умолчанию) и EUR)
- Discount, Tax(поля name, percentage) - модели для скидок и налогов/сборов, которые применяются к Order
- Order(поля items, tax, discount) - модель заказа с возможностью применения скидок и налогов/сборов к заказу.
Доступны следующие эндпойнты:
- /items/{id}/ - возвращает простую .html страницу с информацией о товаре и кнопкой для покупки, по нажатию на которую происходит создание Stripe.session для выбранного Item
- /items/{id}/buy/ - метод для получения Stripe.session.id для перехода к checkout
- /orders/{id}, /orders/{id}/buy - аналогичные методы для модели Order, которая позволяет объединить несколько Item и добавить к ним Tax и Discount, которые отображаются в Stripe Checkout форме
## Запуск
Приложение можно запускать разными способами:
1. Локально
- создать виртуальное окружение
- установить зависимости
- применить миграции
- запустить приложение
2. С помощью Docker
## Примечания
- так как в приложении реализованы и модель Item, и модель Order, структура эндпойнтов отличается от заданной в ТЗ, для поддержки оплаты и того, и того по отдельности