from datetime import datetime
from dateutil.parser import parse
from app.models import Entry, NameMapping, Tag, AccountType
from config import Config
from app import db, format_datetime, format_currency
from app.my_parser import parseData, parseNameMappings


def importData(db):
    # name Mappings
    parseNameMappings(db, 'nameMappings.csv')

    # accounts

    parseData(db, '%s/%s' % (Config.BACKUP_FOLDER, 'Credit_Card.csv'), 'Credit Card', parseExtra=True)
    parseData(db, '%s/%s' % (Config.BACKUP_FOLDER, 'Money_Market.csv'), 'Money Market', parseExtra=True)
    parseData(db, '%s/%s' % (Config.BACKUP_FOLDER, 'Checking.csv'), 'Checking', parseExtra=True)

if __name__ == '__main__':
    importData(db)