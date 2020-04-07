#!/usr/bin/env python3
"""
Guara's Happy Helper Telegram Bot

First, a few callback functions are defined. Those functions are passed
to the Dispatcher and registered at their respective places.
Then the bot is started and runs until we press Ctrl-C on the command line.
"""
import re
import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from env import BOT_TOKEN


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s -'
                    ' %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


SECTION, MEDICINE_SELECTION, MEDICINE_SIGNUP, \
    FOREIGN_SELECTION, FOREIGN_SIGNUP, REPORT = range(6)
OPTIONS = ['Medicina', 'Extranjeros', 'Ayuda', 'Reportar']


# GENERAL #
def start(update, context):
    logger.info(f"{update.message.from_user.first_name} started talking to me")
    update.message.reply_text(
        'Hola! Soy un bot conector! En cualquier momento podés tipear /start y te daremos una lista de comandos que podés usar. Por favor elegí el código de círculo al que querés entrar, este código seguramente te lo dio quién te comentó sobre nosotros.',
        reply_markup=ReplyKeyboardMarkup([OPTIONS], one_time_keyboard=True)
    )
    return SECTION


def select_option(update, context):
    update.message.reply_text(
        'Elije una de las siguientes opciones (en cualquier momento puedes escribir "cancelar"):',
        reply_markup=ReplyKeyboardMarkup([OPTIONS], one_time_keyboard=True)
    )
    return SECTION


# HELP #
def opt_help(update, context):
    user = update.message.from_user
    logger.info(f"{user.first_name} chose {update.message.text}")
    update.message.reply_text(
        'Hicimos este bot porque fue como se nos ocurrió que podíamos apoyar en estos tiempos. El bot es gratuito y está hecho con mucho amor por guara.ai. Si tenés alguna duda, sugerencia o ganas de darnos una mano podés escribirnos a info@guara.ai.'
    )
    return select_option(update, context)


# MEDICINE #
def get_med_professional():
    return {'name': 'Inés Benson', 'username': '@ineben'}


def opt_medicine(update, context):
    user = update.message.from_user
    logger.info(f"{user.first_name} chose {update.message.text}")
    MEDICINE_OPTS = ['🤔 Tengo una duda',
                     '💪🏻 Puedo estar de guardia desde mi cuarentena',
                     'Volver a empezar']
    update.message.reply_text('Genial. Creamos este bot pensando que hay muchos médicos que estarán en cuarentena y otros pueden encontrarse en situaciones difíciles o con dudas. Sólo para asegurarnos, para ser parte de este círculo tenés que tener que tener algún tipo de formación médica.')
    update.message.reply_text(
        'Habiendo aclarador esto: Tenés una duda o sos un experto?',
        reply_markup=ReplyKeyboardMarkup([MEDICINE_OPTS], one_time_keyboard=True)
    )
    return MEDICINE_SELECTION


def med_doubt(update, context):
    user = update.message.from_user
    update.message.reply_text('Buscando un profesional médico que te pueda ayudar...')
    professional = get_med_professional()
    logger.info(
        f"{user.first_name} chose {update.message.text}. "
        f"Recommending {professional['name']} ({professional['username']})"
    )
    update.message.reply_text(
        f"Podés contactarte con {professional['name']} ({professional['username']})."
    )
    update.message.reply_text('Por favor ten respeto por su tiempo!')


def med_signup(update, context):
    user = update.message.from_user
    logger.info(f"{user.first_name} wants to sign up as medical professional")
    update.message.reply_text(
        f'Genial, {user.first_name}. La idea es que le daremos tu contacto de Telegram a personas que tengan dudas que puedas resolver.\n\n'
    )
    update.message.reply_text(
        'Si no estás de acuerdo poné "no". Si estás de acuerdo con esto, ¿podrías darme una breve introducción sobre tu experiencia por favor para poder conectarte con alguien? Por favor escribila en tercera persona. Por ejemplo "es un médico clínico con 10 años de experiencia en el Hospital de Clínicas que se encuentra haciendo cuarentena en Buenos Aires". Este resumen es para no hacerte perder tiempo a vos ni a una persona con una duda.'
    )
    return MEDICINE_SIGNUP


def med_signed_up(update, context):
    user = update.message.from_user
    logger.info(f"{user.first_name} signed up as medical professional with text: {update.message.text}")
    update.message.reply_text(
        f"Buenísimo, {user.first_name}. Muchas gracias por dar una mano! Podés darte de baja en cualquier momento escribiendo /eliminarme."
    )


# FOREIGN #
def get_local_helper():
    return {'name': 'Seni Nosneb', 'username': '@ineben'}


def opt_foreigner(update, context):
    user = update.message.from_user
    logger.info(f"{user.first_name} chose {update.message.text}")
    FOREIGN_OPTS = ['🤔 Tengo una duda',
                    '💪🏻 Me considero un local',
                    'Volver a empezar']
    update.message.reply_text('Gran grupo ;) Creamos este bot pensando que todo este tema de la contingencia puede estar causando muchas dudas a algunos recién llegados al país.')
    update.message.reply_text(
        '¿Tenés una duda o te considerás un local en Chile?',
        reply_markup=ReplyKeyboardMarkup([FOREIGN_OPTS], one_time_keyboard=True)
    )
    return FOREIGN_SELECTION


def foreigner_doubt(update, context):
    user = update.message.from_user
    update.message.reply_text('Buscando un local que te pueda ayudar...')
    professional = get_local_helper()
    logger.info(f"{user.first_name} chose {update.message.text}. "
                f"Recommending {professional['name']} ({professional['username']})")
    update.message.reply_text(
        f"Podés contactarte con {professional['name']} ({professional['username']})."
    )
    update.message.reply_text("Por favor ten respeto por su tiempo!")


