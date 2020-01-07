#######################
# TRANSACTIONS MODULE #
#######################


# LIBRARIES

import logging
import json
import sys
import os
import csv
import time
import datetime
from shutil import copyfile


# FUNCTIONS

# Make a transaction file backup
def backup(db_transactions, db_transactions_backup):
    try:
        copyfile(db_transactions, db_transactions_backup)
    except:
        return False
    return True


# Recover a transaction file from a backup
def restore(db_transactions, db_transactions_backup):
    try:
        copyfile(db_transactions_backup, db_transactions)
    except:
        return False
    return True


# Register a transaction
def add(bot, update):

    # Config file load
    script_path = os.path.dirname(sys.argv[0])
    with open(script_path + '/../config/config.json', 'r') as f1:
        config = json.load(f1)
    db_transactions = config['DEFAULT']['DB_TRANSACTIONS_FILE']
    db_transactions_backup = config['DEFAULT']['DB_TRANSACTIONS_BACKUP_FILE']
    managers = config['LEAGUE']['MANAGERS']

    # Syntax checks
    params = update.message.text.replace("/transactions_add ", "")
    if params == "/transactions_add":
        bot.send_message(chat_id=update.message.chat_id,
                         text="Para registrar una transacción debe proceder como se indica:\n"
                              "  /transactions_add <fecha> <manager> <compra/venta> <jugador> <precio>")
        return False
    args = params.split(" ")
    n_args = len(args)
    if n_args < 5:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Sintanxis incorrecta. Para registrar una transacción debe proceder como se indica:\n"
                              "  /transactions_add <fecha> <manager> <compra/venta> <jugador> <precio>")
        logging.warning(
            "Sintaxis incorrecta al intentar registrar una transacción, a petición del cliente ID " +
            str(update.message.chat_id))
        return False
    else:
        transaction_date = args[0]
        transaction_manager = args[1]
        transaction_action = args[2]
        transaction_player = ' '.join(args[3:-1])
        transaction_cost = args[n_args - 1]

    # Check the transaction date
    try:
        datetime.datetime.strptime(transaction_date, '%d/%m/%Y')
    except ValueError:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Fecha no válida: El formato de la fecha debe de ser \"DD/MM/YYYY\"")
        logging.warning(
            "Detectada fecha no válida al intentar registrar una transacción, a petición del cliente ID " +
            str(update.message.chat_id))
        return False

    # Check the manager of the transaction
    if transaction_manager not in managers:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Mánager no válido: Utilice un mánager registrado en esta Liga")
        logging.warning(
            "Detectado mánager no válido al intentar registrar una transacción, a petición del cliente ID " +
            str(update.message.chat_id))
        return False

    # Check the action of the transaction
    if transaction_action != "compra" and transaction_action != "venta":
        bot.send_message(chat_id=update.message.chat_id,
                         text="Acción no válida: Las acciones válidas son \"compra\" o \"venta\"")
        logging.warning(
            "Detectada acción no válida al intentar registrar una transacción, a petición del cliente ID " +
            str(update.message.chat_id))
        return False

    # Check the transaction cost
    try:
        int(transaction_cost)
    except ValueError:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Precio no válido. El precio ha de ser un valor numérico")
        logging.warning(
            "Detectado precio no válido al intentar registrar una transacción, a petición del cliente ID " +
            str(update.message.chat_id))
        return False

    # Make a transaction file backup
    if backup(db_transactions, db_transactions_backup):
        logging.debug("Se ha realizado un backup del fichero de transacciones, al registrar una nueva transacción")
    else:
        logging.warning("Ha fallado el backup del fichero de transacciones, al registrar una nueva transacción")

    # Register the transaction
    transaction = transaction_date + ";" + transaction_manager + ";" + transaction_action + ";" + \
                  transaction_player + ";" + transaction_cost
    with open(db_transactions, 'a+') as f2:
        f2.write("\n")
        f2.write(transaction)
    bot.send_message(chat_id=update.message.chat_id,
                     text="Transacción añadida")
    logging.info(
        "Se ha registrado la siguiente transacción a petición del cliente ID " + str(update.message.chat_id) + ": " +
        transaction)
    return True


