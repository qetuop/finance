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

if __name__ == '__main__':
    print(__name__)

    nameMapping = NameMapping(description='Dividend', name='div')
    try:
        db.session.add(nameMapping)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    parseData(db, 'cc_sample.csv', 'Credit Card')
    parseData(db, 'mm_sample.csv', 'Money Market')
    parseData(db, 'check_sample.csv', 'Checking')

    cat1 = Category(name='Bill')
    db.session.add(cat1)
    db.session.commit()
    cat2 = Category(name='Water',parent_id=cat1.id)
    db.session.add(cat2)
    db.session.commit()

    entry = Entry( name='bar')
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

    cat3 = Category(name='Finance')
    db.session.add(cat3)
    db.session.commit()
    entry3 = Entry(name='car')
    entry3.category_id = cat3.id
    db.session.add(entry3)
    db.session.commit()
    #rows_changed = Entry.query.filter_by(name='car').update(dict(category_id=cat3.id))
