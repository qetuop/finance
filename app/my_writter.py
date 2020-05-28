from datetime import datetime
from dateutil.parser import parse
from app.models import Entry, NameMapping, Tag, AccountType
from config import Config
from app import db, format_datetime, format_currency

accountFileDict = {}


def openAccountFile(accountType):
    accountFile = open('%s/%s.csv' % (Config.BACKUP_FOLDER, accountType.replace(' ', '_')), "w")

    if accountType == 'Checking':
        accountFile.write("\"Date\",\"No.\",\"Description\",\"Debit\",\"Credit\",\"Name\",\"Tag\"\n")
    elif accountType == 'Money Market':
        accountFile.write("\"Date\",\"No.\",\"Description\",\"Debit\",\"Credit\",\"Name\",\"Tag\"\n")
    elif accountType == 'Credit Card':
        accountFile.write("\"Transaction Date\",\"Posted Date\",\"Description\",\"Debit\",\"Credit\",\"Name\",\"Tag\"\n")

    return accountFile


def writeEntry(entry, accountFile):
    global accountFileDict

    accountType = entry.account_type

    if accountType == 'Checking':
        accountFile.write('"{}","{}","{}","{}","{}","{}","{}"\n'.format(format_datetime(entry.date),
                                                                                         entry.check_number,
                                                                                         entry.description,
                                                                                         format_currency(entry.debit,
                                                                                                         format='simple'),
                                                                                         format_currency(entry.credit,
                                                                                                         format='simple'),
                                                                                         entry.name,
                                                                                         entry.displayTag()))
    elif accountType == 'Money Market':
        accountFile.write('"{}","{}","{}","{}","{}","{}","{}"\n'.format(format_datetime(entry.date),
                                                                                         entry.check_number,
                                                                                         entry.description,
                                                                                         format_currency(entry.debit,
                                                                                               format='simple'),
                                                                                         format_currency(entry.credit,
                                                                                               format='simple'),
                                                                                         entry.name,
                                                                                         entry.displayTag()))
    elif accountType == 'Credit Card':
        accountFile.write('"{}","{}","{}","{}","{}","{}","{}"\n'.format(format_datetime(entry.date),
                                                                                        format_datetime(entry.posted_date),
                                                                                        entry.description,
                                                                                        format_currency(entry.debit,
                                                                                               format='simple'),
                                                                                         format_currency(entry.credit,
                                                                                               format='simple'),
                                                                                         entry.name,

                                                                                         entry.displayTag()))
def writeAccount(accountType):
    accountFile = openAccountFile(accountType)

    entries = Entry.query.filter_by(account_type=accountType).all()
    for entry in entries:
        writeEntry(entry, accountFile)

    accountFile.close()

def writeEntries():
    accountTypes = AccountType.query.all()
    for accountType in accountTypes:
        writeAccount(accountType.name)

def writeNameMappings():
    nameMappingFile = open('%s/nameMappings.csv'%Config.BACKUP_FOLDER, "w")
    nameMappingFile.write("\"Description\",\"Name\", \"Exact Match\n")

    nameMappings = NameMapping.query.all()
    for nameMapping in nameMappings:
        nameMappingFile.write('"{}","{}","{}"\n'.format(nameMapping.description,nameMapping.name, nameMapping.exact_match))
'''
def writeTags():
    tagFile = open('%s/tags.csv'%Config.BACKUP_FOLDER, "w")
    tagFile.write("\"Description\",\"Tag\"\n")

    tags = Tag.querry.all()
    for tag in tags:
        entry = Entry.query.filter_by(id=tag.id)
        tagFile.write('"{}","{}"\n'.format(entry.description,tag.name))
'''
def backupData(db):
    writeEntries()
    writeNameMappings()

    #writeTags()

    # close each account
    #for f in accountFileDict.values():
    #    f.close()


if __name__ == '__main__':
    backupData(db)
