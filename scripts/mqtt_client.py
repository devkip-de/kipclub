# /scripts/mqtt_client.py
import os
import ssl
import paho.mqtt.client as mqtt
from django.db import connection
from django.conf import settings

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.kipclub_ru.models import MQTTSettings  # Импорт модели настроек

# Функция для загрузки настроек MQTT из базы данных
def get_mqtt_settings():
    try:
        settings = MQTTSettings.objects.first()
        if not settings:
            raise ValueError("Настройки MQTT не найдены в базе данных.")
        return settings
    except Exception as e:
        print(f"Ошибка при загрузке настроек MQTT: {e}")
        raise

# Callback функции MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Подключение к MQTT брокеру успешно.")
        client.subscribe([(settings.mqtt_topic, 0)])  # Подписка на топик
    else:
        print(f"Ошибка подключения к MQTT брокеру. Код: {rc}")

def on_message(client, userdata, msg):
    print(f"Новое сообщение: Топик: {msg.topic}, Сообщение: {msg.payload.decode()}")

# Основной код
if __name__ == "__main__":
    try:
        # Загрузка настроек из базы данных
        mqtt_settings = get_mqtt_settings()

        # Настройка клиента MQTT
        client = mqtt.Client()
        client.username_pw_set(mqtt_settings.mqtt_username, mqtt_settings.mqtt_password)
        client.on_connect = on_connect
        client.on_message = on_message

        # Подключение SSL/TLS (если включено)
        if mqtt_settings.encryption.lower() == "yes":
            client.tls_set(
                ca_certs=None,  # Путь к файлу сертификата CA
                certfile=None,
                keyfile=None,
                tls_version=ssl.PROTOCOL_TLSv1_2
            )
            client.tls_insecure_set(False)

        # Подключение к брокеру
        client.connect(mqtt_settings.mqtt_broker, mqtt_settings.mqtt_port, 60)
        client.loop_forever()

    except Exception as e:
        print(f"Ошибка в MQTT клиенте: {e}")
