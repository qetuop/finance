from datetime import datetime
from dateutil.parser import parse
from app.models import Entry, NameMapping, Tag, AccountType
from config import Config
from app import db, format_datetime, format_currency

accountFileDict = {}


def openAccountFile(accountType):
    accountFile = open('%s/%s.csv' % (Config.UPLOAD_FOLDER, accountType.replace(' ', '_')), "w")

    if accountType == 'Checking':
        accountFile.write("\"Date\",\"No.\",\"Description\",\"Debit\",\"Credit\",\"Name\",\"Tag\"\n")
    elif accountType == 'Money Market':
        accountFile.write("\"Date\",\"No.\",\"Description\",\"Debit\",\"Credit\",\"Name\",\"Tag\"\n")
    elif accountType == 'Credit Card':
        accountFile.write("\"Transaction Date\",\"Posted Date\",\"Description\",\"Debit\",\"Credit\",\"Name\",\"Tag\"\n")

    return accountFile


def writeEntry(entry):
    global accountFileDict

    accountType = entry.account_type
    accountFile = None
    if accountFileDict.get(accountType) is None:
        accountFile = openAccountFile(accountType)
        accountFileDict[accountType] = accountFile

    if accountType == 'Checking':
        accountFileDict[accountType].write('"{}","{}","{}","{}","{}","{}","{}"\n'.format(format_datetime(entry.date),
                                                                                         entry.check_number,
                                                                                         entry.description,
                                                                                         format_currency(entry.debit,
                                                                                                         format='simple'),
                                                                                         format_currency(entry.credit,
                                                                                                         format='simple'),
                                                                                         entry.name,
                                                                                         entry.displayTag()))
    elif accountType == 'Money Market':
        accountFileDict[accountType].write('"{}","{}","{}","{}","{}","{}","{}"\n'.format(format_datetime(entry.date),
                                                                               entry.check_number, entry.description,
                                                                               format_currency(entry.debit,
                                                                                               format='simple'),
                                                                               format_currency(entry.credit,
                                                                                               format='simple'),
                                                                                         entry.name,
                                                                                         entry.displayTag()))
    elif accountType == 'Credit Card':
        accountFileDict[accountType].write('"{}","{}","{}","{}","{}","{}","{}"\n'.format(format_datetime(entry.date),
                                                                               format_datetime(entry.posted_date),
                                                                               entry.description,
                                                                               format_currency(entry.debit,
                                                                                               format='simple'),
                                                                               format_currency(entry.credit,
                                                                                               format='simple'),
                                                                                         entry.name,
                                                                                         entry.displayTag()))


def writeAll(db):
    entries = Entry.query.all()
    print(entries)
    for entry in entries:
        writeEntry(entry)

    # close each account
    for f in accountFileDict.values():
        f.close()


if __name__ == '__main__':
    print(__name__)
    writeAll(db)
