################
# STATS MODULE #
################


# LIBRARIES

import logging
import json
import sys
import os
import csv
import time
import datetime


# FUNCTIONS

# Calculate the actual stats (update the stats file)
def update_stats(db_matchdays, db_transactions, db_stats, managers, initial_budget, start_date):

    # Calculate the budget of each manager
    with open(db_matchdays, 'r') as f1:
        matchdays = json.load(f1)
    with open(db_transactions, 'r') as f2:
        transactions = list(csv.reader(f2, delimiter=';'))
    stats_new = {}
    stats_new['stats'] = []
    for manager in managers:
        budget = initial_budget
        last_purchase_date = start_date
        # Calculate the budget of each manager: transactions
        for transaction in transactions:
            if transaction[1] == manager:
                if transaction[2] == "compra":
                    budget = str(int(budget) - int(transaction[4]))
                    last_purchase_date = transaction[0]
                elif transaction[2] == "venta":
                    budget = str(int(budget) + int(transaction[4]))
                else:
                    logging.warning("Detectada transacción incorrecta al actualizar las cuentas")
        # Calculate the budget of each manager: matchdays
        for matchday in matchdays['matchdays']:
            if matchday['manager'] == manager:
                matchday_points = \
                    int(matchday['matchday_1']) + int(matchday['matchday_2']) + int(matchday['matchday_3']) \
                    + int(matchday['matchday_4']) + int(matchday['matchday_5']) + int(matchday['matchday_6']) \
                    + int(matchday['matchday_7']) + int(matchday['matchday_8']) + int(matchday['matchday_9']) \
                    + int(matchday['matchday_10']) + int(matchday['matchday_11']) + int(matchday['matchday_12']) \
                    + int(matchday['matchday_13']) + int(matchday['matchday_14']) + int(matchday['matchday_15']) \
                    + int(matchday['matchday_16']) + int(matchday['matchday_17']) + int(matchday['matchday_18']) \
                    + int(matchday['matchday_19']) + int(matchday['matchday_20']) + int(matchday['matchday_21']) \
                    + int(matchday['matchday_22']) + int(matchday['matchday_23']) + int(matchday['matchday_24']) \
                    + int(matchday['matchday_25']) + int(matchday['matchday_26']) + int(matchday['matchday_27']) \
                    + int(matchday['matchday_28']) + int(matchday['matchday_29']) + int(matchday['matchday_30']) \
                    + int(matchday['matchday_31']) + int(matchday['matchday_32']) + int(matchday['matchday_33']) \
                    + int(matchday['matchday_34']) + int(matchday['matchday_35']) + int(matchday['matchday_36']) \
                    + int(matchday['matchday_37']) + int(matchday['matchday_38'])
                budget = str(int(budget) + (matchday_points * 100000))
        budget_formated = format(int(budget), ',d')

        # Calculate the days to buy by paying the entire clause
        last_purchase_timestamp = int(
            time.mktime(datetime.datetime.strptime(last_purchase_date, "%d/%m/%Y").timetuple())
        )
        current_timestamp = int(datetime.datetime.now().timestamp())
        last_purchase_days = int((float(current_timestamp - last_purchase_timestamp)) / 86400)
        days_to_clause = str(14 - last_purchase_days)
        # Register the stats
        stats_new['stats'].append({
            'manager': manager,
            'budget': budget_formated,
            'last_purchase': last_purchase_date,
            'days_to_clause': days_to_clause
        })

    # Check for changes in the stats file
    with open(db_stats, 'r') as f3:
        stats_ori = json.load(f3)
    if stats_new != stats_ori:
        with open(db_stats, 'w') as f4:
            json.dump(stats_new, f4, indent=2)
        return True
    else:
        return False


