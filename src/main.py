
from telegram.ext import Updater, ConversationHandler
from botStates import WelcomeState, ShowImageState, States, Cancel

import logging, os

logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

TOKEN = os.getenv(
    "TOKEN", ""
)

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=WelcomeState().handlers,
        states={
            States.ShowImage: ShowImageState().handlers
        },
        fallbacks=Cancel().handlers,
        allow_reentry=True
    )

    dispatcher.add_handler(conv_handler)
    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
