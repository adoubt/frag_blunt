import asyncio
from aiogram import types
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from src.handlers.decorators import new_user_handler, FSMContext,PassStates
import requests,aiofiles
import  os
from bs4 import BeautifulSoup
import re,random
from src.keyboards import user_keyboards
from src.methods.database.db_manager import DbManager
from src.methods.database.users_manager import UsersDatabase
router =  Router()
from src.misc import bot,bot_id,PASSWORD

help_msg = '''/ava {n} Available
/una {n} Unavailable
/tak {n} Taken
n = 10 by default
/db  Download Base
/del {username}
/del all
/start
/help
'''

@router.message(Command("start"))
@new_user_handler
async def start_handler(message: Message, state: FSMContext,is_clb=False,**kwargs):
    await message.answer(help_msg)

@router.message(Command("ava"))
@new_user_handler
async def avat_handler(message: Message, state = FSMContext,is_clb=False,**kwargs):
    arg = message.text.split()
    parametr = arg[1] if len(arg) > 1 else 10
    rows = await DbManager.get_latest_records(parametr,'Available') 
    response_text = "<b>Available:</b>\n\n"   
    for row in rows:
        response_text += f"@{row[1]} {row[3][:10]}\n"
    await message.answer(text =response_text, parse_mode = 'HTML')

@router.message(Command("una"))
@new_user_handler
async def una_handler(message: Message,state = FSMContext, is_clb=False,**kwargs):
    arg = message.text.split()
    parametr = arg[1] if len(arg) > 1 else 10
    rows = await DbManager.get_latest_records(parametr,'Unavailable') 
    response_text = "<b>Unavailable:</b>\n\n"   
    for row in rows:
        response_text += f"@{row[1]} {row[3][:10]}\n"
    await message.answer(text =response_text, parse_mode = 'HTML')

@router.message(Command("tak"))
@new_user_handler
async def tak_handler(message: Message, state = FSMContext,is_clb=False,**kwargs):
    arg = message.text.split()
    parametr = arg[1] if len(arg) > 1 else 10
    rows = await DbManager.get_latest_records(parametr,'Taken') 
    response_text = "<b>Taken:</b>\n\n"   
    for row in rows:
        response_text += f"@{row[1]} {row[3][:10]}\n"
    await message.answer(text =response_text, parse_mode = 'HTML')

@router.message(Command("del"))
@new_user_handler
async def del_handler(message: Message,  state = FSMContext,is_clb=False,**kwargs):
    arg = message.text.split()
    if len(arg) <= 1:
       await message.answer('Missing username (/del durov)') 
       return
    parametr = arg[1]
    if parametr == 'all': await DbManager.del_usernames() 
    else: await DbManager.del_username(parametr) 
    await message.answer('Deleted')


@router.message(Command("db"))
@new_user_handler
async def db_handler(message: types.Message, state = FSMContext, is_clb=False, **kwargs):
    rows, columns = await DbManager.get_all_records()
    output_file = 'usernames.csv'
    # Открываем файл асинхронно в текстовом режиме 
    async with aiofiles.open(output_file, mode='w', newline='', encoding='utf-8') as file:
        # Записываем заголовки 
        await file.write(','.join(columns) + '\n') 
        for row in rows: await file.write(','.join(map(str, row)) + '\n')
    agenda = FSInputFile("usernames.csv", filename="usernames.csv")
    # Отправляем файл пользователю
    await message.answer_document(document=agenda)
    # Удаляем файл после отправки
    if os.path.exists(output_file):
        os.remove(output_file)

@router.message(Command("help"))
@new_user_handler
async def send_help(message: Message, state = FSMContext, is_clb=False,**kwargs):
    await message.answer(help_msg)


# Обработчик текстовых сообщений
@router.message(F.text and F.text!=f'{PASSWORD}'and F.text!='start')
@new_user_handler
async def check_username(message: Message, state = FSMContext,**kwargs):
    if not message.text:
        await message.answer()
        return
    message_lines = message.text.splitlines()
    text = f'<b>Username</b> <b>Status</b> <b>Fragment</b>\n\n'
    msg = await message.answer(text,parse_mode='HTML')
    count = 0
    for username in message_lines:
        if not validate_string(username):
            await message.answer(f'{username} - некоректный ввод')
            continue
        result = await check_username(username)
        
        if not result:
            continue
        
        
        text += f'@{username} | <b>{result}</b> : <a href="https://fragment.com/username/{username}">link</a>\n'
        await msg.edit_text(text=text,parse_mode='HTML',disable_web_page_preview=True)
        await DbManager.create_username(username,result)
        count+=1
        await asyncio.sleep(random.uniform(0, 2))
    errors = len(message_lines) - count
    if errors>0:
        
        text+=f'\nErrors: {errors}'
        await msg.edit_text(text=text,parse_mode='HTML',disable_web_page_preview=True)


async def check_username(username) -> str:
    url=f'https://fragment.com/?query={username}'
    r = requests.post(url)
    if r.status_code != 200:
         return None
    soup = BeautifulSoup(r.text, 'html.parser')
    # Ищем тег <a>
    # Ищем первый div с классом, начинающимся на 'tm-status'
    status_div = soup.find('div', class_=re.compile(r'tm-status-'))

    # Извлекаем текст, если элемент найден
    status_text = status_div.get_text(strip=True) if status_div else None
    print(status_text)  # Output: Available
    return status_text
   
def validate_string(s: str) -> bool:
    try: 
        perviy = s[0]
        suka = int(perviy)
        return False
    except:

        return True if ' ' not in s and re.match('^[A-Za-z0-9_]+$', s) else False
    

@router.message(PassStates.pass_ask)
async def pass_ask_handler(message: types.Message, state: FSMContext, **kwargs):
    user_id = message.chat.id
    if message.text == PASSWORD:
        await UsersDatabase.set_value(user_id,'is_admin',1)
        await message.answer("welcome /start")
        await state.clear()

    else:
        await message.answer("try more..")
        await state.set_state(PassStates.pass_ask)