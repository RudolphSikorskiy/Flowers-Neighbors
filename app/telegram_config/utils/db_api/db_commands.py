from asgiref.sync import sync_to_async
import logging

log = logging.getLogger(__name__)

# 1. You should import models from django app
# from makret.models import Customer
#
# 2. Use @sync_to_async to CRUD
# @sync_to_async
# def add_customer(telegram_id, fullname, username):
#     return Customer(full_name=fullname,
#                     username=username,
#                     telegram_id=telegram_id).save()