# Show the manager account statistics
def budget(bot, update):

    # Config file load
    script_path = os.path.dirname(sys.argv[0])
    with open(script_path + '/../config/config.json', 'r') as f1:
        config = json.load(f1)
    db_matchdays = config['DEFAULT']['DB_MATCHDAYS_FILE']
    db_transactions = config['DEFAULT']['DB_TRANSACTIONS_FILE']
    db_stats = config['DEFAULT']['DB_STATS_FILE']
    managers = config['LEAGUE']['MANAGERS']
    initial_budget = config['LEAGUE']['INITIAL_BUDGET']
    start_date = config['LEAGUE']['START_DATE']

    # Syntax checks
    params = update.message.text.replace("/stats_budget ", "")
    if params == "/stats_budget":
        bot.send_message(chat_id=update.message.chat_id,
                         text="Para mostrar las estadisticas presupuestarias debe proceder como se indica:\n"
                              "  /stats_budget all\n"
                              "  /stats_budget <manager>")
        return False

    # Show the account statistics for all managers
    if len(params.split(" ")) == 1 and params == "all":
        if update_stats(db_matchdays, db_transactions, db_stats, managers, initial_budget, start_date):
            bot.send_message(chat_id=update.message.chat_id, text="Se han recalculado las estadísticas")
            logging.info("Se han recalculado las estadísticas")
        with open(db_stats, 'r') as f2:
            stats = json.load(f2)
        for stat in stats['stats']:
            bot.send_message(chat_id=update.message.chat_id,
                             text="  Manager: " + stat['manager'] + "\n"
                                  "  Presupuesto: " + stat['budget'] + "\n")

    # Show the account statistics for a manager
    elif len(params.split(" ")) == 1:
        if params in managers:
            if update_stats(db_transactions, db_stats, managers, initial_budget, start_date):
                bot.send_message(chat_id=update.message.chat_id, text="Se han recalculado las estadísticas")
                logging.info("Se han recalculado las estadísticas")
            with open(db_stats, 'r') as f3:
                stats = json.load(f3)
            for stat in stats['stats']:
                if stat['manager'] == params:
                    bot.send_message(chat_id=update.message.chat_id,
                                     text="  Manager: " + stat['manager'] + "\n"
                                          "  Presupuesto: " + stat['budget'])
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text="No conozco al manager seleccionado")
            logging.warning(
                "Manager incorrecto al intentar mostrar las estadisticas presupuestarias, a petición del cliente ID " +
                str(update.message.chat_id))
            return False

    # Bad syntax
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Sintanxis incorrecta. Para mostrar las estadisticas presupuestarias debe proceder como se indica:\n"
                              "  /stats_budget all\n"
                              "  /stats_budget <manager>")
        logging.warning(
            "Sintaxis incorrecta al intentar mostrar las estadisticas presupuestarias, a petición del cliente ID " +
            str(update.message.chat_id))
        return False
    return True


# Show the manager clause statistics
def clause(bot, update):

    # Config file load
    script_path = os.path.dirname(sys.argv[0])
    with open(script_path + '/../config/config.json', 'r') as f1:
        config = json.load(f1)
    db_matchdays = config['DEFAULT']['DB_MATCHDAYS_FILE']
    db_transactions = config['DEFAULT']['DB_TRANSACTIONS_FILE']
    db_stats = config['DEFAULT']['DB_STATS_FILE']
    managers = config['LEAGUE']['MANAGERS']
    initial_budget = config['LEAGUE']['INITIAL_BUDGET']
    start_date = config['LEAGUE']['START_DATE']

    # Syntax checks
    params = update.message.text.replace("/stats_clause ", "")
    if params == "/stats_clause":
        bot.send_message(chat_id=update.message.chat_id,
                         text="Para mostrar la posibilidad de clausulazo debe proceder como se indica:\n"
                              "  /stats_clause all\n"
                              "  /stats_clause <manager>")
        return False

    # Show the clause statistics for all managers
    if len(params.split(" ")) == 1 and params == "all":
        if update_stats(db_matchdays, db_transactions, db_stats, managers, initial_budget, start_date):
            bot.send_message(chat_id=update.message.chat_id, text="Se han recalculado las estadísticas")
            logging.info("Se han recalculado las estadísticas")
        with open(db_stats, 'r') as f2:
            stats = json.load(f2)
        for stat in stats['stats']:
            bot.send_message(chat_id=update.message.chat_id,
                             text="  Manager: " + stat['manager'] + "\n"
                                  "  Última operación: " + stat['last_purchase'] + "\n"
                                  "  Días para clausulazo: " + stat['days_to_clause'] + "\n")

    # Show the clause statistics for a manager
    elif len(params.split(" ")) == 1:
        if params in managers:
            if update_stats(db_matchdays, db_transactions, db_stats, managers, initial_budget, start_date):
                bot.send_message(chat_id=update.message.chat_id, text="Se han recalculado las estadísticas")
                logging.info("Se han recalculado las estadísticas")
            with open(db_stats, 'r') as f3:
                stats = json.load(f3)
            for stat in stats['stats']:
                if stat['manager'] == params:
                    bot.send_message(chat_id=update.message.chat_id,
                                     text="  Manager: " + stat['manager'] + "\n"
                                          "  Última operación: " + stat['last_purchase'] + "\n"
                                          "  Días para clausulazo: " + stat['days_to_clause'])
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text="No conozco al manager seleccionado")
            logging.warning(
                "Manager incorrecto al intentar mostrar las estadisticas presupuestarias, a petición del cliente ID " +
                str(update.message.chat_id))
            return False

    # Bad syntax
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Sintanxis incorrecta. Para mostrar las estadisticas presupuestarias debe proceder como se indica:\n"
                              "  /stats_budget all\n"
                              "  /stats_budget <manager>")
        logging.warning(
            "Sintaxis incorrecta al intentar mostrar las estadisticas presupuestarias, a petición del cliente ID " +
            str(update.message.chat_id))
        return False
    return True
