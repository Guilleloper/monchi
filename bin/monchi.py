##########
# MONCHI #
##########


# LIBRARIES

import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import json
import sys
import os
from modules import mod_stats
from modules import mod_transactions
from modules import mod_matchdays


# FUNCTIONS

# Check authorized access
def client_authentication(bot, client_id):
    if str(client_id) in client_ids:
        return True
    else:
        bot.send_message(chat_id=client_id,
                         text="Lo siento, pero no estás autorizado para interactuar conmigo.\n"
                              ":(")
        logging.warning("Registrado acceso no autorizado del cliente " + str(client_id))
        return False


# /start option
def start(bot, update):
    if client_authentication(bot, update.message.chat_id):
        bot.send_message(chat_id=update.message.chat_id, text="Monchi a la escucha. Estoy deseando trabajar contigo.\n"
                                              "Si necesitas ayuda usa /help")


# /help option
def help(bot, update):
    if client_authentication(bot, update.message.chat_id):
        bot.send_message(chat_id=update.message.chat_id, text="Opciones disponibles:\n"
                                                              "  /matchdays\n"
                                                              "  /stats\n"
                                                              "  /transactions")


# Unknown options
def unknown(bot, update):
    if client_authentication(bot, update.message.chat_id):
        bot.send_message(chat_id=update.message.chat_id, text="Lo siento, no conozco esa opción.\n"
                                                              "Si necesita ayuda use /help")


# Internal errors
def error(update, error):
    logging.warning('Update "%s" caused error "%s"', update, error)


# /mantchdays option
def matchdays(bot, update):
    if client_authentication(bot, update.message.chat_id):
        bot.send_message(chat_id=update.message.chat_id, text="Administrar jornadas:\n"
                                                              "  /matchdays_edit\n"
                                                              "  /matchdays_list\n"
                                                              "  <--  /back")


# /matchdays_edit option
def matchdays_edit(bot, update):
    if client_authentication(bot, update.message.chat_id):
        mod_matchdays.edit(bot, update)
        matchdays(bot, update)


# /matchdays_list option
def matchdays_list(bot, update):
    if client_authentication(bot, update.message.chat_id):
        mod_matchdays.show(bot, update)
        matchdays(bot, update)


# /stats option
def stats(bot, update):
    if client_authentication(bot, update.message.chat_id):
        bot.send_message(chat_id=update.message.chat_id, text="Mostrar estadisticas:\n"
                                                              "  /stats_budget\n"
                                                              "  /stats_clause\n"
                                                              "  <--  /back")


# /stats_budget option
def stats_budget(bot, update):
    if client_authentication(bot, update.message.chat_id):
        mod_stats.budget(bot, update)
        stats(bot, update)


# /stats_clause option
def stats_clause(bot, update):
    if client_authentication(bot, update.message.chat_id):
        mod_stats.clause(bot, update)
        stats(bot, update)


# /transactions option
def transactions(bot, update):
    if client_authentication(bot, update.message.chat_id):
        bot.send_message(chat_id=update.message.chat_id, text="Administrar transacciones:\n"
                                                              "  /transactions_add\n"
                                                              "  /transactions_list\n"
                                                              "  /transactions_remove\n"
                                                              "  /transactions_undo\n"
                                                              "  <--  /back")


# /transactions_add option
def transactions_add(bot, update):
    if client_authentication(bot, update.message.chat_id):
        mod_transactions.add(bot, update)
        transactions(bot, update)


# /transactions_list option
def transactions_list(bot, update):
    if client_authentication(bot, update.message.chat_id):
        mod_transactions.show(bot, update)
        transactions(bot, update)


# /transactions_remove option
def transactions_remove(bot, update):
    if client_authentication(bot, update.message.chat_id):
        mod_transactions.remove(bot, update)
        transactions(bot, update)


# /transactions_undo option
def transactions_undo(bot, update):
    if client_authentication(bot, update.message.chat_id):
        mod_transactions.undo(bot, update)
        transactions(bot, update)


