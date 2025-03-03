import uuid
from yookassa import Payment
from yookassa import Configuration
from asgiref.sync import sync_to_async
import os

# Конфигурация
Configuration.account_id = os.getenv("YOOKASSA_SHOP_ID")
Configuration.secret_key = os.getenv("YOOKASSA_SECRET_KEY")

@sync_to_async
def create_payment(user_id, amount, return_url="https://t.me/AnyTechShopBot"):
    """Создает платеж и возвращает ссылку на оплату"""
    payment = Payment.create({
        "amount": {
            "value": str(amount),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url
        },
        "capture": True,
        "description": f"Оплата заказа для пользователя {user_id}",
        "metadata": {"user_id": user_id}
    }, idempotency_key=str(uuid.uuid4()))

    return payment.id, payment.confirmation.confirmation_url

@sync_to_async
def check_payment_status(payment_id):
    """Проверяет статус платежа"""
    payment = Payment.find_one(payment_id)
    return payment.status