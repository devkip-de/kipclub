import sys
import os
import ssl
import paho.mqtt.client as mqtt
from django.conf import settings
from django.db import connection

# Шаг 1: Убедимся, что путь к проекту добавлен в sys.path
# Это необходимо, чтобы корректно настроить Django, даже если скрипт запускается из папки scripts
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Получаем путь к корню проекта
if project_path not in sys.path:  # Если путь не в sys.path, добавляем его
    sys.path.insert(0, project_path)

# Шаг 2: Устанавливаем переменную окружения для Django, указывая настройки проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Указываем путь к файлу настроек Django

import django  # Импортируем Django после добавления пути
django.setup()  # Настроим Django, чтобы можно было использовать его функциональность

# Шаг 3: Импортируем модель настроек для MQTT
from apps.kipclub_ru.models import MQTTSettings  # Модель для получения настроек MQTT из базы данных

# Функция для загрузки настроек MQTT из базы данных
def get_mqtt_settings():
    try:
        settings = MQTTSettings.objects.first()  # Получаем первые настройки MQTT из базы данных
        if not settings:
            raise ValueError("Настройки MQTT не найдены в базе данных.")  # Если настройки не найдены, вызываем исключение
        return settings  # Возвращаем настройки
    except Exception as e:
        print(f"Ошибка при загрузке настроек MQTT: {e}")  # Печатаем ошибку, если что-то пошло не так
        raise

# Callback функции MQTT
def on_connect(client, userdata, flags, rc):
    """Callback функция, которая будет вызвана после успешного подключения к MQTT брокеру."""
    if rc == 0:
        print("Подключение к MQTT брокеру успешно.")
        client.subscribe([(mqtt_settings.MQTT_TOPICS, 0)])  # Подписываемся на топик
    else:
        print(f"Ошибка подключения к MQTT брокеру. Код: {rc}")

def on_message(client, userdata, msg):
    """Callback функция, которая будет вызвана при получении сообщения."""
    print(f"Новое сообщение: Топик: {msg.topic}, Сообщение: {msg.payload.decode()}")

# Основной код
if __name__ == "__main__":
    try:
        # Шаг 4: Загрузка настроек MQTT из базы данных
        mqtt_settings = get_mqtt_settings()

        # Шаг 5: Настройка MQTT клиента
        client = mqtt.Client()  # Создаем объект клиента MQTT
        client.username_pw_set(mqtt_settings.MQTT_USERNAME, mqtt_settings.MQTT_PASSWORD)  # Устанавливаем логин и пароль
        client.on_connect = on_connect  # Привязываем callback для подключения
        client.on_message = on_message  # Привязываем callback для получения сообщений

        # Шаг 6: Подключение SSL/TLS (если настроено)
        if mqtt_settings.ENCRYPTION.lower() == "yes":  # Если шифрование включено
            client.tls_set(
                ca_certs=None,  # Путь к сертификату CA, если используется
                certfile=None,  # Путь к сертификату клиента, если используется
                keyfile=None,  # Путь к приватному ключу, если используется
                tls_version=ssl.PROTOCOL_TLSv1_2  # Указываем используемую версию TLS
            )
            client.tls_insecure_set(False)  # Запрещаем использование небезопасных TLS соединений

        # Шаг 7: Подключение к MQTT брокеру
        client.connect(mqtt_settings.MQTT_BROKER, mqtt_settings.MQTT_PORT, 60)  # Подключаемся к брокеру
        client.loop_forever()  # Запускаем бесконечный цикл получения сообщений

    except Exception as e:
        print(f"Ошибка в MQTT клиенте: {e}")  # Печатаем ошибку, если что-то пошло не так
