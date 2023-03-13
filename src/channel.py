import json
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build


"""Загружаем путь до файла с перменными окружения"""
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

YT_API_KEY = os.environ.get("YT_API_KEY")


class Channel:
    """Класс для ютуб-канала"""

    OBJ = build('youtube', 'v3', developerKey=YT_API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        self.channel = self.OBJ.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']
        self.url = self.get_correct_url()

    @property
    def channel_id(self):
        """Геттер для self.channel_id"""
        return self.__channel_id

    def to_json(self, file):
        """
        Запись атрибутов экземпляра класса в json
        """
        with open(file, 'w') as file:
            json.dump(self.__dict__, file, indent=4, ensure_ascii=False)

    @classmethod
    def get_service(cls):
        """
        Метод получения обьекта класса googleapiclient через класс Channel
        """
        return cls.OBJ

    def get_correct_url(self):
        """
        Вспомогательный метод для получения url каннала
        """
        hosting = self.channel['items'][0]['kind'].split('#')[0]
        channel = self.channel['items'][0]['kind'].split('#')[1]
        url = f"https://www.{hosting}.com/{channel}/{self.__channel_id}"
        return url

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

