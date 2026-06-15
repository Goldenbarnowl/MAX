import asyncio
import re

import aiomax
from aiomax import Router, fsm, ContactAttachment, Message

from config import bot
from src.aiomax_fix.contact_attachment_class_fix import fixed_from_json
from src.keyboards.user_keyboards import (
    hello_button,
    gender_keyboard_maker,
    yesorno_keyboard_maker, kb_done, menu_keyboard_maker, faq_keyboard_maker, slovar, faq_answers,
    payment_keyboard_maker
)
from src.texts import HELLO, INFO

main_router = Router()


# --- СТАРТ ---
@main_router.on_command("start")
@main_router.on_bot_start()
async def start(payload: aiomax.BotStartPayload, cursor: fsm.FSMCursor):

    doc_attachment = await bot.upload_video(r"src/media/maskot.gif")
    await payload.send(
        text=HELLO,
        attachments=[doc_attachment]
    )

    await asyncio.sleep(1)

    doc_file = await bot.upload_file(r"src/media/Политика конфиденциальности.docx.pdf")
    await payload.send(
        text="Политика конфиденциальности:",
        attachments=[doc_file]
    )

    await payload.send(
        text=INFO,
        keyboard=hello_button()
    )
    cursor.change_state('wait_phone_number')



# --- ОБРАБОТКА КОНТАКТА ---
@main_router.on_message(aiomax.filters.state('wait_phone_number'))
async def handle_contact(message: aiomax.Message, cursor: fsm.FSMCursor):
    ContactAttachment.from_json = staticmethod(fixed_from_json)

    if not message.body.attachments or not isinstance(message.body.attachments[0], ContactAttachment):
        await message.send("Нажмите на кнопку внизу экрана для общения со мной")
        return

    contact = message.body.attachments[0]
    vcard_data = str(contact.vcf_info)
    match = re.search(r"TEL;?.*:([\d+]+)", vcard_data)

    if match:
        phone = match.group(1)
        cursor.change_data({"phone": phone})

        await message.send(
            text="Расскажите немного о себе",
            keyboard=None
        )
        await message.send(
            text="Кто вы?\nИспользуйте кнопки внизу сообщения для выбора ответа:",
            keyboard=gender_keyboard_maker()
        )
        cursor.change_state('gender')

# --- ВЫБОР ПОЛА (Inline/Callback) ---
@main_router.on_button_callback(aiomax.filters.state('gender'))
async def gender_choice(callback: aiomax.Callback, cursor: fsm.FSMCursor):

    await bot.edit_message(
        message_id=callback.message.id,
        keyboard=kb_done(callback.payload)
    )

    if callback.payload == "female":
        cursor.change_data({"gender": "Женский"})
        text = ("Знаете, я заметил одну вещь 🤔 женщины в разном возрасте переживают стресс совсем по-разному.\n"
                "Поэтому мне очень важно знать — на каком вы сейчас жизненном этапе?\n\n"
                "Напишите в сообщении сколько вам лет:")
    else:
        cursor.change_data({"gender": "Мужской"})
        text = ("Мужчины редко признаются, что им тяжело, поэтому то, что ты здесь — уже большой шаг.\n"
                "Поэтому мне очень важно знать — в каком вы сейчас жизненном этапе?\n\n"
                "Напишите в сообщении сколько вам лет:")


    await callback.send(text=text)
    cursor.change_state('age')


# --- ОБРАБОТКА ВОЗРАСТА ---
@main_router.on_message(aiomax.filters.state('age'))
async def process_age(message: aiomax.Message, cursor: fsm.FSMCursor):
    # Проверка: является ли текст числом
    if not message.body.text or not message.body.text.isdigit():
        await message.send(
            text="Не понял. Напишите цифрами в сообщении сколько вам лет, например, 23."
        )
        return

    age_val = int(message.body.text)

    # Валидация возраста
    if age_val < 12:
        await message.send(text="Вам должно быть 12 лет или больше. Попробуйте ещё раз:")
        return
    elif age_val > 100:
        await message.send(text="Вам должно быть меньше 100 лет. Попробуйте ещё раз:")
        return

    cursor.change_data({"age": age_val})


    text_swo = (
        "Ещё один маленький, но важный вопрос…\n\n"
        "Сейчас многие живут с тяжёлым чувством, когда близкий человек на передовой. "
        "И знаю, как сильно это влияет на сон, нервы, силы…\n\n"
        "Можешь не рассказывать подробностей — просто скажи, есть ли у тебя сейчас такой человек среди родных или самых близких?"
    )

    await message.send(
        text=text_swo,
        keyboard=yesorno_keyboard_maker()
    )
    cursor.change_state('swo_family')


