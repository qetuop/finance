from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app.models import NameMapping, Tag, Entry, AccountType, TagNameMapping
from app.my_parser import parseData, parseNameMappings
from app import db
import sys

#app = Flask(__name__)
#app.config.from_object(Config)
#db = SQLAlchemy(app)



def createCategories():
    print('createCategories()')

    tagDict = {
        'Bill':['Electric','Water', 'HOA', 'Car Insurance', 'Credit Card Payment', 'Cable & Internet', 'Phone', 'Mortgage', 'Misc'],
        'Household':['Retail', 'Food', 'Clothes', 'Repair & Improvement', 'Alcohol', 'Misc'],
        'Entertainment':['Restaurants', 'Netflix DVD', 'Netflix Streaming', 'Video Games', 'Misc'],
        'Finance':['Cash', 'Account Transfer', 'Misc'],
        'Transportation':['Fuel', 'Maintenance & Repair', 'Misc'],
        'Income':['Dividend','Wages', 'Gift', 'Tax Refund', 'Cash Back', 'Misc'],
        'Health & Fitness': ['Dentist', 'Medical', 'Lab', 'Vet', 'Haircut', 'Misc'],
        'Investments': ['Vanguard', 'Misc'],
        'Taxes': ['Federal', 'State & Local', 'Property'],
        'UNCATEGORIZED':['Misc']
    }

    for key in tagDict.keys():
        for value in tagDict[key]:
            tag = Tag(category=key, subCategory=value )
            db.session.add(tag)
            db.session.commit()

def createAccountTypes():
    print('createAccounTypes()')

    types = ['Checking', 'Money Market', 'Credit Card']
    for type in types:
        accountType = AccountType(name=type)
        db.session.add(accountType)
        db.session.commit()


def setup():
    print('setup()')

    print('drop_all')
    db.drop_all()

    print('create_all')
    db.create_all()

    print('commit')
    db.session.commit()

    createAccountTypes()
    createCategories()

def testSetup():
    print('testSetup')

    # import name mappings
    parseNameMappings(db, '%s/%s' % (Config.BACKUP_FOLDER, 'nameMappings.csv'))

    parseData(db, '%s/%s' % (Config.UPLOAD_FOLDER, 'cc_sample.csv'), 'Credit Card')
    parseData(db, '%s/%s' % (Config.UPLOAD_FOLDER, 'mm_sample.csv'), 'Money Market')
    parseData(db, '%s/%s' % (Config.UPLOAD_FOLDER, 'check_sample.csv'), 'Checking')

    #parseNameMappings(db, '%s/%s' % (Config.BACKUP_FOLDER, 'nameMappings2.csv'))
    #parseData(db, '%s/%s' % (Config.UPLOAD_FOLDER, 'cc_sample2.csv'), 'Credit Card')

if __name__ == '__main__':
    setup()

    if len(sys.argv) > 1:
        testSetup()




