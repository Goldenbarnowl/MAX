import asyncio
import aiomax
from aiomax import Router, fsm, buttons
from config import bot

test_router = Router()

# -------------------- ДАННЫЕ --------------------
ST_QUESTIONS = ["1. Я спокоен", "2. Мне ничто не угрожает", "3. Я нахожусь в напряжении", "4. Я внутренне скован",
                "5. Я чувствую себя свободно", "6. Я расстроен", "7. Меня волнуют возможные неудачи",
                "8. Я ощущаю душевный покой", "9. Я встревожен", "10. Я испытываю чувство внутреннего удовлетворения",
                "11. Я уверен в себе", "12. Я нервничаю", "13. Я не нахожу себе места", "14. Я взвинчен",
                "15. Я не чувствую скованности, напряжённости", "16. Я доволен", "17. Я озабочен",
                "18. Я слишком возбуждён, и мне не по себе", "19. Мне радостно", "20. Мне приятно"]

LT_QUESTIONS = ["1. У меня бывает приподнятое настроение", "2. Я бываю раздражительным", "3. Я легко могу расстроиться",
                "4. Я хотел бы быть таким же удачливым, как и другие",
                "5. Я сильно переживаю неприятности и долго не могу о них забыть",
                "6. Я чувствую прилив сил, желание работать", "7. Я спокоен, хладнокровен и собран",
                "8. Меня тревожат возможные трудности", "9. Я слишком переживаю из-за пустяков",
                "10. Я бываю вполне счастлив", "11. Я всё принимаю близко к сердцу",
                "12. Мне не хватает уверенности в себе", "13. Я чувствую себя беззащитным",
                "14. Я стараюсь избегать критических ситуаций и трудностей", "15. У меня бывает хандра",
                "16. Я бываю доволен", "17. Всякие пустяки отвлекают и волнуют меня",
                "18. Бывает, что я чувствую себя неудачником", "19. Я уравновешенный человек",
                "20. Меня охватывает беспокойство, когда я думаю о своих делах и заботах"]

ANSWERS = ["1 – Нет, это не так / Никогда", "2 – Пожалуй, так / Почти никогда",
           "3 – Верно / Часто", "4 – Совершенно верно / Почти всегда"]

ST_KEY = [(4, 3, 2, 1), (4, 3, 2, 1), (1, 2, 3, 4), (1, 2, 3, 4), (4, 3, 2, 1), (1, 2, 3, 4), (1, 2, 3, 4),
          (4, 3, 2, 1), (1, 2, 3, 4), (4, 3, 2, 1), (4, 3, 2, 1), (1, 2, 3, 4), (1, 2, 3, 4), (1, 2, 3, 4),
          (4, 3, 2, 1), (4, 3, 2, 1), (1, 2, 3, 4), (1, 2, 3, 4), (4, 3, 2, 1), (4, 3, 2, 1)]

LT_KEY = [(4, 3, 2, 1), (1, 2, 3, 4), (1, 2, 3, 4), (1, 2, 3, 4), (1, 2, 3, 4), (4, 3, 2, 1), (4, 3, 2, 1),
          (1, 2, 3, 4), (1, 2, 3, 4), (4, 3, 2, 1), (1, 2, 3, 4), (1, 2, 3, 4), (1, 2, 3, 4), (1, 2, 3, 4),
          (1, 2, 3, 4), (4, 3, 2, 1), (1, 2, 3, 4), (1, 2, 3, 4), (4, 3, 2, 1), (1, 2, 3, 4)]

# -------------------- Клавиатура --------------------
def get_answers_kb(prefix: str):
    kb = buttons.KeyboardBuilder()
    for i, text in enumerate(ANSWERS, 1):
        kb.row(buttons.CallbackButton(text=text, payload=f"{prefix}_{i}"))
    return kb

# -------------------- СТАРТ ТЕСТА --------------------
@test_router.on_button_callback(aiomax.filters.equals("main_test"))
async def cmd_spilberger(callback: aiomax.Callback, cursor: fsm.FSMCursor):
    cursor.change_data({"st": [], "lt": []})

    await callback.send(
        text="Здорово, что вы решили лучше понять свое психологическое состояние!\n"
             "💡 Тестирование занимаете около 30-40 минут\n\n"
             "Отвечая на вопросы, попытайтесь сфокусироваться на своем эмоциональном "
             "и физическом состоянии за последние две недели.\n"
             "Прошу вас отвечать искренне, это очень важно для точности результатов"
    )

    await asyncio.sleep(2)

    await callback.send(
        text=f"🧠 **Тест**\n\n"
             f"Сейчас будет 20 вопросов про ваше **состояние прямо сейчас** (ситуативная тревожность).\n"
             f"Отвечайте честно и быстро.\n\n"
             f"Вопрос 1 из {len(ST_QUESTIONS)}\n\n"
             f"**{ST_QUESTIONS[0]}**",
        keyboard=get_answers_kb("st")
    )
    cursor.change_state('waiting_st_answer')

