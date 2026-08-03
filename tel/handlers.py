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

    async def help(self, update: Update):
        await update.message.reply_text("helper")


class MsgHandler(BaseHandler):
    '''
    handle message update
    '''
    def __init__(self):
        pass 


    def LLM(self, chat: str):
        return chat


    async def chat(self, update: Update):
        await update.message.reply_text(update.message.text)


class CbQueryHandler(BaseHandler):
    '''
    handle callback query update
    use for button click
    '''
    def __init__(self):
        pass

    async def button(self, update: Update):
        await update.callback_query.message.edit_text(update.callback_query.data)
