import sys  # Импортируем модуль sys, который предоставляет доступ к некоторым параметрам и функциям интерпретатора Python, включая манипуляцию путями (sys.path).
import os  # Импортируем модуль os для работы с операционной системой, например, для получения путей или работы с переменными окружения.
import ssl  # Импортируем модуль ssl для работы с безопасными соединениями через TLS/SSL.
import paho.mqtt.client as mqtt  # Импортируем библиотеку paho.mqtt.client с псевдонимом mqtt для работы с MQTT протоколом.
from django.conf import settings  # Импортируем объект settings из Django для доступа к настройкам проекта.
from django.db import connection  # Импортируем объект connection для работы с подключением к базе данных в Django.


# Добавляем путь к проекту в sys.path, чтобы корректно настроить Django
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Получаем абсолютный путь к родительской директории
if project_path not in sys.path:  # Если путь к проекту не уже в sys.path
    sys.path.insert(0, project_path)  # Добавляем его в начало списка

# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Указываем, какой модуль настроек Django использовать

import django  # Импортируем Django
django.setup()  # Инициализируем Django, чтобы можно было работать с моделями и базой данных

# Импортируем необходимые модели из Django
from apps.kipclub_ru.models import MQTTSettings  # Модель для получения настроек MQTT из базы данных
from apps.kip_online_ru.models import MQTTBrokerMessage  # Модель для сохранения сообщений MQTT в базу данных

# Функция для загрузки настроек MQTT из базы данных
def get_mqtt_settings():
    try:
        # Получаем настройки MQTT из базы данных (первая запись, если она есть)
        settings = MQTTSettings.objects.first()  # Получаем первые настройки
        if not settings:  # Если настройки не найдены
            raise ValueError("Настройки MQTT не найдены в базе данных.")  # Выбрасываем ошибку
        return settings  # Возвращаем настройки
    except Exception as e:  # Если произошла ошибка
        print(f"Ошибка при загрузке настроек MQTT: {e}")  # Логируем ошибку
        raise  # Выбрасываем исключение дальше

# Функция для сохранения сообщения в таблице MQTTBrokerMessage
def save_mqtt_message(topic, payload):
    try:
        # Сохраняем сообщение в базу данных
        MQTTBrokerMessage.objects.create(
            topic=topic,  # Сохраняем топик (тема сообщения)
            message=payload  # Сохраняем само сообщение как строку
        )
        
        print(f"Сообщение сохранено: Топик {topic}, Сообщение {payload}")  # Логируем успешное сохранение
    except Exception as e:  # Если произошла ошибка при сохранении
        print(f"Ошибка при сохранении сообщения MQTT: {e}")  # Логируем ошибку

# Callback-функции для обработки событий MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:  # Если код возврата подключения равен 0, значит подключение прошло успешно
        print("Подключение к MQTT брокеру успешно.")  # Логируем успешное подключение
        # Подписываемся на топики из настроек (тема передается как строка)
        client.subscribe([(mqtt_settings.MQTT_TOPICS, 0)])  # Подписка на топик с QoS 0
    else:  # Если подключение не удалось
        print(f"Ошибка подключения к MQTT брокеру. Код: {rc}")  # Логируем код ошибки

def on_message(client, userdata, msg):
    # Логируем приходящее сообщение
    print(f"Новое сообщение: Топик: {msg.topic}, Сообщение: {msg.payload.decode()}")

    # Сохраняем сообщение в таблице MQTTBrokerMessage
    save_mqtt_message(msg.topic, msg.payload.decode())  # Передаем топик и сообщение как строки

# Основной код для запуска MQTT клиента
if __name__ == "__main__":  # Проверяем, что скрипт выполняется напрямую, а не импортируется
    try:
        # Получаем настройки MQTT из базы данных
        mqtt_settings = get_mqtt_settings()  # Загружаем настройки с помощью функции get_mqtt_settings()

        # Создаем MQTT клиент
        client = mqtt.Client()  # Инициализируем MQTT клиент
        
        # Устанавливаем имя пользователя и пароль для MQTT подключения
        client.username_pw_set(mqtt_settings.MQTT_USERNAME, mqtt_settings.MQTT_PASSWORD)  # Устанавливаем данные для аутентификации

        # Привязываем callback-функции для обработки событий
        client.on_connect = on_connect  # Устанавливаем обработчик для события подключения
        client.on_message = on_message  # Устанавливаем обработчик для события получения сообщения

        # Если используется шифрование, настраиваем SSL
        if mqtt_settings.ENCRYPTION.lower() == "yes":  # Проверяем, включено ли шифрование
            client.tls_set(
                ca_certs=None,  # Не используем сертификаты CA
                certfile=None,  # Не используем сертификат клиента
                keyfile=None,  # Не используем ключ клиента
                tls_version=ssl.PROTOCOL_TLSv1_2  # Устанавливаем TLS версию 1.2
            )
            client.tls_insecure_set(False)  # Отключаем проверку сертификатов для упрощения

        # Подключаемся к MQTT брокеру
        client.connect(mqtt_settings.MQTT_BROKER, mqtt_settings.MQTT_PORT, 60)  # Подключаемся к брокеру, указывая порт и тайм-аут

        # Запускаем основной цикл для обработки сообщений
        client.loop_forever()  # Этот метод блокирует выполнение и ждет сообщений
    except Exception as e:  # Если произошла ошибка при запуске клиента
        print(f"Ошибка в MQTT клиенте: {e}")  # Логируем ошибку
