import aiohttp
from config import proxyapi_key, gpt_users_prompt, vk_token, tg_token, tg_chat
import vk_api
import requests
import db
import json
import telebot
from telebot import types
from integrations.vk_send import send_message

tg_bot = telebot.TeleBot(tg_token)
vk = vk_api.VkApi(token=vk_token)

def generate_answer(user_id, question):
    info_data = db.info_sync.get_informations()
    info = ''
    for i in info_data:
        info += f'Информация: {i["info"]} ; Описание: {i["description"]}\n'
    prompt = gpt_users_prompt.replace('%info%', info).replace('%question%', question)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {proxyapi_key}"
    }
    json = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://api.proxyapi.ru/openai/v1/chat/completions", json=json, headers=headers, verify=False)
    answer_gpt = eval(response.json()["choices"][0]["message"]["content"])
    print(answer_gpt)
    answer = answer_gpt["answer"]
    status = answer_gpt["status"]
    if status:
        send_message(user_id, answer)
    else:
        markup = types.InlineKeyboardMarkup()
        btn_edit = types.InlineKeyboardButton(text='✏️ Редактировать', callback_data=f'admin.eq.{user_id}')
        btn_answer = types.InlineKeyboardButton(text='⬅️ Ответить', callback_data=f'admin.aq.{user_id}')
        markup.row(btn_edit)
        markup.row(btn_answer)
        tg_bot.send_message(tg_chat, f'Неизвестный вопрос:\n{question}\n=-=-=-=-=\nВариант ответа:\n{answer}', reply_markup=markup)

