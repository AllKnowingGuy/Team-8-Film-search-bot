class PrefHandler:
    """
    An entity that holds and handles the preference list (which is actually a dict)
    """
    pl: dict[int, dict[str, str]]
    key_locales: dict[str, str]
    def __init__(self):
        self.pl = {}
        self.key_locales = {
            'precise_title': 'Точное название',
            'approximate_title': 'Слова в названии',
            'genre': 'Жанр',
            'country': 'Страна',
            'precise_year': 'Год создания',
            'year_span': 'Год создания в промежутке',
            'minimum_IMDB': 'Минимальный рейтинг',
            'age': 'Ваш возраст',
            'keywords': 'Ключевые слова',
            'mood': 'Ваше настроение',
        }

    def save_user_data(self, user_id: int, question: str, answer: str):
        if user_id not in self.pl:
            self.pl[user_id] = {}
        self.pl[user_id][question] = answer

    def erase_user_data(self, user_id: int, question: str):
        if user_id not in self.pl:
            self.pl[user_id] = {}
        if question in self.pl[user_id]:
            self.pl[user_id].pop(question)

    def return_user_data(self, user_id: int) -> dict[str, str]:
        if user_id in self.pl:
            return self.pl[user_id]
        return {}

    def tell_user_data(self, user_id: int) -> str:
        out_list = []
        if user_id in self.pl:
            for entry, value in self.return_user_data(user_id).items():
                out_list.append(self.key_locales[entry]+': '+value)
        return '\n'.join(out_list)
