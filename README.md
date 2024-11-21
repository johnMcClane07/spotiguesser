# 🎵 SPOTIGUESSER 🎶  
**Музыкальные викторины с использованием Spotify API**  

![Logo/Preview](https://via.placeholder.com/800x400?text=Music+Quiz+App)

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
'''bash
sudo apt install redis
redis-server



   
   


