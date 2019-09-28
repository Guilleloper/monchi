####################
# MATCHDAYS MODULE #
####################


# LIBRARIES

import logging
import json
import sys
import os
import csv
import time
import datetime
from shutil import copyfile


# Register a matchday
def edit(bot, update):
    # Config file load
    script_path = os.path.dirname(sys.argv[0])
    with open(script_path + '/../config/config.json', 'r') as f1:
        config = json.load(f1)
    db_matchdays = config['DEFAULT']['DB_MATCHDAYS_FILE']
    managers = config['LEAGUE']['MANAGERS']

    # Syntax checks
    params = update.message.text.replace("/matchdays_edit ", "")
    if params == "/matchdays_edit":
        bot.send_message(chat_id=update.message.chat_id,
                         text="Para registrar los puntos de una jornada se debe proceder como se indica:\n"
                              "  /matchdays_edit <jornada> <manager> <puntos>")
        return False
    args = params.split(" ")
    n_args = len(args)
    if n_args != 3:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Sintanxis incorrecta. Para registrar los puntos de una jornada se debe proceder "
                              "como se indica:\n"
                              "  /matchdays_edit <jornada> <manager> <puntos>")
        logging.warning(
            "Sintaxis incorrecta al intentar registrar los puntos de una jornada, a petición del cliente ID " +
            str(update.message.chat_id))
        return False
    else:
        matchday_number = args[0]
        matchday_manager = args[1]
        matchday_points = args[2]

    # Check the matchday number
    try:
        int(matchday_number)
    except ValueError:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Jornada no válida. La jornada ha de ser un valor numérico")
        logging.warning(
            "Detectado número de jornada no válido al intentar registrar los puntos de un jornada, "
            "a petición del cliente ID " + str(update.message.chat_id))
        return False
    if int(matchday_number) < 1 or int(matchday_number) > 38:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Jornada no válida. El número de jornada ha de estar compredido entre el 1 y el 38")
        logging.warning(
            "Detectado número de jornada no válido al intentar registrar los puntos de un jornada, "
            "a petición del cliente ID " + str(update.message.chat_id))
        return False

    # Check the matchday manager
    if matchday_manager not in managers:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Mánager no válido: Utilice un mánager registrado en esta Liga")
        logging.warning(
            "Detectado mánager no válido al intentar registrar los puntos de una jornada, "
            "a petición del cliente ID " + str(update.message.chat_id))
        return False

    # Check de matchday points
    try:
        int(matchday_points)
    except ValueError:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Puntos no válidos. Los puntos han de ser un valor numérico")
        logging.warning(
            "Detectado puntos no válidos al intentar registrar los puntos de un jornada, "
            "a petición del cliente ID " + str(update.message.chat_id))
        return False

    # Register the matchday points
    with open(db_matchdays, 'r') as f2:
        matchdays = json.load(f2)
    matchday_number = "matchday_" + matchday_number
    index = 0
    for matchday in matchdays['matchdays']:
        if matchday['manager'] == matchday_manager:
            matchdays['matchdays'][index][matchday_number] = matchday_points
        else:
            index += 1
    with open(db_matchdays, 'w') as f3:
        json.dump(matchdays, f3, indent=2)
    bot.send_message(chat_id=update.message.chat_id,
                     text="Puntos de jornada registrados")
    logging.info(
        "Se ha registrado los siguientes puntos de una jornada a petición del cliente ID "
        + str(update.message.chat_id) + ": " + "jornada " + matchday_number + ", manager " + matchday_manager +
        ", " + matchday_points + " puntos")
    return True


# List the matchdays
def show(bot, update):
    # Config file load
    script_path = os.path.dirname(sys.argv[0])
    with open(script_path + '/../config/config.json', 'r') as f1:
        config = json.load(f1)
    db_matchdays = config['DEFAULT']['DB_MATCHDAYS_FILE']

    # Syntax checks
    params = update.message.text.replace("/matchdays_list ", "")
    if params == "/matchdays_list":
        bot.send_message(chat_id=update.message.chat_id,
                         text="Para mostrar las puntuaciones se debe proceder como se indica:\n"
                              "  /matchdays_list all\n"
                              "  /matchdays_list <matchday>")
        return False

    if len(params.split(" ")) != 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Sintaxis incorrecta. Para mostrar las puntuaciones se debe proceder como se indica:\n"
                              "  /matchdays_list all\n"
                              "  /matchdays_list <matchday>")

        logging.warning(
            "Sintaxis incorrecta al intentar al intentar mostrar las puntuaciones, a petición del cliente ID " +
            str(update.message.chat_id))
        return False

    # Show all the matchdays points
    if len(params.split(" ")) == 1 and params == "all":
        with open(db_matchdays, 'r') as f2:
            matchdays = json.load(f2)
        points_sorted = {}
        for matchday in matchdays['matchdays']:
            matchday_manager = matchday['manager']
            matchday_points = int(matchday['matchday_1']) + int(matchday['matchday_2']) + int(matchday['matchday_3']) \
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
            points_sorted[matchday_manager] = matchday_points
        # Sort the output by the total points
        for key, value in sorted(points_sorted.items(), key=lambda item: item[1], reverse=True):
            bot.send_message(chat_id=update.message.chat_id,
                             text="  Manager: " + key + "\n"
                                                        "  Puntos: " + str(value) + "\n")
        return True

    # Syntax check (numeric matchday)
    if len(params.split(" ")) == 1:
        try:
            int(params)
        except ValueError:
            bot.send_message(chat_id=update.message.chat_id,
                             text="Jornada no válida. La jornada ha de ser un valor numérico")
            logging.warning(
                "Detectado número de jornada no válido al intentar mostrar las puntuaciones de un jornada, "
                "a petición del cliente ID " + str(update.message.chat_id))
            return False

    # Syntax check (matchday between 1 and 38)
    if len(params.split(" ")) == 1 and (int(params) < 1 or int(params) > 38):
        bot.send_message(chat_id=update.message.chat_id,
                         text="Jornada no válida. El número de jornada ha de estar compredido entre el 1 y el 38")
        logging.warning(
            "Detectado número de jornada no válido al mostrar las puntuaciones, a petición del cliente ID " +
            str(update.message.chat_id))
        return False

    # Show the account statistics for a matchday
    with open(db_matchdays, 'r') as f3:
        matchdays = json.load(f3)
    points_sorted = {}
    matchday_number = "matchday_" + params
    for matchday in matchdays['matchdays']:
        matchday_manager = matchday['manager']
        matchday_points = int(matchday[matchday_number])
        points_sorted[matchday_manager] = matchday_points
    # Sort the output by the total points
    for key, value in sorted(points_sorted.items(), key=lambda item: item[1], reverse=True):
        bot.send_message(chat_id=update.message.chat_id,
                         text="  Manager: " + key + "\n"
                                                    "  Puntos: " + str(value) + "\n")
    return True