# -------------------- Обработка СТ --------------------
@test_router.on_button_callback(aiomax.filters.state('waiting_st_answer'))
async def process_st_answer(callback: aiomax.Callback, cursor: fsm.FSMCursor):
    if not callback.payload.startswith("st_"):
        return

    data = cursor.get_data()
    st_list = data.get("st", [])
    answer = int(callback.payload.split("_")[1])

    st_list.append(answer)
    data["st"] = st_list
    cursor.change_data(data)

    current_q = len(st_list)

    if current_q < len(ST_QUESTIONS):
        await bot.edit_message(
            message_id=callback.message.id,
            text=f"Вопрос {current_q + 1} из {len(ST_QUESTIONS)}\n\n"
                 f"**{ST_QUESTIONS[current_q]}**",
            keyboard=get_answers_kb("st")
        )
    else:
        await bot.edit_message(
            message_id=callback.message.id,
            text="Отлично! Первая часть завершена.\n\n"
                 "Теперь 20 вопросов про вас **в целом, как черту характера** (личностная тревожность).\n\n"
                 f"Вопрос 1 из {len(LT_QUESTIONS)}\n\n"
                 f"**{LT_QUESTIONS[0]}**",
            keyboard=get_answers_kb("lt")
        )
        cursor.change_state('waiting_lt_answer')

# -------------------- Обработка ЛТ --------------------
@test_router.on_button_callback(aiomax.filters.state('waiting_lt_answer'))
async def process_lt_answer(callback: aiomax.Callback, cursor: fsm.FSMCursor):
    if not callback.payload.startswith("lt_"):
        return

    data = cursor.get_data()
    lt_list = data.get("lt", [])
    answer = int(callback.payload.split("_")[1])

    lt_list.append(answer)
    data["lt"] = lt_list
    cursor.change_data(data)

    current_q = len(lt_list)

    if current_q < len(LT_QUESTIONS):
        await bot.edit_message(
            message_id=callback.message.id,
            text=f"Вопрос {current_q + 1} из {len(LT_QUESTIONS)}\n\n"
                 f"**{LT_QUESTIONS[current_q]}**",
            keyboard=get_answers_kb("lt")
        )
    else:
        st_answers = data.get("st", [])
        lt_answers = data.get("lt", [])

        st_score = sum(ST_KEY[i][ans - 1] for i, ans in enumerate(st_answers))
        lt_score = sum(LT_KEY[i][ans - 1] for i, ans in enumerate(lt_answers))

        def interpret(score: int) -> str:
            if score <= 30: return "низкая"
            elif score <= 44: return "умеренная"
            else: return "высокая"

        # Формируем тексты интерпретации
        if st_score <= 30:
            st_text = "В настоящий период времени для вас нехарактерно состояние тревоги. Ваша текущая жизненная ситуация является стабильной."
        elif st_score <= 44:
            st_text = "Актуальная жизненная ситуация может быть умеренно тревожной. Вы справляетесь с трудностями, но иногда чувствуете напряжение."
        else:
            st_text = "Вероятно, вы пребываете в стрессовой ситуации. Вы чувствуете себя встревоженным и неуверенным."

        if lt_score <= 30:
            lt_text = "Вы — нетревожный человек. Ситуации редко вызывают у вас сильное напряжение."
        elif lt_score <= 44:
            lt_text = "Вы достаточно уравновешены, но периодически беспокойство и волнение могут присутствовать."
        else:
            lt_text = "Тревожность — ваша устойчивая характеристика. Практически в любых условиях присутствует состояние напряженности."

        result_text = (
            "Предлагаю вам ознакомиться с общим заключением:\n\n"
            f"Ситуативная тревожность (СТ): **{st_score}** баллов → **{interpret(st_score)}**\n"
            f"{st_text}\n\n"
            f"Личностная тревожность (ЛТ): **{lt_score}** баллов → **{interpret(lt_score)}**\n\n"
            f"{lt_text}\n\n"
            "Интерпретация:\n"
            "• до 30 — низкая\n"
            "• 31–44 — умеренная\n"
            "• 45+ — высокая"
        )
        final = buttons.KeyboardBuilder()
        final.add(buttons.LinkButton(text="🚑 Связаться с психологом", url="https://max.ru/u/f9LHodD0cOLPoq8UJ_jqWBGvJpL2A9zo6Pv4A2aK4fmGXQzMKLyo2hBUK8o"))
        # Удаляем клавиатуру и выводим итог
        await bot.edit_message(message_id=callback.message.id, text=result_text, keyboard=final)

        from src.keyboards.user_keyboards import menu_keyboard_maker
        await callback.send(
            text="Тест завершён! Спасибо за ответы ❤️",
            keyboard=menu_keyboard_maker()
        )
        cursor.change_state('menu')