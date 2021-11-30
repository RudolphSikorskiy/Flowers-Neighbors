import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.webhook import DeleteMessage

from telegram_config.loader import storage, bot

log = logging.getLogger(__name__)


class BigBrother(BaseMiddleware):
    # 1
    async def on_pre_process_update(self, update: types.Update, data: dict):
        # log.info('[-------------------------Новый апдейт!-----------------------------]')
        # log.info('1. pre_process_update')
        # log.info('Next process_update')
        # data['middleware_data'] = 'это пойдет в post_process_update'

        if update.message:
            user_id = update.message.from_user.id
            chat_id = update.message.chat.id
            fsm = FSMContext(storage, user_id, chat_id)
            state = await fsm.get_state()
            state_data = await fsm.get_data()
            if '/start' in str(update.message.text) and state:
                log.info(f'update.message.text-> {str(update.message.text)}')
                log.info(f'state {state}')
                log.info(f'state_data {state_data}')
                log.info('[-------------------------Удаление-----------------------------]')
                await bot.delete_message(chat_id, update.message.message_id-1)
                await bot.delete_message(chat_id, update.message.message_id)
                await fsm.finish()
        elif update.callback_query:
            user_id = update.callback_query.from_user.id
        else:
            log.error(f'NOT  message or callback_query')
            return

        banned_users = []
        if user_id in banned_users:
            raise CancelHandler()

    # 2
    async def on_process_update(self, update: types.Update, data: dict):
        # log.info(f'2. process_update, {data=}')
        # log.info(str(update.message.text))
        # log.info('Next pre_process_message')
        pass

    # 3
    async def on_pre_process_message(self, update: types.Message, data: dict):
        # log.info(f'3. pre_process_message, {data=}')
        # log.info(update.text)
        # log.info('Next filters, process_message')
        # data['middlewares'] = 'это пойдет в on_process_message'
        pass

    # 4 Filters

    # 5
    async def on_process_message(self, update: types.Message, data: dict):
        # log.info(f'5. process_message, {data=}')
        # log.info(update.text)
        # log.info('Next Handlers')
        # user_id = update.from_user.id
        # chat_id = update.chat.id
        # if '/reset' in str(update.text):
        #     data['middleware_data'] = 'информация в Handler'
        pass
