import logging

from aiomax.buttons import CallbackButton

from config import bot
from src.routers.test_router import test_router
from src.routers.user_routers import main_router

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(name)s:%(funcName)s:%(lineno)d → %(message)s',
    )


def main():
    setup_logging()

    bot.add_router(main_router)
    bot.add_router(test_router)

    logging.info("Запуск бота...")
    bot.run()

def patch_aiomax_callback_button():
    @staticmethod
    def from_json(data: dict) -> CallbackButton:
        return CallbackButton(
            data["text"],
            data["payload"],
            data.get("intent", "default")
        )

    CallbackButton.from_json = from_json


if __name__ == '__main__':
    patch_aiomax_callback_button()
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен!")