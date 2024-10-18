from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from tg_routers.admin.replics import *
from tg_routers.admin import keyboards
import db
from tg_routers.admin import models
import config
import traceback
from integrations import vk_send

router = Router()
bot = Bot(token=config.tg_token)

@router.message(models.editStates.edit_answer, F.text)
async def edit_answerFunc(message: Message, state: FSMContext):
    data = models.editor_answers_data[message.chat.id]
    text, markup = await replic_edit_answer(data["first_text"], message.text, data['user_id'])
    await message.answer(text, reply_markup=markup)
    await state.clear()


@router.message(models.editStates.edit, F.text)
async def editFunc(message: Message, state: FSMContext):
    try:
        info_data = (await db.info.get_informations())[models.editor_data[message.chat.id]]
        new_info = message.text.split(sep='++')
        print(new_info)
        info, description = new_info[0], new_info[1]
        await db.info.update_info(info_data["id"], info)
        await db.info.update_description(info_data["id"], description)
        text, markup = await replic_edit_information(models.editor_data[message.chat.id])
        await message.answer(text, reply_markup=markup)
        await state.clear()
    except Exception as e:
        traceback.print_exc()
        print(e)
        await message.answer(replic_edit_error)

@router.message(F.text == '/admin')
async def start_command(message: Message):
    await message.answer(replic_admin_menu, reply_markup=keyboards.admin_menu)

@router.callback_query(F.data.startswith('admin'))
async def callback(call, state: FSMContext):
    user_id = call.message.chat.id
    calls = str(call.data).split(sep='.')
    l1 = calls[0]
    l2 = calls[1]
    l3 = calls[2]
    if l2 == 'menu':
        if l3 == 'main':
            await bot.edit_message_text(text=replic_admin_menu, chat_id=user_id, message_id=call.message.message_id, reply_markup=keyboards.admin_menu)
    elif l2 == 'editor':
        if l3 == 'menu':
            text, markup = await replic_get_informations()
            await bot.edit_message_text(text=text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        elif l3 == 'add':
            await db.info.add_information()
            array_id = len(await db.info.get_informations()) - 1
            text, markup = await replic_edit_information(array_id)
            await bot.edit_message_text(text=text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        else:
            array_id = int(l3)
            text, markup = await replic_edit_information(array_id)
            await bot.edit_message_text(text=text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
    elif l2 == 'edit':
        models.editor_data[user_id] = int(l3)
        await bot.edit_message_text(text=replic_edit_info, chat_id=user_id, message_id=call.message.message_id)
        await state.set_state(models.editStates.edit)
    elif l2 == 'delete':
        info_data = (await db.info.get_informations())[int(l3)]
        await db.info.delete_info(info_data["id"])
        array_id = int(l3) - 1
        if array_id == -1:
            text, markup = await replic_get_informations()
            await bot.edit_message_text(text=text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
        else:
            text, markup = await replic_edit_information(array_id)
            await bot.edit_message_text(text=text, chat_id=user_id, message_id=call.message.message_id, reply_markup=markup)
    elif l2 == 'eq':
        text = call.message.text
        text_splited = text.split(sep="Вариант ответа:")
        first_text = text_splited[0]
        models.editor_answers_data[user_id] = {'first_text': first_text, "user_id": int(l3)}
        await state.set_state(models.editStates.edit_answer)
        await bot.edit_message_text(text=replic_edit_answer_phrase, chat_id=user_id, message_id=call.message.message_id)
    elif l2 == 'aq':
        text = call.message.text
        text_splited = text.split(sep="Вариант ответа:")
        answer = text_splited[1]
        vk_send.send_message(int(l3), answer)
        await bot.edit_message_text(text=call.message.text + "\n✔️ Отправлено", chat_id=user_id, message_id=call.message.message_id)

