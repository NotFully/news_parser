import pymysql

from utils.db.db import DB
from utils.config import PASSWORD


class User:
	def __init__(self):
		db = DB()
		self.connection = db.get_connection()
		self.cursor = self.connection.cursor()

	def check_password(self, possible_password: str) -> bool:
		return possible_password == PASSWORD

	def add_user(self, user_id: int, username: str, ) -> None:
		try:
			sql = """
					INSERT INTO users (user_id, username) VALUES (%s, %s)
				"""
			self.cursor.execute(sql, (user_id, username))
			self.connection.commit()
		except pymysql.err.IntegrityError:
			pass

	def user_is_trusted(self, user_id: int) -> bool:
		try:
			sql = """
				SELECT COUNT(*) FROM users WHERE user_id = %s
			"""
			self.cursor.execute(sql, (user_id,))
			result = self.cursor.fetchone()

			return result[0] > 0
		except Exception as e:
			print(f"Error checking if user is trusted: {e}")
			return False

	def get_first_trusted_user(self) -> int:
		try:
			sql = """
			    SELECT user_id FROM users
			"""
			self.cursor.execute(sql)
			result = self.cursor.fetchall()
			if result:
				list_user = []

				if result != ():
					for i in result:
						list_user.append(i[0])

				return list_user
		except TypeError:
			raise TypeError('Ошибка: не одного модератора не найдено :(')


