import pymysql
from utils.db.db import DB

from pydantic import BaseModel


class Channel:
    def __init__(self):
        db = DB()
        self.connection = db.get_connection()
        self.cursor = self.connection.cursor()

    def add_channel(self, name: str, url_id: int) -> None:
        sql = """
            INSERT INTO my_channels (name, url_id)
            VALUES (%s, %s)
        """
        self.cursor.execute(sql, (name, url_id))
        self.connection.commit()
        print(f"Channel '{name}' added successfully.")

    def get_channels(self) -> list:
        sql = """
            SELECT id, name, url_id
            FROM my_channels
        """
        self.cursor.execute(sql)
        channels = self.cursor.fetchall()
        return [{"id": channel[0], "name": channel[1], 'url_id': channel[2]} for channel in channels]

    def remove_channel(self, channel_id: int) -> None:
        sql = """
            DELETE FROM my_channels
            WHERE id = %s
        """
        self.cursor.execute(sql, (channel_id,))
        self.connection.commit()
        print(f"Channel with ID '{channel_id}' removed successfully.")

    def get_channel_keywords(self, channel_id: int) -> list:
        sql = """
            SELECT keyword
            FROM keywords
            WHERE channel_id = %s
        """
        self.cursor.execute(sql, (channel_id,))
        keywords = self.cursor.fetchall()
        return [keyword[0] for keyword in keywords]

    def get_channel_id_by_name(self, name: str) -> int:
        sql = """
            SELECT id
            FROM my_channels
            WHERE name = %s
        """
        self.cursor.execute(sql, (name,))
        channel_id = self.cursor.fetchone()[0]
        return channel_id

    def get_channel_url_by_name(self, name: int) -> int:
        sql = """
            SELECT url_id
            FROM my_channels
            WHERE name = %s
        """
        self.cursor.execute(sql, (name,))
        channel_url = self.cursor.fetchone()[0]
        return channel_url

    def get_channel_name_by_id(self, channel_id: int) -> str:
        sql = """
            SELECT name
            FROM my_channels
            WHERE id = %s
        """
        self.cursor.execute(sql, (channel_id,))
        channel_name = self.cursor.fetchone()[0]
        return channel_name
