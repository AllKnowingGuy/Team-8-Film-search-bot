from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ContextTypes
import asyncio


async def launch_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Opens a menu of buttons to select necessary preferences
    """
    last_user_message = update.message.text
    has_visited = context.user_data.get('has_visited_menu')

    keyboard = [
        [KeyboardButton("🔤Название"), KeyboardButton("🎭Жанр"), KeyboardButton("🌍Страна")],
        [KeyboardButton("⌛Год"), KeyboardButton("🏆Рейтинг"), KeyboardButton("🔞Возраст")],
        [KeyboardButton("🎈Ключевые слова🦇"), KeyboardButton("😊Настроение😔")],
        [KeyboardButton("📋 Проверить предпочтения 📋")],
        [KeyboardButton("🔍 - Искать! - 🔍")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    menu_greetings_messages = [
        'Рад снова видеть тебя в меню!',
        'Хочешь ещё что-нибудь сообщить о фильме?',
        'Информация о фильме - моя пища. Но не перекорми!',
        'Добро пожаловать в меню! Видишь кнопки категорий под полем ввода?'
    ]

    menu_message = """
Выбери категорию, чтобы указать предпочтения по ней.
Написал(а) не то или нажал(а) не ту кнопку? Просто вернись и исправь!

Когда укажешь всё, что важно, смело нажимай "Искать!"
    """

    if has_visited is None:
        await update.message.reply_text(
            menu_greetings_messages[-1] + '\n' + menu_message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        context.user_data['has_visited_menu'] = 'true'
    else:
        await update.message.reply_text(
            menu_greetings_messages[len(last_user_message) % 3] + '\n' + menu_message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    context.user_data['waiting_for'] = 'menu_option'


async def ask_if_knows_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Description
    """
    keyboard = [
        [KeyboardButton("Точно"),KeyboardButton("Примерно")],
        [KeyboardButton("Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    title_message = """
Насколько точно ты знаешь название фильма?
    """
    await update.message.reply_text(title_message, parse_mode='Markdown', reply_markup=reply_markup)
    context.user_data['waiting_for'] = 'type_of_title'


async def ask_for_precise_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Description
    """
    keyboard = [
        [KeyboardButton("Сбросить ответ")],
        [KeyboardButton("Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    title_message = """
Введи же это название:
    """
    await update.message.reply_text(title_message, parse_mode='Markdown', reply_markup=reply_markup)
    context.user_data['waiting_for'] = 'precise_title'


async def ask_for_approximate_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Description
    """
    keyboard = [
        [KeyboardButton("Сбросить ответ")],
        [KeyboardButton("Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    title_message = """
Тогда введи слова из названия, которые помнишь:
    """
    await update.message.reply_text(title_message, parse_mode='Markdown', reply_markup=reply_markup)
    context.user_data['waiting_for'] = 'approximate_title'


async def ask_for_genre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Asks to enter or pick the genre
    """
    keyboard = [
        [KeyboardButton("Комедия"), KeyboardButton("Драма")],
        [KeyboardButton("Фантастика"), KeyboardButton("Хоррор")],
        [KeyboardButton("Сбросить ответ")],
        [KeyboardButton("Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    genre_message = """
Какой жанр должен быть у твоего фильма? Выбери с помощью кнопок или введи свой:
    """
    await update.message.reply_text(genre_message, parse_mode='Markdown', reply_markup=reply_markup)
    context.user_data['waiting_for'] = 'genre'


async def ask_for_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Asks to enter or pick the country of filming
    """
    keyboard = [
        [KeyboardButton("США"), KeyboardButton("Франция")],
        [KeyboardButton("Россия"), KeyboardButton("Япония")],
        [KeyboardButton("Великобритания"), KeyboardButton("Индия")],
        [KeyboardButton("Сбросить ответ")],
        [KeyboardButton("Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    genre_message = """
В какой же стране был снят тот самый фильм? Назови её в сообщении или выбери кнопкой:
    """
    await update.message.reply_text(genre_message, parse_mode='Markdown', reply_markup=reply_markup)
    context.user_data['waiting_for'] = 'country'


async def ask_if_precise_year(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Description
    """
    keyboard = [
        [KeyboardButton("Точный год"), KeyboardButton("Год в промежутке")],
        [KeyboardButton("Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    year_message = """
Важен ли тебе точный год, или он просто должен попасть в некий промежуток?
    """
    await update.message.reply_text(year_message, parse_mode='Markdown', reply_markup=reply_markup)
    context.user_data['waiting_for'] = 'type_of_year'


async def ask_for_precise_year(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Description
    """
    keyboard = [
        [KeyboardButton("Сбросить ответ")],
        [KeyboardButton("Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    year_message = """
Тогда введи этот год (только 4-значное число):
    """
    await update.message.reply_text(year_message, parse_mode='Markdown', reply_markup=reply_markup)
    context.user_data['waiting_for'] = 'precise_year'


async def ask_for_year_span(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Description
    """
    keyboard = [
        [KeyboardButton("Сбросить ответ")],
        [KeyboardButton("Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    year_message = """
Тогда введи этот промежуток (два 4-значных числа, разделённые дефисом, например, 1950-2000)
    """
    await update.message.reply_text(year_message, parse_mode='Markdown', reply_markup=reply_markup)
    context.user_data['waiting_for'] = 'year_span'


async def ask_for_minimum_imdb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Asks to enter the minimum IMDB rating
    """
    keyboard = [
        [KeyboardButton("Сбросить ответ")],
        [KeyboardButton("Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    rating_message = """
Рейтинг фильма - это важно! Укажи минимальный балл по IMDB для твоего фильма, и я найду такие, у которых балл выше!

Введи рейтинг - целое или дробное число от 0 до 10 (в дробном числе только целые и десятые, разделённые ТОЧКОЙ, например, 8.7):
    """
    await update.message.reply_text(rating_message, parse_mode='Markdown', reply_markup=reply_markup)
    context.user_data['waiting_for'] = 'minimum_IMDB'


async def ask_for_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Asks to enter the age
    """
    keyboard = [
        [KeyboardButton("Сбросить ответ")],
        [KeyboardButton("Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    age_message = """
    Я знаю фильмы, которые тебе могут не подойти, если ты слишком молод(а). Чтобы я случайно их не предложил, укажи свой возраст (я буду держать его в секрете, обещаю!)

Введи возраст - только число:
    """
    await update.message.reply_text(age_message, parse_mode='Markdown', reply_markup=reply_markup)
    context.user_data['waiting_for'] = 'age'


async def ask_for_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Asks to enter the keywords
    """
    keyboard = [
        [KeyboardButton("Сбросить ответ")],
        [KeyboardButton("Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    keywords_message = """
    Результат будет ещё точнее, если ты расскажешь, кто или что должно быть в фильме. Назови мне любые ключевые слова для поиска, но не переусердствуй!

Введи нужные слова через пробел:
    """
    await update.message.reply_text(keywords_message, parse_mode='Markdown', reply_markup=reply_markup)
    context.user_data['waiting_for'] = 'keywords'


async def ask_for_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Description
    """
    keyboard = [
        [KeyboardButton("Сбросить ответ")],
        [KeyboardButton("Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    mood_message = """
Я подберу такой фильм, который максимально подходит под твоё текущее настроение! Скажи, какое оно у тебя?
    """
    await update.message.reply_text(mood_message, parse_mode='Markdown', reply_markup=reply_markup)
    context.user_data['waiting_for'] = 'mood'


async def process_menu_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str | None:
    """
    Receives and processes a chosen menu option
    """
    chosen_option = update.message.text
    if chosen_option == "🔤Название":
        await ask_if_knows_title(update, context)
    elif chosen_option == "🎭Жанр":
        await ask_for_genre(update, context)
    elif chosen_option == "🌍Страна":
        await ask_for_country(update, context)
    elif chosen_option == "⌛Год":
        await ask_if_precise_year(update, context)
    elif chosen_option == "🏆Рейтинг":
        await ask_for_minimum_imdb(update, context)
    elif chosen_option == "🔞Возраст":
        await ask_for_age(update, context)
    elif chosen_option == "🎈Ключевые слова🦇":
        await ask_for_keywords(update, context)
    elif chosen_option == "😊Настроение😔":
        await ask_for_mood(update, context)
    elif chosen_option == "📋 Проверить предпочтения 📋":
        return 'Show preferences'
    elif chosen_option == "🔍 - Искать! - 🔍":
        return 'Launch the search'
    else:
        await update.message.reply_text('Кажется, такой кнопки у меня нет. Попробуй другую!', parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(2)
        await launch_menu(update, context)


async def process_preference(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str | None:
    """
    Receives and processes different types of chosen preferences
    """
    # user_id = update.effective_user.id
    user_message = update.message.text
    waiting_for = context.user_data.get('waiting_for')

    # Special actions with returns for special buttons
    if user_message == 'Назад':
        return 'Back to menu'
    elif user_message == 'Сбросить ответ':
        await update.message.reply_text(
            'Сбросил это предпочтение. Не переживай, ты можешь ввести его снова!',
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardRemove())
        return 'Reset the answer'

    # Name routes
    if waiting_for == 'type_of_title':
        if user_message == 'Точно':
            await ask_for_precise_title(update, context)
        elif user_message == 'Примерно':
            await ask_for_approximate_title(update, context)

    # Year routes
    elif waiting_for == 'type_of_year':
        if user_message == 'Точный год':
            await ask_for_precise_year(update, context)
        elif user_message == 'Год в промежутке':
            await ask_for_year_span(update, context)

    # AI mistake correction
    elif waiting_for == 'mistake':
        if user_message == 'Всё в порядке/Пойдёт и так':
            await goodbye_and_finish(update, context)
            return None
        elif user_message == 'Нейросеть отвечает по старым данным':
            return 'Priming'
        elif user_message == 'Нейросеть говорит слишком много лишнего':
            return 'Format ignoring'
        elif user_message == 'Нейросеть выводит явно неподходящую информацию':
            return 'Incapacity'

    # Generic reception and saving
    else:
        if waiting_for == 'precise_title':
            await update.message.reply_text(
                'Интересное название, запомнил!',
                parse_mode='Markdown',
                reply_markup=ReplyKeyboardRemove())
        elif waiting_for == 'approximate_title':
            await update.message.reply_text(
                'Спасибо за слова, постараюсь собрать из них название!',
                parse_mode='Markdown',
                reply_markup=ReplyKeyboardRemove())
        elif waiting_for == 'genre':
            await update.message.reply_text(
                'Такой жанр мы одобряем!',
                parse_mode='Markdown',
                reply_markup=ReplyKeyboardRemove())
        elif waiting_for == 'country':
            await update.message.reply_text(
                'А ты ценитель киноиндустрии этой страны!',
                parse_mode='Markdown',
                reply_markup=ReplyKeyboardRemove())
        elif waiting_for == 'precise_year':
            await update.message.reply_text(
                'Пойду погляжу архивы за этот год)',
                parse_mode='Markdown',
                reply_markup=ReplyKeyboardRemove())
        elif waiting_for == 'year_span':
            await update.message.reply_text(
                'Запомнил: год фильма будет в этом промежутке!',
                parse_mode='Markdown',
                reply_markup=ReplyKeyboardRemove())
        elif waiting_for == 'minimum_IMDB':
            await update.message.reply_text(
                'Я и не такие ожидания видал)',
                parse_mode='Markdown',
                reply_markup=ReplyKeyboardRemove())
        elif waiting_for == 'age':
            await update.message.reply_text(
                'Спасибо! ',
                parse_mode='Markdown',
                reply_markup=ReplyKeyboardRemove())
        elif waiting_for == 'keywords':
            await update.message.reply_text(
                'Получил ключевые слова, спасибо!',
                parse_mode='Markdown',
                reply_markup=ReplyKeyboardRemove())
        elif waiting_for == 'mood':
            await update.message.reply_text(
                'Настрой понятен, спасибо!',
                parse_mode='Markdown',
                reply_markup=ReplyKeyboardRemove())
        return 'Save the answer'


async def ask_if_mistaken(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Asks if the AI answer needs to be corrected
    """
    keyboard = [
        [KeyboardButton("Всё в порядке/Пойдёт и так")],
        [KeyboardButton("Нейросеть отвечает по старым данным")],
        [KeyboardButton("Нейросеть говорит слишком много лишнего")],
        [KeyboardButton("Нейросеть выводит явно неподходящую информацию")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    mistake_message = """
Тебе подходит такой ответ?
Если в нём есть проблема, нажми на подходящую кнопку.
Если проблем нет или она несущественная, выбери "Всё в порядке/Пойдёт и так".
        """
    await update.message.reply_text(mistake_message, parse_mode='Markdown', reply_markup=reply_markup)
    context.user_data['waiting_for'] = 'mistake'


async def goodbye_and_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Finishes the work
    """
    last_message = """
    Тогда я завершаю работу!

Рад был пройти это небольшое приключение вместе с тобой! Оно помогло мне стать чуточку лучше!

Если захочешь позвать меня на поиск нового фильма - просто введи /start!
    """
    await update.message.reply_text(
        last_message,
        parse_mode='Markdown'
    )
    context.user_data['has_visited_menu'] = None
    context.user_data['waiting_for'] = None
    context.user_data['sent_database'] = None

