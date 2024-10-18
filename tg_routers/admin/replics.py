import db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

replic_admin_menu = 'Меню администратора'
replic_edit_info = "Введите новую информацию и описание в таком формате:\nИнформация ++ Описание"
replic_edit_error = 'Ошибка! Введите информацию в правильном формате'
replic_edit_answer_phrase = 'Введите ответ'

async def replic_get_informations():
    data = await db.info.get_informations()
    keyboard = []
    for i in range(len(data)):
        keyboard.append([InlineKeyboardButton(text=f'{i + 1}', callback_data=f'admin.editor.{i}')])
    keyboard.append([InlineKeyboardButton(text='➕ Добавить', callback_data='admin.editor.add')])
    keyboard.append([InlineKeyboardButton(text='⬅️ Назад', callback_data='admin.menu.main')])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = 'Выберите информацию для редактирования'
    return text, markup

async def replic_edit_information(array_id):
    data = await db.info.get_informations()
    keyboard = []
    item_data = data[array_id]
    btn_edit = InlineKeyboardButton(text='✏️ Редактировать', callback_data=f'admin.edit.{array_id}')
    btn_delete = InlineKeyboardButton(text='❌ Удалить', callback_data=f'admin.delete.{array_id}')
    btn_back = InlineKeyboardButton(text='⬅️', callback_data=f'admin.editor.{array_id - 1}')
    btn_next = InlineKeyboardButton(text='➡️', callback_data=f'admin.editor.{array_id + 1}')
    btn_add = InlineKeyboardButton(text='➕ Добавить', callback_data='admin.editor.add')
    btn_to_menu = InlineKeyboardButton(text='️🚪 Назад', callback_data='admin.editor.menu')
    if array_id == 0 and len(data) > 1:
        keyboard.append([btn_edit, btn_next])
    elif array_id == 0 and len(data) == 1:
        keyboard.append([btn_edit, btn_add])
    elif array_id == len(data) - 1:
        keyboard.append([btn_back, btn_edit, btn_add])
    else:
        keyboard.append([btn_back, btn_edit, btn_next])
    keyboard.append([btn_delete])
    keyboard.append([btn_to_menu])
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    text = f'Информация {array_id}\n{item_data["info"]}\n\n{item_data["description"]}'
    return text, markup

async def replic_edit_answer(first_text, new_text, user_id):
    text = first_text + "Вариант ответа:\n" + new_text
    btn_edit = InlineKeyboardButton(text='✏️ Редактировать', callback_data=f'admin.eq.{user_id}')
    btn_answer = InlineKeyboardButton(text='⬅️ Ответить', callback_data=f'admin.aq.{user_id}')
    markup = InlineKeyboardMarkup(inline_keyboard=[[btn_edit], [btn_answer]])
    return text, markup