def foreigner_signup(update, context):
    user = update.message.from_user
    logger.info(f"{user.first_name} wants to sign up as a local")
    update.message.reply_text(
        f'Genial, {user.first_name}. La idea es que le daremos tu contacto de Telegram a personas que tengan dudas que puedas resolver.\n\n'
    )
    update.message.reply_text(
        '¿Podrías darme una breve introducción sobre tu experiencia por favor para poder conectarte con alguien? Por favor escribila en tercera persona. Por ejemplo "es un argentino que vive hace 10 años en Chile y tiene un restaurant en Macul". Este resumen es para no hacerte perder tiempo a vos ni a una persona con una duda. '
        'Si no estás de acuerdo con que compartamos tu ID, por favor tipea "no".'
    )
    return FOREIGN_SIGNUP


def foreigner_signed_up(update, context):
    user = update.message.from_user
    logger.info(f"{user.first_name} signed up as local with text: {update.text}")
    update.message.reply_text(
        f"Wow {user.first_name}. Muchas gracias por da una mano!!! Si preferís eliminar tu nombre de nuestra red de apoyo podés hacer tipeando: `/eliminarme`."
    )
    return False


# REPORT #
def opt_report(update, context):
    user = update.message.from_user
    logger.info(f"{user.first_name} wants to report someone")
    update.message.reply_text(
        'Si querés reportar a una persona tipea su usuario y cuéntanos la razón por la que lo quieres reportar y lo evaluaremos, puede que te contactemos para más información!'
    )
    return REPORT


def reported_professional(update, context):
    user = update.message.from_user
    logger.info(f"{user.first_name} ({user.username})'s report:\n{update.message.text}")
    update.message.reply_text(f"Gracias. Tu reporte ha sido registrado.")


def easter_egg(update, context):
    update.message.reply_text('42')

# # If you wanted to receive a picture...
# def photo(update, context):
#     user = update.message.from_user
#     photo_file = update.message.photo[-1].get_file()
#     photo_file.download('user_photo.jpg')
#     logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
#     update.message.reply_text('Gorgeous! Now, send me your location please, '
#                               'or send /skip if you don\'t want to.')
#     return LOCATION

# def skip_photo(update, context):
#     user = update.message.from_user
#     logger.info("User %s did not send a photo.", user.first_name)
#     update.message.reply_text('I bet you look great! '
#                               'Now, send me your location please, '
#                               'or send /skip.')
#     return LOCATION


# # ...or a location
# def location(update, context):
#     user = update.message.from_user
#     user_location = update.message.location
#     logger.info("Location of %s: %f / %f",
#                 user.first_name,
#                 user_location.latitude,
#                 user_location.longitude)
#     update.message.reply_text('Maybe I can visit you sometime! '
#                               'At last, tell me something about yourself.')
#     return BIO

# def skip_location(update, context):
#     user = update.message.from_user
#     logger.info("User %s did not send a location.", user.first_name)
#     update.message.reply_text('You seem a bit paranoid! '
#                               'At last, tell me something about yourself.')
#     return BIO


def cancel(update, context):
    user = update.message.from_user
    logger.info(f"User {user.first_name} canceled the conversation.")
    update.message.reply_text('Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    logger.info("Setting-up...")
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SECTION: [
                MessageHandler(Filters.regex(re.compile(fr'^{OPTIONS[0]}$', re.IGNORECASE)), opt_medicine),
                MessageHandler(Filters.regex(re.compile(fr'^{OPTIONS[1]}$', re.IGNORECASE)), opt_foreigner),
                MessageHandler(Filters.regex(re.compile(fr'^{OPTIONS[2]}$', re.IGNORECASE)), opt_help),
                MessageHandler(Filters.regex(re.compile(fr'^{OPTIONS[3]}$', re.IGNORECASE)), opt_report),
            ],

            MEDICINE_SELECTION: [
                MessageHandler(Filters.regex('duda'), med_doubt),
                MessageHandler(Filters.regex('guardia'), med_signup),
                MessageHandler(Filters.regex('empezar'), select_option),
            ],

            MEDICINE_SIGNUP: [
                MessageHandler(Filters.regex('(no|cancelar|start|volver)'), select_option),
                MessageHandler(Filters.text, med_signed_up)
            ],

            FOREIGN_SELECTION: [
                MessageHandler(Filters.regex('duda'), foreigner_doubt),
                MessageHandler(Filters.regex('local'), foreigner_signup),
                MessageHandler(Filters.regex('empezar'), select_option),
            ],

            FOREIGN_SIGNUP: [
                MessageHandler(Filters.regex('(no|cancelar|start|volver)'), select_option),
                MessageHandler(Filters.text, foreigner_signed_up)
            ],

            REPORT: [
                MessageHandler(Filters.regex('(no|cancelar|start|volver)'), select_option),
                MessageHandler(Filters.text, reported_professional)
            ],

            # PHOTO: [
            #     MessageHandler(Filters.photo, photo),
            #     CommandHandler('skip', skip_photo)
            # ],

            # LOCATION: [
            #     MessageHandler(Filters.location, location),
            #     CommandHandler('skip', skip_location)
            # ],
        },

        fallbacks=[
            CommandHandler('cancel', cancel),
            CommandHandler('cancelar', cancel),
            MessageHandler(Filters.regex('cancelar'), cancel),
            CommandHandler('ayuda', opt_help),
            CommandHandler('empezar', start),
            CommandHandler('start', start),
            MessageHandler(Filters.regex('(cancel|empezar|start)'), start),
            MessageHandler(Filters.regex('meaning of life'), easter_egg),
        ]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    logger.info('Started!')
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
