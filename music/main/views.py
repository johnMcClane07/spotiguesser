from django.shortcuts import render, redirect
from .models import QuizResult
from spotipy import Spotify,exceptions
import random
from django.utils import timezone
from django.core.cache import cache
from accounts.views import get_spotify_oauth_handler
from django.conf import settings
from accounts.views import get_or_refresh_token


def is_authenticated(request):
    """
    Проверяет, аутентифицирован ли пользователь.

    Получает информацию о токене с помощью функции get_or_refresh_token.
    Если токен валиден, возвращает True, иначе False.

    """
    token_info = get_or_refresh_token(request, get_spotify_oauth_handler(request))
    if token_info:
        return True
    else:
        return False    
    

def homepage(request):
    """
    Главная страница. Показывает случайные 5 любимых исполнителей
    аутентифицированного пользователя. Если пользователь не аутентифицирован,
    то просто отображает страницу.

    """
    
    try:
        counter=cache.get('quiz_initializations_count')
        if is_authenticated(request):
            homepage_id=f'{Spotify(auth=request.session["token_info"]["access_token"]).current_user()["display_name"]}'
            homepage_artists=cache.get(homepage_id)
            if not homepage_artists:
                favourite_artists=Spotify(auth=request.session['token_info']['access_token']).current_user_followed_artists()['artists']['items']
                favourite_artists_info=[]
                for artist in favourite_artists:
                    info={
                        'name':artist['name'],
                        'id':artist['id'],
                        'image_url':artist['images'][0]['url'] if artist['images'] else None
                    }
                    favourite_artists_info.append(info)
                cache.set(homepage_id,favourite_artists_info)

                homepage_artists = favourite_artists_info
        
            
            return render(request, 'home.html',{
                'is_authenticated': is_authenticated(request)
                ,
                'favourite_artists':random.sample(homepage_artists, 5),

                'counter':counter
            })
        else:
            return render(request, 'home.html',{'is_authenticated': is_authenticated(request),'counter':counter})
    except exceptions.SpotifyException as e:
        if e.http_status == 401:
            get_or_refresh_token(request, get_spotify_oauth_handler(request))
            return redirect('homepage')
        else:
            return render(request, 'error.html', {'error': str(e)})

def search(request):
    """
    Обрабатывает поиск исполнителей по запросу пользователя.
    
    Если запрос пришел с использованием HTMX, извлекает поисковую строку из
    параметров запроса и выполняет поиск исполнителей с использованием Spotify API.
    Возвращает до 5 исполнителей, включая их изображения, если они имеются.
    Если поисковый запрос пустой, возвращает пустой список исполнителей.
    
    В случае успешного выполнения возвращает шаблон 'home_partial.html' с контекстом
    найденных исполнителей. Если запрос не использует HTMX, возвращает шаблон 'home.html'.
    
    Если возникает ошибка аутентификации Spotify, пытается обновить токен и перенаправляет
    на частичный поиск.
    """
    try:
        if request.htmx:
            search = request.GET.get('q')
            if search:
                sp=Spotify(auth=request.session['token_info']['access_token'])
                artists = sp.search(search, type='artist', limit=5)['artists']['items']
                
                for artist in artists:
                    artist['image_url'] = artist['images'][0]['url'] if artist['images'] else None
                
            else:
                artists = []

            return render(
                request=request,
                template_name='home_partial.html',
                context={
                    'artists': artists,
                }
            )
        return render(request, 'home.html',{
                })
    except exceptions.SpotifyException as e:
        if e.http_status == 401:
            get_or_refresh_token(request, get_spotify_oauth_handler(request))
            return redirect('partial_search')
