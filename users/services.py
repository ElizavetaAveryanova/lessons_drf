import stripe

from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_stripe_price(product_id, payment_count):
    """
    Создание цены для курса.
    """
    price = stripe.Price.create(
        unit_amount=int(payment_count) * 100,
        currency="rub",
        product=product_id,
    )
    return price.id


def create_stripe_session(price_id):
    """
    Создание сессии для оплаты.
    """

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session