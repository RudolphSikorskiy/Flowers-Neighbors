from asgiref.sync import sync_to_async
import logging

from django_app.models import Customer, Product, Manager, Order, Store
from decimal import Decimal

log = logging.getLogger(__name__)


@sync_to_async
def add_customer(telegram_id, fullname, username):
    return Customer(full_name=fullname,
                    username=username,
                    telegram_id=telegram_id).save()


@sync_to_async
def select_all_customers():
    customers = Customer.objects.all()
    return customers


@sync_to_async
def select_customer(telegram_id):
    customer = Customer.objects.get(telegram_id=telegram_id)
    return dict(customer_id=customer.id,
                full_name=customer.full_name,
                username=customer.username,
                phone=customer.phone,
                telegram_id=customer.telegram_id,
                email=customer.email,
                )


@sync_to_async
def select_all_managers():
    managers = Manager.objects.all()
    lst = []
    for mg in managers:
        lst.append(dict(
            id=mg.id,
            full_name=mg.full_name,
            username=mg.username,
            phone=mg.phone,
            telegram_id=mg.telegram_id,
            email=mg.email,
        )
        )

    return lst


@sync_to_async
def select_products(price_from, price_to):
    log.info(f'{price_from} {price_to}')
    lst = []
    try:
        product = Product.objects.filter(price__range=[Decimal(price_from), Decimal(price_to)])
    except Exception as err:
        log.info(f'ERROR --------> {err}')
        return None
    else:
        for pr in product:
            lst.append(dict(id=pr.id,
                            name=pr.name,
                            photo=pr.photo,
                            price=pr.price,
                            description=pr.description,
                            ))
        return lst


@sync_to_async
def add_order(customer_id, product_id, telegram_id, shipping_address,
              phone_number,
              email,
              ):
    return Order(customer_id=Customer.objects.get(telegram_id=telegram_id),
                 product_id=Product.objects.get(id=product_id),
                 shipping_address=shipping_address,
                 phone_number=phone_number,
                 email=email).save()


@sync_to_async
def select_all_cities():
    cities = Store.objects.order_by().values('city').distinct()
    return list(cities)


@sync_to_async
def select_all_stores(city):

    stores = Store.objects.values('id', 'name', 'city', 'street', 'house').filter(city=city)
    log.warning(list(stores))
    return list(stores)

# 1. You should import models from django app
# from makret.models import Customer
#
# 2. Use @sync_to_async to CRUD
# @sync_to_async
# def add_customer(telegram_id, fullname, username):
#     return Customer(full_name=fullname,
#                     username=username,
#                     telegram_id=telegram_id).save()