# MAIN PROGRAM

def main():

    # Config file load
    script_path = os.path.dirname(sys.argv[0])
    with open(script_path + '/../config/config.json', 'r') as f:
        config = json.load(f)
    log_file = config['DEFAULT']['LOG_FILE']
    log_level = config['DEFAULT']['LOG_LEVEL']
    bot_token = config['DEFAULT']['BOT_TOKEN']
    global client_ids
    client_ids = config['DEFAULT']['CLIENT_IDS']

    # Configure logging to file
    logging.basicConfig(level=getattr(logging, log_level),
                        format="[%(asctime)s] [%(levelname)s] - [Monchi] - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename=log_file,
                        filemode='a')

    # Configure logging to stdout
    console = logging.StreamHandler()
    console.setLevel(getattr(logging, log_level))
    console.setFormatter(logging.Formatter("[%(levelname)s] - [Monchi] - %(message)s"))
    logging.getLogger('').addHandler(console)

    # Start
    logging.info("Inicio del programa")

    # Create bot EventHandler
    updater = Updater(token=bot_token)

    # Get the Dispatcher for registering the Handlers
    dispatcher = updater.dispatcher

    # Add a Handler to the Dispatcher for the command /start
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Add a Handler to the Dispatcher for the command /help
    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    # Add a Handler to the Dispatcher for the command /matchdays
    matchdays_handler = CommandHandler('matchdays', matchdays)
    dispatcher.add_handler(matchdays_handler)

    # Add a Handler to the Dispatcher for the command /matchdays_edit
    matchdays_edit_handler = CommandHandler('matchdays_edit', matchdays_edit)
    dispatcher.add_handler(matchdays_edit_handler)

    # Add a Handler to the Dispatcher for the command /matchdays_list
    matchdays_list_handler = CommandHandler('matchdays_list', matchdays_list)
    dispatcher.add_handler(matchdays_list_handler)

    # Add a Handler to the Dispatcher for the command /stats
    stats_handler = CommandHandler('stats', stats)
    dispatcher.add_handler(stats_handler)

    # Add a Handler to the Dispatcher for the command /stats_budget
    stats_budget_handler = CommandHandler('stats_budget', stats_budget)
    dispatcher.add_handler(stats_budget_handler)

    # Add a Handler to the Dispatcher for the command /stats_clause
    stats_clause_handler = CommandHandler('stats_clause', stats_clause)
    dispatcher.add_handler(stats_clause_handler)

    # Add a Handler to the Dispatcher for the command /transactions
    transactions_handler = CommandHandler('transactions', transactions)
    dispatcher.add_handler(transactions_handler)

    # Add a Handler to the Dispatcher for the command /transactions_add
    transactions_add_handler = CommandHandler('transactions_add', transactions_add)
    dispatcher.add_handler(transactions_add_handler)

    # Add a Handler to the Dispatcher for the command /transactions_list
    transactions_list_handler = CommandHandler('transactions_list', transactions_list)
    dispatcher.add_handler(transactions_list_handler)

    # Add a Handler to the Dispatcher for the command /transactions_remove
    transactions_remove_handler = CommandHandler('transactions_remove', transactions_remove)
    dispatcher.add_handler(transactions_remove_handler)

    # Add a Handler to the Dispatcher for the command /transactions_undo
    transactions_undo_handler = CommandHandler('transactions_undo', transactions_undo)
    dispatcher.add_handler(transactions_undo_handler)

    # Add a Handler to the Dispatcher for the command /back
    back_handler = CommandHandler('back', help)
    dispatcher.add_handler(back_handler)

    # Add a Handler to the Dispatcher for the unknown commands
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    # Register all the errors
    dispatcher.add_error_handler(error)

    # Start Updater
    updater.start_polling()
    logging.info("Monchi online")
    updater.idle()
    logging.info("Monchi offline")

    # End
    logging.info("Fin del programa")


if __name__ == '__main__':
    main()
