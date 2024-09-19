import pymysql
from utils.db.db import DB
from pydantic import BaseModel


class Keyword:
    def __init__(self):
        db = DB()
        self.connection = db.get_connection()
        self.cursor = self.connection.cursor()

    def add_keyword_by_channel(self, channel_id: int, keyword: str) -> None:
        sql = """
            INSERT INTO keywords (channel_id, keyword)
            VALUES (%s, %s)
        """
        self.cursor.execute(sql, (channel_id, keyword))
        self.connection.commit()
        print(f"Keyword '{keyword}' added to channel ID '{channel_id}' successfully.")

    def change_keyword_by_channel(self, channel_id: int, old_keyword_id: int, new_keyword: str) -> None:
        sql = """
            UPDATE keywords
            SET keyword = %s
            WHERE id = %s AND channel_id = %s
        """
        self.cursor.execute(sql, (new_keyword, old_keyword_id, channel_id))
        self.connection.commit()

    def remove_keyword_by_channel(self, channel_id: int, keyword_id: int) -> None:
        sql = """
            DELETE FROM keywords
            WHERE channel_id = %s AND id = %s
        """
        self.cursor.execute(sql, (channel_id, keyword_id))
        self.connection.commit()

    def get_keywords_by_channel_id(self, channel_id: int) -> list:
        sql = """
            SELECT id, keyword
            FROM keywords
            WHERE channel_id = %s
        """
        self.cursor.execute(sql, (channel_id,))
        keywords = self.cursor.fetchall()
        return [{'id': keyword[0], 'name': keyword[1]} for keyword in keywords]

    def get_keywords(self) -> list:
        class ParsingKeyword(BaseModel):
            # класс-сборщик для менеджмента ключевых слов вместе с их каналами
            keyword_name: str
            keyword_id: int
            for_channel: str
            for_channel_id: int

        sql = """
            SELECT k.id, k.keyword, c.name, c.id
            FROM keywords k
            JOIN my_channels c ON k.channel_id = c.id
        """
        self.cursor.execute(sql)
        keywords = self.cursor.fetchall()

        # Формируем список объектов ParsingKeyword
        return [
            ParsingKeyword(
                keyword_name=keyword[1],
                keyword_id=keyword[0],
                for_channel=keyword[2],
                for_channel_id=keyword[3]
            )
            for keyword in keywords
        ]

    def get_keyword_name_by_id(self, keyword_id: int) -> dict:
        sql = """
            SELECT keyword
            FROM keywords
            WHERE id = %s
        """
        self.cursor.execute(sql, (keyword_id,))
        keyword = self.cursor.fetchone()
        return keyword[0]

