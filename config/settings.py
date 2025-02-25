import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env (если таковой имеется).
# Это полезно для хранения секретных данных (таких как ключи и пароли) вне исходного кода.
load_dotenv()

# Определяем базовую директорию проекта. Это корневая папка, в которой находится manage.py,
# и она будет использоваться для построения абсолютных путей к файлам и папкам проекта.
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ Django, который необходим для защиты данных и безопасности.
# Он должен быть уникальным и не должен быть доступен публично.
# Значение по умолчанию 'your_default_secret_key' следует заменить.
SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')

# Включение режима отладки. Если DEBUG=True, Django покажет более подробные сообщения об ошибках.
# Для продакшн-сервера рекомендуется устанавливать DEBUG=False.
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Список доменных имён или IP-адресов, которые разрешены для обращения к проекту.
# Доступ к проекту будет запрещён для запросов с других доменов.
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'kipclub.ru', 'www.kipclub.ru', 'kipclub.store', 'www.kipclub.store', 'kip-online.ru', 'www.kip-online.ru', 'kipcloud.ru', 'www.kipcloud.ru']

# Список установленных приложений, включая стандартные приложения Django, сторонние библиотеки
# (например, REST framework), а также пользовательские приложения проекта.
INSTALLED_APPS = [
    'django.contrib.admin',             # Административный интерфейс
    'django.contrib.auth',              # Аутентификация и права доступа
    'django.contrib.contenttypes',      # Система типов содержимого
    'django.contrib.sessions',          # Поддержка сессий
    'django.contrib.messages',          # Сообщения
    'django.contrib.staticfiles',       # Управление статическими файлами
    'rest_framework',                   # Django REST Framework для построения API
    'django_celery_beat',               # Celery Beat для периодических задач
    'apps.kipclub_ru',                  # Основное приложение проекта (информация и услуги компании)
    'apps.kipclub_store',               # Приложение для интернет-магазина
    'apps.kip_online_ru',               # Приложение для мониторинга корпоративных клиентов
    'apps.kipcloud_ru',                 # Приложение для мониторинга частных клиентов
]

# Промежуточное ПО (middleware) обрабатывает запросы и ответы между клиентом и сервером.
# Каждое промежуточное ПО выполняет определённые функции (безопасность, управление сессиями и т.д.).
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',        # Основная защита безопасности
    'django.contrib.sessions.middleware.SessionMiddleware', # Поддержка сессий
    'django.middleware.common.CommonMiddleware',            # Общие процессы
    'django.middleware.csrf.CsrfViewMiddleware',            # Защита от CSRF-атак
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Аутентификация
    'django.contrib.messages.middleware.MessageMiddleware', # Сообщения
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Защита от Clickjacking
#    'config.middleware.HostRoutingMiddleware',         # Это наш файл для настройки маршрутизации middleware/HostRoutingMiddleware.py
    'config.middleware.HostRoutingMiddleware.HostRoutingMiddleware',     
]

# Корневой URL конфиг - указывает на файл, где находится основная маршрутизация URL-адресов проекта.
ROOT_URLCONF = 'config.urls'

# Настройки шаблонов. Здесь определяется, как Django обрабатывает HTML-шаблоны.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Бэкэнд шаблонизатора
        'DIRS': [BASE_DIR / 'templates'],  # Папка для пользовательских шаблонов
        'APP_DIRS': True,  # Автоматический поиск шаблонов в приложениях проекта
        'OPTIONS': {
            'context_processors': [  # Процессоры контекста, добавляющие данные во все шаблоны
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Настройки WSGI (для обработки стандартных HTTP-запросов) и ASGI (для асинхронных запросов).
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Настройки подключения к базе данных. Здесь используется PostgreSQL.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Движок базы данных PostgreSQL
        'NAME': os.getenv('DB_NAME', 'kipclub_db'), # Имя базы данных
        'USER': os.getenv('DB_USER', 'kipclub_user'), # Имя пользователя базы данных
        'PASSWORD': os.getenv('DB_PASSWORD', 'owlpass'), # Пароль пользователя
        'HOST': os.getenv('DB_HOST', 'localhost'), # Хост базы данных
        'PORT': os.getenv('DB_PORT', '5432'), # Порт для подключения
    }
}

# Валидаторы паролей. Они обеспечивают минимальный уровень безопасности паролей для пользователей.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Локализация и настройки часового пояса
LANGUAGE_CODE = 'ru-ru'   # Устанавливает русский язык как основной
TIME_ZONE = 'UTC'         # Устанавливает UTC в качестве часового пояса
USE_I18N = True           # Включает интернационализацию
USE_L10N = True           # Включает локализацию форматов (дата, время, числа)
USE_TZ = True             # Включает поддержку временных зон

# Настройки для хранения и доступа к статическим и медиа-файлам.
STATIC_URL = '/static/'                      # URL для доступа к статическим файлам
STATICFILES_DIRS = [BASE_DIR / 'static']     # Папка для статических файлов
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'                        # URL для доступа к медиа-файлам
MEDIA_ROOT = BASE_DIR / 'media'              # Папка для хранения медиа-файлов

# Настройки Django REST Framework (DRF) для аутентификации и разрешений.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication', # Аутентификация по сессии
        'rest_framework.authentication.BasicAuthentication',   # Базовая аутентификация
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',          # Доступ только для аутентифицированных пользователей
    ],
}

# Настройки Celery (для фоновых задач) и Redis (в качестве брокера и хранилища результатов задач).
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0') # Адрес брокера сообщений Redis
CELERY_RESULT_BACKEND = CELERY_BROKER_URL                               # Хранилище для результатов выполнения задач
CELERY_ACCEPT_CONTENT = ['json']                                       # Форматы данных, поддерживаемые Celery
CELERY_TASK_SERIALIZER = 'json'                                        # Формат сериализации задач
CELERY_RESULT_SERIALIZER = 'json'                                      # Формат сериализации результатов
CELERY_TIMEZONE = TIME_ZONE                                           # Часовой пояс для задач Celery

# Настройки логирования. Они определяют обработчики и уровни для записи логов.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,   # Позволяет сохранять существующие логгеры
    'handlers': {
        'file': {                       # Обработчик записи логов в файл
            'level': 'DEBUG',           # Уровень записи логов (DEBUG - для отладки)
            'class': 'logging.FileHandler', # Класс для записи логов в файл
            'filename': BASE_DIR / 'debug.log', # Путь к файлу логов
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],       # Используемый обработчик
            'level': 'DEBUG',           # Уровень логирования для Django
            'propagate': True,          # Пропаганда логов на верхние уровни
        },
    },
}
