import vk_api
from config import vk_token

vk = vk_api.VkApi(token=vk_token)

def send_message(user_id, message):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,  # Отправляем то же сообщение
        'random_id': 0,  # Уникальный ID для каждого сообщения
    })