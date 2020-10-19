from datetime import datetime
from dateutil.parser import parse
from app.models import Entry, NameMapping, Tag, AccountType,TagNameMapping
from config import Config
from app import db, format_datetime, format_currency
from app.my_parser import parseData, parseNameMappings, parseTagNameMappings
from setup import setup


def restoreData(db):

    # clear it all out, TODO: am i sure about this?
    setup()

    # name Mappings
    try:
        parseNameMappings(db, '%s/%s' % (Config.BACKUP_FOLDER, 'nameMappings.csv'))
    except FileNotFoundError:
        print('nameMappings.csv not found')

    # tag Mappings
    try:
        parseTagNameMappings(db, '%s/%s' % (Config.BACKUP_FOLDER, 'tagNameMappings.csv'))
    except FileNotFoundError:
        print('tagNameMappings.csv not found')

    # accounts
    try:
        parseData(db, '%s/%s' % (Config.BACKUP_FOLDER, 'Credit_Card.csv'), 'Credit Card')
    except FileNotFoundError:
        print('Credit_Card.csv not found')

    try:
        parseData(db, '%s/%s' % (Config.BACKUP_FOLDER, 'Money_Market.csv'), 'Money Market')
    except FileNotFoundError:
        print('Money_Market.csv not found')

    try:
        parseData(db, '%s/%s' % (Config.BACKUP_FOLDER, 'Checking.csv'), 'Checking')
    except FileNotFoundError:
        print('Checking.csv not found')





if __name__ == '__main__':
    restoreData(db)