def quiz(request, artist_id):
    """
    Викторина. Показывает случайный трек исполнителя,
    даёт выбор из трёх вариантов, и если пользователь
    угадывает, то увеличивает счёт.
    
    Если пользователь не угадывает, то ничего не делает.
    
    Если пользователь отгадает 10 треков, то
    перенаправляет на страницу результатов викторины.
    
    Если возникает ошибка аутентификации Spotify, то
    пытается обновить токен и перенаправляет на викторину.
    """
    try:
        quiz_id = f'{request.session["token_info"]["access_token"]}{artist_id}'
        quiz_data = cache.get(quiz_id)

        if quiz_data is None:
            try:
                sp = Spotify(auth=request.session['token_info']['access_token'])
                artist_name = sp.artist(artist_id)['name']
                albums = sp.artist_albums(artist_id)['items']
                albums_id = [album['id'] for album in albums][:20]
                albums_data = sp.albums(albums_id)['albums']
                tracks = []
                for album in albums_data:
                    album_image = album['images'][0]['url'] if album['images'] else None

                    for track in album['tracks']['items']:
                        if 'preview_url' not in track:
                            continue
                        if not any(artist['name'] == artist_name for artist in track['artists']):
                            continue
                        track_info = {
                            "name": track['name'],
                            'id': track['id'],
                            "artists": [artist['name'] for artist in track['artists']],
                            "duration_ms": track['duration_ms'],
                            "preview_url": track['preview_url'],
                            "album_image": album_image,
                            'start_time': timezone.now()
                        }
                        tracks.append(track_info)

                try:
                    true_answers = random.sample(tracks, 10)
                except ValueError:
                    return render(request, 'error.html', {'error': 'У исполнителя слишком мало треков'})

                quiz_data = {
                    'progress': 0,
                    'score': 0,
                    'tracks': tracks,
                    'true_answers': true_answers,
                    'current_track': true_answers[0]
                }
                cache.set(quiz_id, quiz_data)

            except exceptions.SpotifyException as e:
                if e.http_status == 401:
                    get_or_refresh_token(request, get_spotify_oauth_handler(request))
                    return quiz(request, artist_id) 
                else:
                    raise e

        progress = quiz_data['progress']
        score = quiz_data['score']
        tracks = quiz_data['tracks']
        true_answers = quiz_data['true_answers']

        if progress >= 9:
            end_time = timezone.now()
            elapsed_time = (end_time - quiz_data['current_track']['start_time']).seconds
            if not cache.get('quiz_initializations_count'):
                cache.set('quiz_initializations_count', 0)

            cache.incr('quiz_initializations_count')
            cache.persist('quiz_initializations_count')
            cache.delete(quiz_id)
            return render(request, 'quiz_result.html', {'score': score, 'total_questions': len(true_answers), 'time': elapsed_time, 'artist_id': artist_id})

        current_track = true_answers[progress]
        fake_answers = [track for track in tracks if track not in true_answers]
        options = random.sample([current_track] + random.sample(fake_answers, 2), 3)

        if request.method == 'POST' and request.POST.get('answer'):
            user_answer = request.POST.get('answer')
            if user_answer == current_track['name']:
                quiz_data['score'] += 1

            quiz_data['progress'] += 1

            if quiz_data['progress'] <= 9:
                quiz_data['current_track'] = true_answers[quiz_data['progress']]

            cache.set(quiz_id, quiz_data)

            if quiz_data['progress'] < len(true_answers):
                current_track = true_answers[quiz_data['progress']]

            fake_answers = [track for track in tracks if track not in true_answers]
            options = [current_track] + random.sample(fake_answers, 2)
            random.shuffle(options)

            if request.htmx:
                return render(request, 'quiz_content.html', {
                    'current_track': current_track,
                    'options': options,
                    'progress': quiz_data['progress'] + 1,
                    'total_questions': len(true_answers),
                    'artist_id': artist_id
                })

        return render(request, 'quiz.html', {
            'current_track': current_track,
            'options': options,
            'progress': quiz_data['progress'] + 1,
            'total_questions': len(true_answers),
            'artist_id': artist_id
        })

    except exceptions.SpotifyException as e:
        if e.http_status == 401:
            get_or_refresh_token(request, get_spotify_oauth_handler(request))
            return quiz(request, artist_id)  
        else:
            return render(request, 'error.html', {'error': str(e)})



def save_result(request, artist_id):
    """
    Сохраняет результат викторины для указанного исполнителя.

    Если метод запроса POST, извлекает счет и затраченное время из данных формы,
    обновляет или создает запись QuizResult для текущего пользователя и исполнителя.
    Затем извлекает и отображает таблицу с лучшими результатами для данного исполнителя.

    В случае ошибки аутентификации Spotify, обновляет токен и повторяет попытку.
    В случае других ошибок Spotify, отображает страницу с сообщением об ошибке.

    """
    try:
        if request.method == 'POST':
            score = request.POST.get('score')
            elapsed_time = request.POST.get('elapsed_time')

            QuizResult.objects.update_or_create(
            user=Spotify(auth=request.session['token_info']['access_token']).current_user()['display_name'],
            artist=artist_id,
            defaults={
                'score': score,
                'elapsed_time': elapsed_time,
                'artist_name': Spotify(auth=request.session['token_info']['access_token']).artist(artist_id)['name']
            }
        )
            
            best_results = QuizResult.objects.filter(artist=artist_id).order_by('-score', 'elapsed_time')

            return render(request, 'quiz_result_table.html', {'quiz_result': best_results})
        
        return redirect('quiz', artist_id=artist_id)
    except exceptions.SpotifyException as e:
        if e.http_status == 401:
            get_or_refresh_token(request, get_spotify_oauth_handler(request))
            return save_result(request, artist_id)  
        else:
            return render(request, 'error.html', {'error': str(e)})

def user_profile(request):
    """
    Отображает профиль пользователя с информацией о пройденных викторинах.

    Извлекает и отображает список викторин, которые пользователь прошел, 
    отсортированный по дате в порядке убывания. В случае ошибки аутентификации 
    Spotify, обновляет токен и повторяет попытку. В случае других ошибок Spotify, 
    отображает страницу с сообщением об ошибке.
    """
    try:
        user_quizes=QuizResult.objects.filter(user=Spotify(auth=request.session['token_info']['access_token']).current_user()['display_name']).order_by('-date')
        return render(request, 'profile.html',{'completed_quizzes':user_quizes})
    except exceptions.SpotifyException as e:
        if e.http_status == 401:
            get_or_refresh_token(request, get_spotify_oauth_handler(request))
            return user_profile(request)  
        else:
            return render(request, 'error.html', {'error': str(e)})
