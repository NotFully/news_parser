import pymysql
from pydantic import BaseModel

from utils.db.db import DB


class NewsItem(BaseModel):
	news_id: int
	title: str
	link: str
	keyword: str
	for_channel: str


class News:
	def __init__(self):
		db = DB()
		self.connection = db.get_connection()
		self.cursor = self.connection.cursor()

	def add_news(
			self,
			title: str,
			link: str,
			keyword: str,
			for_channel: str,
		) -> None:
		"""
		Записываем каждую подходящую новость в историю,
		чтобы потом получить её информацию после подтверждения модератора
		"""
		sql = """
		         INSERT INTO news (title, keyword, channel, link)
		         VALUES (%s, %s, %s, %s)
		     """
		self.cursor.execute(sql, (title, keyword, for_channel, link))
		self.connection.commit()

	def get_news(self, news_id: int) -> NewsItem | None:
		sql = """
		    SELECT id, title, link, keyword, channel 
		    FROM news
		    WHERE id = %s
		"""
		self.cursor.execute(sql, (news_id,))
		res = self.cursor.fetchone()

		if res:
			return NewsItem(
				news_id=res[0],
				title=res[1],
				link=res[2],
				keyword=res[3],
				for_channel=res[4]
			)
		else:
			return None

	def get_last_news_id(self):
		sql = "SELECT MAX(new_id) FROM news"
		self.cursor.execute(sql)
		result = self.cursor.fetchone()
		return result[0] if result[0] is not None else 0
