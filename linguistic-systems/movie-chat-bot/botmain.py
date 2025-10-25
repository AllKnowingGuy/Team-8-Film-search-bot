from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, Application, filters
import os
import logging
import asyncio
from dotenv import load_dotenv

# Custom frontend functions
from botfront import launch_menu, ask_for_age, process_preference, process_menu_options, goodbye_and_finish, ask_if_mistaken

# Custom backend objects
from botback import PrefHandler
from botbackai import AICommunicator

# Safe token loading
load_dotenv()

# Bot identifier
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Logging settings
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Backend handlers
pref_handler = PrefHandler()
query_handler = AICommunicator()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Says hello and tells about the bot
    """
    # user_id = update.message.from_user.id
    hello_message = """
Привет! Что сегодня посмотрим?

Я - бот What2Watch, твой помощник в мире кино.
Учитывая твои интересы, я помогу подобрать фильмы именно для тебя!
У меня в запасе большая кинобаза, так что найдётся фильм на любой вкус!
\n
По твоим предпочтениям я формирую специальный запрос, который отправлю нейросети - она помогает мне искать фильмы по кинобазе.
Вообще я с ней в ладах, но иногда она выходит из-под контроля и выводит не то, что прошено.
Зато мы с тобой можем попросить её подкорректировать ответ!
    """
    await update.message.reply_text(hello_message, parse_mode='Markdown')
    await asyncio.sleep(5)

    # Frontend menu launch
    await update.message.reply_text('Но для начала мне нужно проверить кое-что.', parse_mode='Markdown')
    await asyncio.sleep(1)
    await ask_for_age(update, context)


async def call_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends the help message
    """
    help_message = """
Вот на какие команды я откликнусь:
/start – Начну работу
/help – Напишу тебе, на какие команды я откликнусь
    """
    await update.message.reply_text(help_message, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles all sorts of messages
    """
    user_id = update.effective_user.id
    user_message = update.message.text
    waiting_for = context.user_data.get('waiting_for')

    got_it_replies = [
        'Прочитал твоё сообщение. Ура, я умею читать!',
        'В этих словах... есть буквы! (надеюсь)',
        'Спасибо за сообщение! Когда-нибудь я пойму, что оно значит!'
    ]
    if waiting_for is None:
        await update.message.reply_text(got_it_replies[len(user_message) % 3], parse_mode='Markdown')
    elif waiting_for == 'menu_option':
        command = await process_menu_options(update, context)
        if command == 'Show preferences':
            message = pref_handler.tell_user_data(user_id)
            await update.message.reply_text(
                'Вот что ты мне успел(а) поведать. Я дам тебе время, чтобы ознакомиться со списком.\n\n'+message,
                parse_mode='Markdown',
                reply_markup=ReplyKeyboardRemove())
            await asyncio.sleep(5)
            await launch_menu(update, context)
        elif command == 'Launch the search':
            await launch_search(update, context, user_id)
    else:
        command = await process_preference(update, context)
        if command == 'Back to menu':
            await launch_menu(update, context)
        elif command == 'Save the answer':
            pref_handler.save_user_data(user_id, waiting_for, user_message)
            await asyncio.sleep(2)
            await launch_menu(update, context)
        elif command == 'Reset the answer':
            pref_handler.erase_user_data(user_id, waiting_for)
            await asyncio.sleep(2)
            await launch_menu(update, context)

        elif command == 'Priming' or command == 'Format ignoring' or command == 'Incapacity':
            await launch_extra_search(update, context, command)
        elif command is None and context.user_data.get('waiting_for') == 'mistake':
            await goodbye_and_finish(update, context)


async def launch_search(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id):
    """
    Follows the scenario of AI search
    """
    saved_prefs = pref_handler.return_user_data(user_id)
    if len(saved_prefs) == 0:
        await update.message.reply_text(
            'Похоже, ты мне не сообщил(а), что искать. Я не могу прийти к нейросети с пустыми руками!',
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(2)
        await launch_menu(update, context)
    else:
        await update.message.reply_text(
            'Запрос отправлен! Осталось только дождаться ответа...',
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardRemove())
        if context.user_data.get('sent_database') == 'true':
            response = await query_handler.handle_ai_query(saved_prefs)
        else:
            response = await query_handler.handle_ai_query(saved_prefs, first_time=True)
            if not response == 'Error processing message':
                context.user_data['sent_database'] = 'true'

        if response == 'Error processing message':
            await update.message.reply_text(
                """
К сожалению, что-то пошло не так, и я не смог связаться с нейросетью. Попробуем ещё разок?
Можешь на всякий случай подкорректировать свои предпочтения!
                """,
                parse_mode='Markdown',
                reply_markup=ReplyKeyboardRemove())
            await asyncio.sleep(2)
            await launch_menu(update, context)
        else:
            await update.message.reply_text(
                'Итак, вот что сообщила мне поисковая нейросеть:\n\n' + response,
                parse_mode='Markdown',
                reply_markup=ReplyKeyboardRemove())
            await asyncio.sleep(7)
            # await goodbye_and_finish(update, context)
            await ask_if_mistaken(update, context)


async def launch_extra_search(update: Update, context: ContextTypes.DEFAULT_TYPE, mistake):
    await update.message.reply_text(
        'Запрос отправлен на доработку! Осталось только дождаться ответа...',
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardRemove())
    response = await query_handler.handle_additional_ai_query(mistake)
    if response == 'Error processing message':
        await update.message.reply_text(
            """
К сожалению, что-то пошло не так, и я не смог связаться с нейросетью. Попробуем ещё разок?
Можешь на всякий случай подкорректировать свои предпочтения!
            """,
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(2)
        await launch_menu(update, context)
    else:
        await update.message.reply_text(
            'Итак, вот что сообщила мне поисковая нейросеть:\n\n' + response,
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(7)
        await ask_if_mistaken(update, context)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Error handler
    """
    logger.error(f"Update {update} caused error {context.error}")


def main() -> None:
    """
    Launch the bot
    """

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", call_help))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.add_error_handler(error_handler)

    application.run_polling() # And it starts


if __name__ == "__main__":
    main()
