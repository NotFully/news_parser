import pymysql


from utils.config import host, user, password, dbname, port


class DB:
    def __init__(self):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=dbname,
            port=port
        )
        self.cursor = self.connection.cursor()

    def get_connection(self):
        return self.connection

    def create_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS my_channels (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    url_id BIGINT NOT NULL
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS keywords (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    channel_id INT NOT NULL,
                    keyword VARCHAR(255) NOT NULL,
                    FOREIGN KEY (channel_id) REFERENCES my_channels(id) ON DELETE CASCADE
                )
            """)

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS news (
                    new_id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    keyword VARCHAR(255) NOT NULL,
                    channel VARCHAR(255) NOT NULL,
                    link VARCHAR(255) NOT NULL
                )
            """)
            self.connection.commit()
            print("Tables created successfully.")
        except pymysql.Error as e:
            print(f"Error creating table: {e}")

