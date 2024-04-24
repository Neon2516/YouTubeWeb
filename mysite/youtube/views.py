from django.shortcuts import render, redirect
from flask import Flask, render_template
from django.views.decorators.csrf import csrf_protect



@csrf_protect
def index(request):
    return render(request, "youtube/index.html")
@csrf_protect
def analysisChannel(request):
    import googleapiclient.discovery

    # Авторизация через OAuth 2.0
    # api_key = "AIzaSyBG5PdXn1r6v8zRl7Tf7TlsRp7ysjbqVA4"
    # youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    #
    # # Получение данных о видео
    # video_id = "81p5kQdmROg"
    # video_response = youtube.videos().list(part="snippet,contentDetails", id=video_id).execute()
    #
    # # Печать данных о видео
    # video_title = video_response["items"][0]["snippet"]["title"]
    # video_description = video_response["items"][0]["snippet"]["description"]
    # video_duration = video_response["items"][0]["contentDetails"]["duration"]
    #
    # print("Название видео:", video_title)
    # print("Описание видео:", video_description)
    # print("Продолжительность видео:", video_duration)

    import googleapiclient.discovery

    def get_channel_views(channel_id):
        api_key = "AIzaSyBG5PdXn1r6v8zRl7Tf7TlsRp7ysjbqVA4"

        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

        response = youtube.channels().list(
            id=channel_id,
            part="statistics"
        ).execute()

        view_count = response["items"][0]["statistics"]["viewCount"]

        print("Количество просмотров - ", view_count)

    def get_average_views_per_video(channel_id):
        api_key = "AIzaSyBG5PdXn1r6v8zRl7Tf7TlsRp7ysjbqVA4"

        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

        response = youtube.channels().list(
            id=channel_id,
            part="statistics"
        ).execute()

        view_count = response["items"][0]["statistics"]["viewCount"]
        video_count = response["items"][0]["statistics"]["videoCount"]

        if int(video_count) == 0:
            return 0

        average_views_per_video = int(int(view_count) / int(video_count))

        print("Среднее количество просмотров - ", average_views_per_video)

    def get_video_count(channel_id):
        api_key = "AIzaSyBG5PdXn1r6v8zRl7Tf7TlsRp7ysjbqVA4"

        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

        response = youtube.channels().list(
            id=channel_id,
            part="statistics"
        ).execute()

        video_count = response["items"][0]["statistics"]["videoCount"]

        return int(video_count)

    import os

    def get_channel_videos(id, max_count=0):
        import scrapetube
        if max_count == 0:
            max_count = get_video_count(id)
        count = 0
        videos = scrapetube.get_channel(id)
        vid = []
        for video in videos:
            if count > max_count:
                break
            count += 1
            vid.append(video['videoId'])
        return vid

    from googleapiclient.discovery import build

    def get_video_views(video_ids):
        counts_views = []
        youtube = build('youtube', 'v3', developerKey="AIzaSyBG5PdXn1r6v8zRl7Tf7TlsRp7ysjbqVA4")
        for video_id in video_ids:

            request = youtube.videos().list(
                part='statistics',
                id=video_id
            )

            response = request.execute()

            if 'items' in response and len(response['items']) > 0:
                view_count = response['items'][0]['statistics']['viewCount']
                counts_views.insert(0, int(view_count))
            else:
                return 'Video not found or statistics not available'
        return counts_views

    def get_video_likes(video_ids):
        youtube = build('youtube', 'v3', developerKey="AIzaSyBG5PdXn1r6v8zRl7Tf7TlsRp7ysjbqVA4")
        likes = []
        for video_id in video_ids:
            request = youtube.videos().list(
                part='statistics',
                id=video_id
            )

            response = request.execute()

            if 'items' in response and len(response['items']) > 0:
                like_count = response['items'][0]['statistics']['likeCount']
                likes.append(int(like_count))
            else:
                return 'Video not found or statistics not available'
        return likes

    def get_video_comments(video_ids):
        youtube = build('youtube', 'v3', developerKey="AIzaSyBG5PdXn1r6v8zRl7Tf7TlsRp7ysjbqVA4")
        comments = []
        for video_id in video_ids:
            request = youtube.videos().list(
                part='statistics',
                id=video_id
            )

            response = request.execute()

            if 'items' in response and len(response['items']) > 0:
                comment_count = response['items'][0]['statistics']['commentCount']
                comments.append(int(comment_count))
            else:
                return 'Video not found or statistics not available'

        return comments

    def get_channel_subscribers(channel_id, path):
        youtube = build('youtube', 'v3', developerKey="AIzaSyBG5PdXn1r6v8zRl7Tf7TlsRp7ysjbqVA4")

        request = youtube.channels().list(
            part='statistics',
            id=channel_id
        )

        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            subscriber_count = response['items'][0]['statistics']['subscriberCount']
            return subscriber_count
            #print(f"Канал {path[path.rindex('/') + 2:]} имеет {subscriber_count} подписчиков")
        else:
            return 'Channel not found or statistics not available'

    import requests

    def get_page_source(url):
        """Получает исходный код веб-страницы по ее URL-адресу.

        Args:
          url: URL-адрес веб-страницы.

        Returns:
          Исходный код веб-страницы в виде строки или None в случае ошибки.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            str = response.text[response.text.rindex('"channelId"') + 13:]
            id = str[:str.index('"')]
            return id
        except requests.exceptions.RequestException:
            return None

    def median(arr):
        """
        Находит медиану в массиве.

        Медиана - это среднее значение, разделяющее верхнюю и нижнюю половины отсортированного массива.

        Args:
          arr (list): Массив чисел.

        Returns:
          float: Медиана массива.
        """

        # Сортируем массив
        arr.sort()

        # Если массив пуст, возвращаем None
        if not arr:
            return None

        # Если массив содержит нечетное количество элементов, возвращаем среднее значение центрального элемента
        if len(arr) % 2 == 1:
            return int(arr[len(arr) // 2])

        # Если массив содержит четное количество элементов, возвращаем среднее значение двух центральных элементов
        else:
            return int(int(arr[len(arr) // 2 - 1] + arr[len(arr) // 2]) / 2)

    def avg(mas):
        return sum(mas) // len(mas)
    def get_most_video_views(video_ids):
        most_views = 0
        video = ""
        youtube = build('youtube', 'v3', developerKey="AIzaSyBG5PdXn1r6v8zRl7Tf7TlsRp7ysjbqVA4")
        for video_id in video_ids:

            request = youtube.videos().list(
                part='statistics',
                id=video_id
            )

            response = request.execute()

            if 'items' in response and len(response['items']) > 0:
                view_count = int(response['items'][0]['statistics']['viewCount'])
                if view_count > most_views:
                    most_views = view_count
                    video = video_id
            else:
                return 'Video not found or statistics not available'
        return video

    def get_most_video_likes(video_ids):
        youtube = build('youtube', 'v3', developerKey="AIzaSyBG5PdXn1r6v8zRl7Tf7TlsRp7ysjbqVA4")
        likes = 0
        video = ""
        for video_id in video_ids:
            request = youtube.videos().list(
                part='statistics',
                id=video_id
            )

            response = request.execute()

            if 'items' in response and len(response['items']) > 0:
                like_count = response['items'][0]['statistics']['likeCount']
                if int(like_count) > int(likes):
                    likes = int(like_count)
                    video = video_id
            else:
                return 'Video not found or statistics not available'
        return video

    if request.method == "POST":
        input_value = request.POST.get("link_channel")
        if not(input_value):
            return redirect("index")

    path = request.POST.get('link_channel')#"https://www.youtube.com/@ExileShow"
    id = get_page_source(path)
    subscribers = int(get_channel_subscribers(id, path))
    videos = get_channel_videos(id, 49)
    counts_views = get_video_views(videos)
    counts_likes = get_video_likes(videos)
    counts_comments = get_video_comments(videos)
    average_views = int(avg(counts_views))
    name = path[path.rindex('/') + 2:]
    most_views_video = get_most_video_views(videos)
    most_likes_video = get_most_video_likes(videos)

    total = subscribers + average_views
    subscribers_percent = round((subscribers / total) * 100)
    average_views_percent = round((average_views / total) * 100)

    data = {"most_likes_video": most_likes_video, "most_views_video": most_views_video,"counts_comments": counts_comments,"counts_likes": counts_likes,"counts_views": counts_views, "name": name, "subscribers": subscribers, "average_views": average_views, "subscribers_percent": subscribers_percent, "average_views_percent": average_views_percent }
    return render(request, "youtube/analysisChannel.html", context=data)

