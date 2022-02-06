from enum import Enum
from telegram import InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, MessageHandler, Filters, CommandHandler, ConversationHandler

from Services.FrameXService import FrameXService, VideoInfoResponse

class States(str, Enum):
    Welcome = 'WELCOME'
    ShowImage = 'SHOWIMAGE'
    Cancel = 'CANCEL'

class BisectObj:
    low: int
    high: int
    midpoint: int

class WelcomeState:

    def __init__(self):
        self.handlers = [CommandHandler('start', self.welcome)]
        
    def welcome(self, update: Update, context: CallbackContext):
        keyboard = [
            ['Lets go']
        ]

        update.message.reply_text(
            'We will be showing you frames from a rocket launch video to help us find the moment of launch.Are you ready?',
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        )

        restartContext(context)

        return States.ShowImage
    

class ShowImageState:

    def __init__(self):
        self.handlers = [MessageHandler(Filters.regex('^(Yes|No|Lets go)$') & ~Filters.command, self.question)]
    
    def question(self, update: Update, context: CallbackContext):
        bisectObj = context.user_data.get('bisectObj')

        if(update.message.text == 'Yes'):
            bisectObj = bisectStep(bisectObj, -1)

        elif(update.message.text == 'No'):
            bisectObj = bisectStep(bisectObj, 1)

        context.user_data['bisectObj'] = bisectObj

        rocketImage = FrameXService.getFrame(bisectObj['midpoint'])

        update.message.reply_photo(rocketImage)

        if(bisectObj['high'] - bisectObj['low'] < 200):
            update.message.reply_text(
                'Image found, thank you'
                )

            return ConversationHandler.END

        keyboard = [
            ['Yes', 'No']
        ]

        update.message.reply_text(
            '''Did the rocket launch yet?''',
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        )

        return States.ShowImage
    
class Cancel:
    def __init__(self):
        self.handlers = [
            CommandHandler('cancel', self.end),
        ]

    def end(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            'Until next time',
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

def restartContext(context):
    videoInfo: VideoInfoResponse = FrameXService.getVideoInfo()

    bisectObj: BisectObj = {
        'low': 0,
        'high': videoInfo['frames'],
        'midpoint': round(videoInfo['frames'] / 2)

        }

    context.user_data['bisectObj'] = bisectObj

def bisectStep(bisectObj: BisectObj, funcResult):
    if(funcResult > 0):
        bisectObj['low'] = bisectObj['midpoint']
    elif(funcResult < 0):
        bisectObj['high'] = bisectObj['midpoint']

    bisectObj['midpoint'] = round((bisectObj['high']+bisectObj['low']) / 2)
    return bisectObj
    