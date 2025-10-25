from typing import BinaryIO

from gigachat import GigaChat
import os
import logging
from dotenv import load_dotenv

# Safe token loading
load_dotenv()

# AI identifier
GIGACHAT_API_TOKEN = os.getenv("GIGACHAT_API_TOKEN")

# Logging settings
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Query parameters paths
CSV_PATH = "assets/films_processed_pico.csv"
PROMPT_PATH = "assets/prompt.txt"

class AICommunicator:
    """
    An entity that handles queries for and answers from the neural network service
    """
    output: str
    the_prompt: str
    priming_prompt: str
    format_prompt: str
    incapacity_prompt: str
    giga: GigaChat

    def __init__(self):
        self.output = ""

        with open(PROMPT_PATH, 'r', encoding='utf-8') as prompt_file:
            self.the_prompt = prompt_file.read()

        self.priming_prompt = """
Теперь оставь в памяти только базу данных и сообщение с правилами поиска. Ты получил на вход только их, а всё, что получал ранее, иррелевантно.
Снова найди и выведи 3 подходящих фильма так, как указано в сообщении с правилами поиска.
        """
        self.format_prompt = """
Ты нарушил формат вывода из сообщения с правилами поиска. Выведи найденные фильмы согласно формату. Всё, что нарушает формат, удали.
"""
        self.incapacity_prompt = """
Все или почти все фильмы, которые ты нашёл, слишком отличаются от предпочтений пользователя. Выполни поиск ещё раз согласно сообщению с правилами поиска.
"""
        self.giga = GigaChat(credentials=GIGACHAT_API_TOKEN, verify_ssl_certs=False)

    async def handle_ai_query(self, user_prefs: dict[str, str], first_time: bool=False):
        """
        Gets the preferences and returns the response
        """
        with open(CSV_PATH, 'rb') as db:
            try:
                # Converting the preferences into a list in a string
                user_prefs_list = []
                for entry, value in user_prefs.items():
                    user_prefs_list.append(entry + ': ' + value)
                updated_prompt = self.the_prompt + '\n\n' + '\n'.join(user_prefs_list) + '\n\nТвой ответ:'

                response = await self.do_ai_db_search(db, updated_prompt, first_time)
                return response

            except Exception as e:
                logger.error(f"Error processing message: {e}")
                return 'Error processing message'

    async def handle_additional_ai_query(self, sent_mistake: str):
        try:
            if sent_mistake == 'Priming':
                suitable_prompt = self.priming_prompt
            elif sent_mistake == 'Format ignoring':
                suitable_prompt = self.format_prompt
            elif sent_mistake == 'Incapacity':
                suitable_prompt = self.incapacity_prompt
            else:
                return 'Error processing message'
            response = await self.adjust_ai_answer(suitable_prompt)
            return response

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return 'Error processing message'

    async def do_ai_db_search(self, database: BinaryIO, text_prompt: str, first_time: bool=False):
        """
        Sends the database and the prompt, returns the AI response
        """
        try:
            # Loading a file to the AI (if not loaded yet) and acquiring its ID
            if first_time:
                self.giga.upload_file(database)
            file_id = self.giga.get_files().data[-1].id_

            # Making a request and returning the answer
            response = self.giga.chat(
                {
                    "function_call": "auto",
                    "messages": [
                        {
                            "role": "user",
                            "content": text_prompt,
                            "attachments": [file_id],
                        }
                    ],
                    "temperature": 0.1
                }
            )
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"GigaChat API error: {e}")
            return 'Error processing message'

    async def adjust_ai_answer(self, text_prompt: str):
        """
        Tries to make the AI correct itself
        """
        try:
            # Making a request and returning the answer
            response = self.giga.chat(
                {
                    "function_call": "auto",
                    "messages": [
                        {
                            "role": "user",
                            "content": text_prompt,
                        }
                    ],
                    "temperature": 0.1
                }
            )
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"GigaChat API error: {e}")
            return 'Error processing message'
