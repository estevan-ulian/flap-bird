import sqlite3


class DBProxy:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.table_name = 'game_data'
        self.connection = sqlite3.connect(self.db_name)
        self.connection.execute(f'''
                                  CREATE TABLE IF NOT EXISTS {self.table_name}(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    score INTEGER NOT NULL,
                                    date TEXT NOT NULL
                                  )
                                ''')

    def save(self, score_dict: dict):
        """ Save a score dictionary to the database """
        self.connection.execute(
            f'INSERT INTO {self.table_name} (score, date) VALUES (:score, :date)', score_dict)
        self.connection.commit()

    def retrieve_top3(self) -> list:
        """ Retrieve the top 3 scores from the database """
        result = self.connection.execute(
            f'SELECT * FROM {self.table_name} ORDER BY score DESC LIMIT 3').fetchall()
        return result

    def get_highest_score(self) -> int:
        """ Retrieve the highest score from the database """
        result = self.connection.execute(
            f'SELECT MAX(score) FROM {self.table_name}').fetchone()

        return result[0] if result[0] is not None else 0
