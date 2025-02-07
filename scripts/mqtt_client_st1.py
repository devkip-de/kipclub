import paho.mqtt.client as mqtt
from django.utils.timezone import now
from apps.kip_online_ru.models import MQTTBrokerMessage

# Настройки MQTT
MQTT_BROKER = "kip-online.ru"
MQTT_PORT = 8883
MQTT_TOPICS = [("#", 0)]  # Подписаться на все топики
MQTT_USERNAME = "dev_mqtt"
MQTT_PASSWORD = "MA_19Va%ReN"

def on_connect(client, userdata, flags, rc):
    """Функция вызывается при подключении к брокеру."""
    if rc == 0:
        print("Подключено к MQTT брокеру")
        for topic, qos in MQTT_TOPICS:
            client.subscribe(topic, qos)
            print(f"Подписан на топик: {topic}")
    else:
        print(f"Ошибка подключения, код: {rc}")

def on_message(client, userdata, msg):
    """Функция вызывается при получении сообщения."""
    print(f"Сообщение получено: {msg.topic} - {msg.payload.decode()}")
    try:
        # Сохранение сообщения в базу данных
        MQTTBrokerMessage.objects.create(
            client_id=client._client_id.decode(),
            topic=msg.topic,
            message=msg.payload.decode(),
            time_stamp=now()
        )
        print(f"Сообщение сохранено в базе данных: {msg.topic}")
    except Exception as e:
        print(f"Ошибка сохранения сообщения: {e}")

def run_mqtt_client():
    """Запуск клиента MQTT."""
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    # Настройка SSL
    client.tls_set(
        ca_certs="/etc/letsencrypt/live/kip-online.ru/fullchain.pem",
        certfile="/etc/letsencrypt/live/kip-online.ru/cert.pem",
        keyfile="/etc/letsencrypt/live/kip-online.ru/privkey.pem"
    )

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        client.loop_forever()
    except Exception as e:
        print(f"Ошибка подключения к брокеру MQTT: {e}")

if __name__ == "__main__":
    run_mqtt_client()
