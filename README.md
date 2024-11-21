# 🎵 SPOTIGUESSER 🎶  
**Музыкальные викторины с использованием Spotify API**  

<img width="1470" alt="Снимок экрана 2024-11-21 в 18 33 08" src="https://github.com/user-attachments/assets/38541dbe-34ba-4945-bd16-e99b160d729d">

## 📖 О проекте  
Это веб-приложение, созданное на Django, которое позволяет пользователям участвовать в увлекательных музыкальных викторинах. С помощью Spotify API приложение получает песни артистов, и пользователь должен отгадать трек по короткому отрывку  

Основные функции:  
- Авторизация через Spotify.
- Каждый раз рандомные треки исполнителя
- Подсчет очков и отображение рейтингов.  
- Динамичный фронтэнд с помощью HTMX

---

## 🚀 Функционал  

- 🔐 **Авторизация Spotify**: Использование OAuth2 для доступа к данным Spotify.  
- 🎶 **Музыкальные вопросы**: Викторины о треках исполнителя, из Spotify.  
- ⚡ **Кэширование через Redis**: Быстрое взаимодействие с API за счет использования Redis для хранения данных.  
- 🌐 **Интерактивный интерфейс с HTMX**: Асинхронная загрузка данных и плавные обновления страницы без полной перезагрузки.  
- 📊 **Рейтинги**: Сравнивайте свои результаты с другими пользователями.  
- 🕹️ **Интерактивный интерфейс**: Простота использования и яркий дизайн.  


---

## 📂 Установка и запуск  

1. **Клонируйте репозиторий**  
   ```bash
   git clone https://github.com/johnMcClane07/spotiguesser.git
2. **Создайте виртуальное окружение**
   ```bash
   python -m venv env
   source env/bin/activate  # Для macOS/Linux
   env\Scripts\activate     # Для Windows

3. **Установите зависимости**
   ```bash
   pip install -r requirements.txt 


4. **Настройте Редис**
   ```bash
   sudo apt install redis
   redis-server

5. **Настройте переменные окружения и базу данных**
   ```python
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
   }

   SPOTIFY_CLIENT_ID=ваш_client_id
   SPOTIFY_CLIENT_SECRET=ваш_client_secret

6. **Примените миграции и запустите сервер**
   ```bash
   python manage.py migrate
   python manage.py runserver


## 🔧 Технологии  

### Backend  
- **Язык программирования:** Python 3.10+  
- **Фреймворк:** Django  
- **Кэширование:** Redis  
- **API:** Spotify Web API  

### Frontend  
- **Интерактивность:** HTMX  
- **Стилизация:** Bootstrap / TailwindCSS  

### База данных  
-  MySQL 

## 🖼️ Скриншоты 

<img width="1469" alt="Снимок экрана 2024-11-21 в 19 02 34" src="https://github.com/user-attachments/assets/3d6e51c2-277c-49f7-a88a-2a37ec25e998">

<img width="1470" alt="Снимок экрана 2024-11-21 в 19 02 53" src="https://github.com/user-attachments/assets/78c0d1a7-ae14-4b91-bfbe-5ada28dacd26">


   
<img width="1469" alt="Снимок экрана 2024-11-21 в 19 03 58" src="https://github.com/user-attachments/assets/e4a8d4e0-f072-4db4-bc8e-554b98455dbd">


<img width="1470" alt="Снимок экрана 2024-11-21 в 19 04 53" src="https://github.com/user-attachments/assets/54a39de4-c6ab-4f66-9e5e-025d814f4909">
<img width="1470" alt="Снимок экрана 2024-11-21 в 19 05 11" src="https://github.com/user-attachments/assets/abb46b98-3626-43e4-a550-5bafb76af70e">

   
   


