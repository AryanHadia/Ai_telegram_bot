import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from handlers import CmdHandler, MsgHandler, CbQueryHandler
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
        )


class Bot:
    '''
    bot class
    '''
    
    def __init__(self):
        self.cmd_handler = CmdHandler()
        self.msg_handler = MsgHandler()
        self.cb_query_handler = CbQueryHandler()
        token = os.getenv('bot_token')
        if not token:
            raise ValueError("bot_token environment variable is not set")
        self.application = ApplicationBuilder().token(token).build()
        self.start_handler = CommandHandler('start', self.cmd_handler.start)
        self.help_handler = CommandHandler('help', self.cmd_handler.help)
        self.message_handler = MessageHandler(filters.TEXT, self.msg_handler.chat)
        self.callback_query_handler = CallbackQueryHandler(self.cb_query_handler.button)
        self.application.add_handler(self.start_handler)
        self.application.add_handler(self.help_handler)
        self.application.add_handler(self.message_handler)
        self.application.add_handler(self.callback_query_handler)
        
    def run(self):
        '''
        run bot
        '''
        try:
            self.application.run_polling() # the main loop of bot
        except Exception as e:
            logging.error(f"Error in run: {e}")


if __name__ == '__main__':
    bot = Bot()
    bot.run()
