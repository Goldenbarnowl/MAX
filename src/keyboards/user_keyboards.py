from aiomax import buttons

# Словари переносим без изменений
slovar = {"hello": "Я согласен на обработку персональных данных 👋", "female": "👩 Женщина‍", "male": "👨 Мужчина",
"yes": "Да", "no": "Нет",
"buttonkey1": "👁 Тестирование", "buttonkey2": "💡 Курсы", "buttonkey3": "❓ Задайте вопрос", "buttonkey4": "❤️ О Нас",}
faqs = {"faq1": "Чем ты можешь мне помочь?", "faq2": "Это бесплатно?", "faq3": "Зачем нужно тестирование?"}
courses_slovar = {"course1": "Онлайн-курс «Терапия творчеством» ✨"}
faq_answers = {"faq1": """Со мной ты можешь:
лучше понять свое психологическое состояние, пройдя тестирование
получить рабочие рекомендации по проживаю стресса, способам самопомощи в сложных ситуациях
выбрать себе психолога или смежного специалиста
пройти онлайн-курсы для улучшения навыков совладания со стрессом""",
               "faq2": """Часть моих возможностей являются бесплатными! Некоторые разделы откроются благодаря ежемесячной подписке за небольшую стоимость.
Разработанные квалифицированными психологами онлайн-курсы также являются платными, но они содержат в себе обучающие материалы, которые позволят надолго закрепить навыки совладания со стрессом.""",
               "faq3": """Мое тестирование разработано квалифицированными специалистами, для которых вопрос стресса является ключевым в их практической и научной деятельности.
Прохождение теста позволит вам лучше понять ваше текущее состояние, а также сформировать наиболее подходящие рекомендации. Без тестирования персональные рекомендации сформировать не получится 🥺""",}


def kb_done(info):
    kb = buttons.KeyboardBuilder()
    kb.add(buttons.CallbackButton(text=slovar[info], payload="done"))
    return kb

def hello_button():
    kb = buttons.KeyboardBuilder()
    # ContactButton в aiomax заменяет request_contact=True
    kb.add(buttons.ContactButton(text=slovar["hello"]))
    return kb

def gender_keyboard_maker():
    kb = buttons.KeyboardBuilder()
    # В aiomax "инлайн" кнопки — это CallbackButton
    kb.add(buttons.CallbackButton(text=slovar["male"], payload="male"))
    kb.add(buttons.CallbackButton(text=slovar["female"], payload="female"))
    return kb

def yesorno_keyboard_maker():
    kb = buttons.KeyboardBuilder()
    # Обычные кнопки — это MessageButton
    kb.add(buttons.CallbackButton(text=slovar["yes"], payload="yes"))
    kb.add(buttons.CallbackButton(text=slovar["no"], payload="no"))
    return kb

def menu_keyboard_maker():
    kb = buttons.KeyboardBuilder()
    # Используем .row() для расположения кнопок друг под другом
    kb.row(buttons.MessageButton(text=slovar["buttonkey1"]))
    kb.row(buttons.MessageButton(text=slovar["buttonkey2"]))
    kb.row(buttons.MessageButton(text=slovar["buttonkey3"]))
    # WebAppButton для открытия мини-приложений
    kb.row(buttons.WebAppButton(
        text=slovar["buttonkey4"],
        bot="https://max.ru/id5501052552_bot"
    ))
    return kb

def faq_keyboard_maker():
    kb = buttons.KeyboardBuilder()
    for faq_id, faq_text in faqs.items():
        # Добавляем каждую кнопку в новый ряд
        kb.row(buttons.CallbackButton(text=faq_text, payload=faq_id))
    return kb

def courses_keyboard_maker():
    kb = buttons.KeyboardBuilder()
    for course_key, course_text in courses_slovar.items():
        kb.row(buttons.CallbackButton(text=course_text, payload=course_key))
    return kb

def main_test_keyboard_maker():
    kb = buttons.KeyboardBuilder()
    kb.add(buttons.CallbackButton(text="Начать тест", payload="main_test"))
    return kb

def payment_keyboard_maker():
    kb = buttons.KeyboardBuilder()
    kb.add(buttons.LinkButton(text="Оплатить", url="https://easyreels.payform.ru/?do=pay&sys=bothelp&callbackType=json&_param_cusid=505895&_param_pid=2&_param_cid=19399&urlNotification=https%3A%2F%2Fprodamus.bothelp.io%2Fsubscription&subscription=2437257&customer_phone=&customer_email=&customer_extra=Если+хотел%28а%29%2C+чтобы%3A%0A—+на+тебя+подписывалось+20-30+тыс.+целевой+аудитории+каждый+месяц%2C%0A—+выйти+на+стабильные+500%2B+тыс+руб+в+месяц+с+блога%2C%0A—+освоить+навык+монтажа+с+0+до+профи%2C%0A%0AДОБРО+ПОЖАЛОВАТЬ+В+КЛУБ+«РИЛС+СТАРТ».+%0AСтоимость+-+990₽%2Fмес.&urlReturn=https%3A%2F%2Fbothelp.cc%2Fmini%3Fdomain%3Dleramarkus%26id%3D3&urlSuccess=https%3A%2F%2Fbothelp.cc%2Fmini%3Fdomain%3Dleramarkus%26id%3D2&tg_user_id=820176381&signature=74bc38a9e84b9916f9f88baebdd4d02a1bc570072f1a718edc017d0d2e17fc26"))
    return kb