# --- ЗАВЕРШЕНИЕ РЕГИСТРАЦИИ И ГЛАВНОЕ МЕНЮ ---
@main_router.on_button_callback(aiomax.filters.state('swo_family'))
async def finish_registration(callback: aiomax.Callback, cursor: fsm.FSMCursor):

    cursor.change_data({"swo_family": callback.payload})

    await bot.edit_message(
        message_id=callback.message.id,
        keyboard=kb_done(callback.payload)
    )

    await callback.send(
        text= "Крепко обнимаю ❤️‍🩹\n"
        "Внизу кнопки — тут ты можешь пройти психологический тест, задать мне любой вопрос, "
        "получить техники или найти специалиста.\n"
        "Выбирай, что нужно прямо сейчас:",
        keyboard=menu_keyboard_maker()
    )
    cursor.change_state('menu')

# --- МЕНЮ ПОВТОР ---
@main_router.on_command("menu")
async def menu(message: Message, cursor: fsm.FSMCursor):
    if cursor.get_state() == "menu":
        await message.send(
            text="Крепко обнимаю ❤️‍🩹\n"
                 "Внизу кнопки — тут ты можешь пройти психологический тест, задать мне любой вопрос, "
                 "получить техники или найти специалиста.\n"
                 "Выбирай, что нужно прямо сейчас:",
            keyboard=menu_keyboard_maker()
        )
        cursor.change_state('menu')

# --- КУРСЫ ---
@main_router.on_message(aiomax.filters.state('menu') and aiomax.filters.equals(slovar["buttonkey2"]))
async def courses(message: aiomax.Message, cursor: fsm.FSMCursor):
    doc_attachment = await bot.upload_image((r"src/media/course1.jpg"))
    await message.send(
        text="""Онлайн-курс повышения квалификации «Терапия творчеством» ✨

    Что вы получите:

    Обновите и упорядочите свои знания в консультировании и тренинговой работе 📚
    Освоите авторские методики терапии творчеством — проверенные, живые, работающие на 100% 🔥
    Научитесь быстро и экологично снимать стресс, тревогу и эмоциональные блоки через творчество 🎨
    Добавите в свою копилку крутые инструменты самопомощи, которыми можно пользоваться каждый день 🌟
            """,
        attachments=[doc_attachment],
    )
    await message.send(
        text="""Вы погрузитесь в волшебные методы:

    Терапия творческим самовыражением ✍️
    Эмоционально-образная терапия (ЭОТ) ❤️
    Кинотерапия 🍿
    Создание терапевтических метафор с юмором и лёгкостью 😄 

    Ведут курс — потрясающие авторы и разработчики программы:
    👩‍🏫 Грушко Наталья Владимировна — руководитель программы, к.п.н., доцент
    👩‍🏫 Карловская Наталья Николаевна — к.п.н., доцент
    👩‍🏫 Козлова Дарья Евгеньевна — старший преподаватель
    👩‍🏫 Динкелакер Людмила Александровна — старший преподаватель
    Кафедра общей и социальной психологии ❤️
    После курса вы уйдёте с целым чемоданом новых идей, тёплым сердцем и уверенностью, что помогать можно легко и с улыбкой 🌈
    Ждём именно вас! 🚀""",
        keyboard=payment_keyboard_maker()
    )



# --- ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ (Текст) ---
@main_router.on_message(aiomax.filters.state('menu') and aiomax.filters.equals(slovar["buttonkey3"]))
async def faq(message: aiomax.Message, cursor: fsm.FSMCursor):
    await message.send(
        text=("Часто задаваемые вопросы ❤️\n\n"
              "Тыкайте на любой вопрос ниже — я сразу подробно отвечу.\n"),
        keyboard=faq_keyboard_maker()
    )


# --- ОТВЕТЫ НА FAQ (Callback) ---
@main_router.on_button_callback(aiomax.filters.state('menu') )
async def faq_answers_handler(callback: aiomax.Callback, cursor: fsm.FSMCursor):
    # faq_answers — это ваш словарь {callback_data: "текст ответа"}
    # Проверяем, есть ли payload кнопки в ключах нашего словаря ответов
    if callback.payload in faq_answers:
        await callback.send(
            text=faq_answers[callback.payload]
        )
    # Если используются другие колбэки в этом состоянии,
    # здесь можно добавить блоки elif или просто пропустить


# --- ВЫЗОВ ТЕСТА ИЗ МЕНЮ ---
@main_router.on_message(aiomax.filters.state('menu') and aiomax.filters.equals(slovar["buttonkey1"]))
async def start_test_info(message: aiomax.Message, cursor: fsm.FSMCursor):
    # Текст описания теста
    text_info = (
        "Благодаря опросу я смогу понять, как вы чувствуете себя и насколько силен ваш стресс.\n"
        "После его прохождения вас ожидает:\n"
        "- психологическое заключение, основанное на результатах\n"
        "- рекомендации для самопомощи, к выполнению которых вы можете приступить уже сегодня\n"
        " ❤️"
    )

    from src.keyboards.user_keyboards import main_test_keyboard_maker  # Импорт вашей функции

    await message.send(
        text=text_info,
        keyboard=main_test_keyboard_maker()
    )
