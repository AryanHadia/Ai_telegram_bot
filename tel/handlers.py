from telegram import Update
from telegram.ext import ContextTypes
from T_LLM import Gemini as llm
import time
from collections import defaultdict

class BaseHandler:
    '''
    base handler for all handlers
    '''
    def __init__(self):
        self.llm = llm.LLM()
        self.user_data = defaultdict(lambda: {
            'message_count': 0,
            'first_time': 0,
            'last_message': '',
            'is_banned': False,
            'ban_until': 0
        })


class CmdHandler(BaseHandler):
    '''
    handle command update
    '''
    def __init__(self):
        super().__init__()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hi!! I'm Heshmat Masnoei. How can I help you today?")

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Helper text here...")
        await update.message.reply_text("1. /start: start the bot")
        await update.message.reply_text("2. /help: show this help text")
        await update.message.reply_text("3. Any other text: send it to the LLM for response")
        await update.message.reply_text("You're free to communicate with me in any language even Farsi!! just start sending messages.")


class MsgHandler(BaseHandler):
    '''
    handle message update
    '''
    def __init__(self):
        super().__init__()
        self.MESSAGE_LIMIT = 5
        self.TIME_WINDOW = 10  # seconds
        self.BAN_DURATION = 300  # 5 minutes

    async def check_spam(self, user_id: int, chat: str) -> bool:
        '''
        check if user is spamming based on message count in time window
        '''
        current_time = time.time()
        user_info = self.user_data[user_id]
        
        # if user is banned and ban time not expired
        if user_info['is_banned']:
            if current_time < user_info['ban_until']:
                return True
            else:
                user_info['is_banned'] = False
                user_info['message_count'] = 0
        
        # new time window started
        if current_time - user_info['first_time'] > self.TIME_WINDOW:
            user_info['first_time'] = current_time
            user_info['message_count'] = 1
            user_info['last_message'] = chat
            return False
        
        # increment message count
        user_info['message_count'] += 1
        user_info['last_message'] = chat
        
        # if user is spamming
        if user_info['message_count'] > self.MESSAGE_LIMIT:
            user_info['is_banned'] = True
            user_info['ban_until'] = current_time + self.BAN_DURATION
            return True
        
        return False

    async def chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        '''
        handle message update
        '''
        user = update.effective_user
        chat_id = update.message.chat_id
        user_id = user.id
        chat_text = update.message.text or ""
        
        # check if user is spamming
        is_spam = await self.check_spam(user_id, chat_text)
        
        if is_spam:
            try:
                # delete spam message
                await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
            except:
                pass
            
            # ban user for spamming
            try:
                until_date = int(time.time()) + self.BAN_DURATION
                await context.bot.ban_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    until_date=until_date
                )
                await update.message.reply_text(f"🚫 you have been banned for spamming for {self.BAN_DURATION//60} minutes!")
            except Exception as e:
                return 
            return
        
        # if user has no username
        if user.username is None:
            await update.message.reply_text("Please set your username first.")
            return
        
        # send message to the LLM for response
        try:
            response = self.llm.generate(prompt=chat_text)
            await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text(f"there was a problem processing your request :(")


class CbQueryHandler(BaseHandler):
    '''
    handle callback query update
    use for button click
    '''
    def __init__(self):
        super().__init__()

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(query.data)