# Show the transactions registered
def show(bot, update):

    # Config file load
    script_path = os.path.dirname(sys.argv[0])
    with open(script_path + '/../config/config.json', 'r') as f1:
        config = json.load(f1)
    db_transactions = config['DEFAULT']['DB_TRANSACTIONS_FILE']
    managers = config['LEAGUE']['MANAGERS']

    # Syntax checks
    params = update.message.text.replace("/transactions_list ", "")
    if params == "/transactions_list":
        bot.send_message(chat_id=update.message.chat_id,
                         text="Para mostrar las transacciones registradas debe proceder como se indica:\n"
                              "  /transactions_list -d <days>\n"
                              "  /transactions_list -m <manager>\n"
                              "  /transactions_list -p <player>")
        return False

    # Show the transactions from the selected days before
    if len(params.split(" ")) == 2 and params.split(" ")[0] == "-d":
        # Syntax check (numeric days)
        try:
            days = int(params.split(" ")[1])
            # Show the transactions from the selected days before
            with open(db_transactions, 'r') as f2:
                transactions = list(csv.reader(f2, delimiter=';'))
            first_line = True
            hit = False
            for transaction in transactions:
                if not first_line:
                    transaction_timestamp = time.mktime(
                        datetime.datetime.strptime(transaction[0], "%d/%m/%Y").timetuple())
                    current_timestamp = int(datetime.datetime.now().timestamp())
                    if transaction_timestamp >= (current_timestamp - (days * 86400)):
                        hit = True
                        if transaction[2] == "compra":
                            action = " compra a "
                        if transaction[2] == "venta":
                            action = " vende a "
                        cost = format(int(transaction[4]), ',d')
                        message = transaction[0] + " - " + transaction[1] + action + transaction[3] + " por " + cost
                        bot.send_message(chat_id=update.message.chat_id,
                                         text=message)
                first_line = False
            if not hit:
                bot.send_message(chat_id=update.message.chat_id,
                                 text="(ninguna)")
            return True
        except ValueError:
            bot.send_message(chat_id=update.message.chat_id,
                             text="Valor de días no válido. Los días han de tener un valor numérico")
            logging.warning(
                "Días incorrectos al intentar mostrar las transacciones, "
                "a petición del cliente ID " + str(update.message.chat_id))
            return False

    # Show the transactions from the selected manager
    elif len(params.split(" ")) == 2 and params.split(" ")[0] == "-m":
        # Check the manager existence
        manager = params.split(" ")[1]
        if manager not in managers:
            bot.send_message(chat_id=update.message.chat_id,
                             text="No conozco al mánager seleccionado")
            logging.warning(
                "Manager incorrecto al intentar mostrar transacciones, a petición del cliente ID " +
                str(update.message.chat_id))
            return False
        else:
            with open(db_transactions, 'r') as f3:
                transactions = list(csv.reader(f3, delimiter=';'))
            first_line = True
            hit = False
            for transaction in transactions:
                if not first_line:
                    if transaction[1] == manager:
                        hit = True
                        if transaction[2] == "compra":
                            action = " compra a "
                        if transaction[2] == "venta":
                            action = " vende a "
                        cost = format(int(transaction[4]), ',d')
                        message = transaction[0] + " - " + transaction[1] + action + transaction[3] + " por " + cost
                        bot.send_message(chat_id=update.message.chat_id,
                                         text=message)
                first_line = False
            if not hit:
                bot.send_message(chat_id=update.message.chat_id,
                                 text="(ninguna)")
            return True

    # Show the transactions with the selected player
    elif len(params.split(" ")) >= 2 and params.split(" ")[0] == "-p":
        player = " ".join(params.split(" ")[1:])
        with open(db_transactions, 'r') as f4:
            transactions = list(csv.reader(f4, delimiter=';'))
        first_line = True
        hit = False
        for transaction in transactions:
            if not first_line:
                if transaction[3] == player:
                    hit = True
                    if transaction[2] == "compra":
                        action = " compra a "
                    if transaction[2] == "venta":
                        action = " vende a "
                    cost = format(int(transaction[4]), ',d')
                    message = transaction[0] + " - " + transaction[1] + action + transaction[3] + " por " + cost
                    bot.send_message(chat_id=update.message.chat_id,
                                     text=message)
            first_line = False
        if not hit:
            bot.send_message(chat_id=update.message.chat_id,
                             text="(ninguna)")
        return True

    # Bad syntax
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Sintanxis incorrecta. Para mostrar las transacciones registradas debe proceder como se indica:\n"
                              "  /transactions_list -d <days>\n"
                              "  /transactions_list -m <manager>\n"
                              "  /transactions_list -p <player>")
        logging.warning(
            "Sintaxis incorrecta al intentar mostrar las transacciones registradas, a petición del cliente ID " +
            str(update.message.chat_id))
        return False


# Remove the last registered transaction
def remove(bot, update):

    # Config file load
    script_path = os.path.dirname(sys.argv[0])
    with open(script_path + '/../config/config.json', 'r') as f1:
        config = json.load(f1)
    db_transactions = config['DEFAULT']['DB_TRANSACTIONS_FILE']
    db_transactions_backup = config['DEFAULT']['DB_TRANSACTIONS_BACKUP_FILE']

    # Make a transaction file backup
    if backup(db_transactions, db_transactions_backup):
        logging.debug("Se ha realizado un backup del fichero de transacciones, al eliminar la última transacción")
    else:
        logging.warning("Ha fallado el backup del fichero de transacciones, al eliminar la última transacción")

    # Remove the last registered transaction
    with open(db_transactions, 'r') as f2:
        transactions_lines = f2.readlines()
    with open(db_transactions, 'w') as f3:
        transactions_lines = transactions_lines[:-1]
        # remove the '/n' at the end of the last line
        transactions_lines[len(transactions_lines)-1] = transactions_lines[len(transactions_lines)-1][:-1]
        f3.writelines(transactions_lines)
    bot.send_message(chat_id=update.message.chat_id,
                     text="Transacción eliminada")
    logging.info(
        "Se ha eliminado la última transacción a petición del cliente ID " + str(update.message.chat_id))
    return True


# Restore transaction file from a backup
def undo(bot, update):

    # Config file load
    script_path = os.path.dirname(sys.argv[0])
    with open(script_path + '/../config/config.json', 'r') as f1:
        config = json.load(f1)
    db_transactions = config['DEFAULT']['DB_TRANSACTIONS_FILE']
    db_transactions_backup = config['DEFAULT']['DB_TRANSACTIONS_BACKUP_FILE']

    # Restore the transaction file
    if restore(db_transactions, db_transactions_backup):
        bot.send_message(chat_id=update.message.chat_id,
                         text="Se ha deshecho el último cambio")
        logging.info("Se ha restaurado el fichero de transacciones de un backup")
    else:
        logging.warning("Ha fallado el backup del fichero de transacciones, al registrar una nueva transacción")