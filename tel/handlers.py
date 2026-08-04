from telegram import Update
from telegram.ext import ContextTypes


class BaseHandler:
    '''
    base handler for all handlers
    '''
    def __init__(self):
        self.llm = None
        self.data_base = None


class CmdHandler(BaseHandler):
    '''
    handle command update
    '''
    def __init__(self):
        pass

    async def start(self, update: Update , context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("I'm a bot, please talk to me!")

    async def help(self, update: Update , context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("helper")


class MsgHandler(BaseHandler):
    '''
    handle message update
    '''
    def __init__(self):
        pass 


    def llm(self , chat=None): # getting chat from bot and giving it to the llm model
        if chat is None:
            print('chat is None')
            return None
        response = self.llm.generate(chat)
        return response


    async def chat(self, update: Update , context: ContextTypes.DEFAULT_TYPE):
        chat = update.message.text
        response = self.llm(chat)
        await update.message.reply_text(response)


class CbQueryHandler(BaseHandler):
    '''
    handle callback query update
    use for button click
    '''
    def __init__(self):
        pass

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.message.edit_text(update.callback_query.data)
