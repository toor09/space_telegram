import telegram

from settings import Settings


def main() -> None:
    """Publish text message to telegram channel."""
    settings = Settings()
    bot = telegram.Bot(token=settings.TG_BOT_TOKEN)
    bot.send_message(chat_id=settings.TG_CHAT_ID, text="Hello, world!")
    bot.send_document(
        chat_id=settings.TG_CHAT_ID,
        document=open("images/space_x_1.jpg", mode="rb")
    )


if __name__ == "__main__":
    main()
