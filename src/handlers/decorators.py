from aiogram.types import Message
from src.methods.database.users_manager import UsersDatabase
from src.misc import bot_id,PASSWORD
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


def new_user_handler(function):
    async def _new_user_handler(message: Message, state: FSMContext, **kwargs):
        
        user_id = message.chat.id
        user = await UsersDatabase.get_user(user_id)
        if user == -1:
            await UsersDatabase.create_user(user_id)
            await message.answer('Password?')
            await state.set_state(PassStates.pass_ask)
            if user_id == int(bot_id):
                
                await UsersDatabase.set_value(user_id,'is_admin',1)
                #назначение бота админом для кнопок в админке(костыль, вроде пофикшен)
        user = await UsersDatabase.get_user(user_id)
        if user[2] == 0:
                
                if message.text == PASSWORD:
                    await UsersDatabase.set_value(user_id,'is_admin',1)
                    await message.answer("welcome /start")
                    await state.clear()

                else:
                    await message.answer('try more..')
                    await state.set_state(PassStates.pass_ask)
                    return


        return await function(message, state, **kwargs)

    return _new_user_handler

class PassStates(StatesGroup):
    pass_ask = State()
