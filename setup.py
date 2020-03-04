from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app.models import NameMapping, Tag, Entry, AccountType
from app.my_parser import parseData
from app import db

#app = Flask(__name__)
#app.config.from_object(Config)
#db = SQLAlchemy(app)

db.drop_all()
db.create_all()
db.session.commit()

def createCategories():
    tagDict = {
        'Bill':['Electric','Water', 'HOA', 'Car Insurance', 'Credit Card Payment', 'Cable & Internet', 'Phone', 'Mortgage', 'Misc'],
        'Household':['Retail', 'Food', 'Repair & Improvement', 'Misc'],
        'Entertainment':['Restaurants', 'Netflix DVD', 'Netflix Streaming', 'Misc'],
        'Finance':['Cash', 'Account Transfer', 'Misc'],
        'Transportation':['Fuel', 'Maintenance & Repair', 'Misc'],
        'Income':['Wages', 'Gift', 'Tax Refund', 'Cash Back', 'Misc'],
        'Health & Fitness': ['Dentist', 'Medical', 'Lab', 'Vet', 'Misc'],
        'Investments': ['Vanguard', 'Misc'],
        'UNCATEGORIZED':['Misc']
    }

    for key in tagDict.keys():
        for value in tagDict[key]:
            tag = Tag(category=key, subCategory=value )
            db.session.add(tag)
            db.session.commit()

def createAccounTypes():
    types = ['Checking', 'Money Market', 'Credit Card']
    for type in types:
        accountType = AccountType(name=type)
        db.session.add(accountType)
        db.session.commit()


if __name__ == '__main__':
    createAccounTypes()
    createCategories()

    parseData(db, 'cc_sample.csv', 'Credit Card')
    parseData(db, 'mm_sample.csv', 'Money Market')
    parseData(db, 'check_sample.csv', 'Checking')




