from django.shortcuts import  redirect
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import DjangoSessionCacheHandler
from django.conf import settings
from spotipy.oauth2 import SpotifyOauthError




def get_spotify_oauth_handler(request):
    """
    Создает и возвращает объект SpotifyOAuth для аутентификации пользователя Spotify.
    
    """
    chace_handler = DjangoSessionCacheHandler(request)
    return SpotifyOAuth(
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
        redirect_uri=settings.REDIRECT_URI,
        scope=settings.SCOPE,
        cache_handler=chace_handler,
        show_dialog=True
    )

def get_or_refresh_token(request, sp_auth):
    """
    Получает токен аутентификации, если он валиден, или обновляет его,
    если он устарел. Возвращает token_info, если он валиден, или None
    в противном случае.
    """
    token_info = sp_auth.get_cached_token()
    if token_info and sp_auth.validate_token(token_info):
        return token_info  
    else:
        return None  

        
def login(request):
    """
    Функция-обработчик для страницы входа в систему.

    Если пользователь уже аутентифицирован, то возвращает сообщение
    "Токен валиден". Если пользователь не аутентифицирован, то
    перенаправляет на страницу аутентификации, где пользователь может
    ввести свои логин и пароль.

    """
    sp_auth = get_spotify_oauth_handler(request)
    token_info = get_or_refresh_token(request, sp_auth)

    if token_info:
        return redirect('home')
    else:
        auth_url = sp_auth.get_authorize_url()
        return redirect(auth_url)
    
def callback(request):
    """
    Обрабатывает обратный вызов после аутентификации пользователя.

    Извлекает код авторизации из запроса и пытается получить информацию о токене
    доступа с помощью обработчика Spotify OAuth. Если это удается, выводит информацию
    о токене и перенаправляет пользователя на домашнюю страницу. Если возникает ошибка
    аутентификации, пытается получить или обновить токен. В случае успешного получения
    токена перенаправляет на домашнюю страницу, в противном случае перенаправляет
    пользователя на страницу авторизации Spotify.
    """
    sp_auth = get_spotify_oauth_handler(request)
    code = request.GET.get('code')

    try:
        token_info = sp_auth.get_access_token(code)
        print(token_info)
    except SpotifyOauthError:
        token_info = get_or_refresh_token(request, sp_auth)

    if token_info:
        return redirect('home')
    else:
        auth_url = sp_auth.get_authorize_url()
        return redirect(auth_url)


