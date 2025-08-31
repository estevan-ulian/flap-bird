from datetime import datetime
from src.dbproxy import DBProxy


class Score():
    def __init__(self):
        self.db_proxy = DBProxy('flap_score_database')

    def save(self, score):
        """ Save the score with the current date and time """
        self.db_proxy.save({"score": score, "date": self.get_formatted_date()})

    def show(self):
        """ Retrieve the top 3 scores """
        top3 = self.db_proxy.retrieve_top3()
        return top3

    def get_highest_score(self):
        """ Retrieve the highest score """
        return self.db_proxy.get_highest_score()

    def get_formatted_date(self):
        """ Get the current date and time formatted as HH:MM - DD/MM/YY """
        current_datetime = datetime.now()
        current_time = current_datetime.strftime("%H:%M")
        current_date = current_datetime.strftime("%d/%m/%y")
        return f"{current_time} - {current_date}"
