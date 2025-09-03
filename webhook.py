import asyncio
import logging
import sys

from app.bot import main_webhook

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(asctime)s - %(message)s",
        datefmt="%d-%m-%y %H:%M:%S"
    )

    main_webhook()
