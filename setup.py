from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app.models import NameMapping, Category, Entry
from app.my_parser import parseData
from app import db

#app = Flask(__name__)
#app.config.from_object(Config)
#db = SQLAlchemy(app)



db.drop_all()
db.create_all()
db.session.commit()

def addCat(cat, sub=None):
    category = Category.catExistsByName(cat)
    retCat = None
    if category is None:
        newCat = Category(name=cat, parent_id=0)
        db.session.add(newCat)
        db.session.commit()
        print(newCat, 'added, id=', newCat.id)
        retCat = newCat

        if sub:
            newCat = Category(name=sub, parent_id=newCat.id)
            db.session.add(newCat)
            db.session.commit()
            print(cat, sub, 'added, id=', newCat.id)

def createCategories():
    dict = {'Bill':['Electric','Water', 'HOA', 'Car Insurance', 'Credit Card Payment'],
            'Household':['Retail', 'Food'],
            'Entertainment':['Restaurants', 'Netflix DVD', 'Netflix Streaming'],
            'Finance':['Mortgage', 'Cash Withdrawl', 'Account Transfer'],
            'Transportation':[],
            'Income':[],
            'Health & Fitness': ['Dentist', 'Doctor', 'Lab', 'Vet'],
            'UNCATEGORIZED':[],
            'Other':[]}

    for key in dict.keys():
        subCats = dict[key]
        cat = Category(name = key, parent_id = 0)
        db.session.add(cat)
        db.session.commit()

        for subCat in subCats:
            sc = Category(name=subCat, parent_id=cat.id)
            db.session.add(sc)
            db.session.commit()

def setupCat():

    # ('Bill') --> None, cat does not exist, add and will get id=1
    name = 'Bill'
    sub = None
    category = Category.catExistsByName(name)
    if category is None:
        cat = Category(name=name, parent_id=0)
        db.session.add(cat)
        db.session.commit()
        print(name, 'added, id=', cat.id)

    # ('Bill') --> 1, cat does  exist
    name = 'Bill'
    sub = None
    category = Category.catExistsByName(name)
    if category is None:
        print(name, '0 should not happen')

    # ('Bill', 'Water') --> None or 1?, subCat does not exist, add and get id=2
    name = 'Bill'
    sub = 'Water'
    category = Category.catExistsByName(name)
    if category is None:
        print(name, '1 should not happen')
    else:
        if Category.catExistsByName(sub) is None:
            cat = Category(name=sub, parent_id=category.id)
            db.session.add(cat)
            db.session.commit()
            print(name,sub, 'added, id=', cat.id)

    # ('Bill', 'Water') --> 2?, subCat does exist, add and get id=2
    name = 'Bill'
    sub = 'Water'
    category = Category.catExistsByName(name)
    if category is None:
        print(name, '2 should not happen')
    else:
        if Category.catExistsByName(sub) is None:
            print(name, '3 should not happen')
        else:
            print(name,sub, 'already exists')

    # ('Finance', '401K') --> None, cat AND subCat don't exist, will need to ???
    name = 'Finance'
    sub = '401K'
    category = Category.catExistsByName(name)
    if category is None:
        cat = Category(name=name, parent_id=0)
        db.session.add(cat)
        db.session.commit()
        print(name, 'added, id=', cat.id)

        # 401K could exist as just a cat but not as a sub to Finance since Finance was just added
        cat = Category(name=sub, parent_id=cat.id)
        db.session.add(cat)
        db.session.commit()
        print(name, sub, 'added, id=', cat.id)

    # ('Water') --> a new Category, already exists as a *subCategory*
    name = 'Water'
    sub = None
    category = Category.catExistsByName(name)
    if category is None:
        print('5 should not happen')
    else:
        print('need to handle')

        # ok to add as new cat --> how to handle queries now??!?
        # Not allow this case?
        if category.parent_id != 0:
            cat = Category(name=name, parent_id=0)
            db.session.add(cat)
            db.session.commit()
            print(name, 'added, id=', cat.id)


    '''
    # ('Bill', 'Electric')
    name = 'Bill'
    sub = 'Electric'
    category = Category.catExistsByName(name)
    if category is None:
        print(name, '4 should not happen')
    else:
        if Category.catExistsByName(sub) is None:
            cat = Category(name=sub, parent_id=category.id)
            db.session.add(cat)
            db.session.commit()
            print(name,sub, 'added, id=', cat.id)
    '''






if __name__ == '__main__':
    createCategories()
    categories = Category.query.filter_by(parent_id=0).all()
    cats = list((map(lambda x: x.name, categories)))
    print(cats)

    #setupCat()


    nameMapping = NameMapping(description='Dividend', name='div')
    try:
        db.session.add(nameMapping)
        db.session.commit()
    except Exception as e:
        db.session.rollback()


    parseData(db, 'cc_sample.csv', 'Credit Card')
    parseData(db, 'mm_sample.csv', 'Money Market')
    parseData(db, 'check_sample.csv', 'Checking')

    entry = Entry(name='bar', description='test',category_id=9)
    db.session.add(entry)
    db.session.commit()

    entry = Entry(name='foo', description='test2', category_id=7)
    db.session.add(entry)
    db.session.commit()


    '''
    cat1 = Category(name='Bill',parent_id=0)
    db.session.add(cat1)
    db.session.commit()
    cat2 = Category(name='Water',parent_id=cat1.id)
    db.session.add(cat2)
    db.session.commit()

    entry = Entry( name='bar', description='test')
    db.session.add(entry)
    db.session.commit()

    entry = Entry.query.filter_by(name='bar')
    entry.category_id = cat2.id
    entry.name = 'FOOBAR'
    #Entry.query.first().update(dict(category_id=cat2.id)) doesn't work
    rows_changed = Entry.query.filter_by(name='bar').update(dict(category_id=cat2.id))
    rows_changed = Entry.query.filter_by(name='bar').update(dict(name='FOOBAR'))

    print(rows_changed)
    #db.session.add(entry)
    db.session.commit()

    cat3 = Category(name='Finance', parent_id=0)
    db.session.add(cat3)
    db.session.commit()


    entry3 = Entry(name='car')
    entry3.category_id = cat3.id
    db.session.add(entry3)
    db.session.commit()

    description='test'
    category_id = None
    existingEntry = Entry.query.filter_by(description=description).first()
    if existingEntry:
        if existingEntry.category_id:
            category_id = existingEntry.category_id

    entry = Entry(name='catcopy',category_id=category_id)
    db.session.add(entry)
    db.session.commit()

    cat = Category(name='Bill',parent_id=0)
    tmpCat = Category.query.filter_by(name=cat.name).first()
    if tmpCat:
        cat = tmpCat
    else:
        db.session.add(cat)
        db.session.commit()

    exists = db.session.query(Category).filter_by(name='Bill').scalar() is not None
    print('a:',exists)
    exists = db.session.query(db.exists().where(Category.name == 'Bill')).scalar()
    print('b:', exists)

    q = db.session.query(Category).filter(Category.name == 'Bill')
    print('here:',db.session.query(q.exists()))
    #db.session.query(Category.id).filter(q.exists()).scalar()

    #exists = Category.query(exists().where
    #print(Category.query.filter_by(db.exists().where(Category.name == cat.name)).one())

    entry = Entry(name='test2')
    entry.category_id = cat.id
    db.session.add(entry)
    db.session.commit()

    print(Category.existsByName('Bill','Water'))
    '''




