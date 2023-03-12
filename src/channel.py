import json
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

YT_API_KEY = os.environ.get("YT_API_KEY")


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id  = channel_id
        self._youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self._youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))
