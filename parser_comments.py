from googleapiclient.discovery import build
import re
import os
from dotenv import load_dotenv

load_dotenv()

class YoutubeParser:

    def __init__(self):
        self.api = os.getenv('API')  # Наш API для связи с YouTube

    def get_comments(self, video_http):
        self.video_http = video_http
        self.video_id = re.findall(r'=[_A-Za-z0-9-]*', self.video_http)  # Получаем ID видео из ссылки
        self.video_id = self.video_id[0].replace('=', '')
        self.comments_list = []  # Создаем список для хранения комментариев
        self.youtube = build('youtube', 'v3', developerKey=self.api)  # Соединяем программу с YouTube
        self.video_response = self.youtube.commentThreads().list(      #
            part='snippet',                                            # Получаем информацию по видео в виде словаря
            videoId=self.video_id                                      #
        ).execute()

        while self.video_response:

            for item in self.video_response['items']:  # Проходим по ключу с комментариями

                self.comment = item['snippet']['topLevelComment']['snippet']['textOriginal']  # Получаем комментарии
                self.comments_list.append(self.comment)  # Добавляем комментарий в список

            if ('nextPageToken' in self.video_response) and (len(self.comments_list) <= 200):  # Проверяем есть ли токен следующей страницы и длина не превышает 300 комментариев

                nextPageToken = self.video_response['nextPageToken']  # Если токен есть, то получаем его
                self.video_response = self.youtube.commentThreads().list(
                    part='snippet',
                    videoId=self.video_id,
                    pageToken=nextPageToken  # Переходим на следующую страницу
                ).execute()
            else:
                break  # Если токена нет, то конец

        return self.comments_list

