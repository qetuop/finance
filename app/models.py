from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
from app import db
'''
entry_category = db.Table('entry_category',
                          db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'), nullable=False),
                          db.Column('category_id', db.Integer, db.ForeignKey('category.id'), nullable=False),
                          db.PrimaryKeyConstraint('entry_id', 'category_id'))
'''

# sqlalchemy.types.DateTime
# Date and time types return objects from the Python datetime module. Most DBAPIs have built in support for the datetime
# module, with the noted exception of SQLite. In the case of SQLite, date and time types are stored as strings which are
# then converted back to datetime objects when rows are returned.
# input= "4/28/2020" --> datetime.strptime(transDate, '%m/%d/%Y') = datetime object (2020-04-28 00:00:00) and various fields
# --> sqlalchemy. DateTime = Depends SQLite vs Other DBs  --> Back out = datetime

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)  # transaction for CC
    posted_date = db.Column(db.DateTime)  # CC only
    check_number = db.Column(db.Integer)  # checking/MM   TODO: should this be a string?  values are '00000000163'
    name = db.Column(db.String(120))  # user entered name
    description = db.Column(db.String(120))  # bank entered name
    debit = db.Column(db.Float)
    credit = db.Column(db.Float)
    account_type = db.Column(db.String(120))

    __table_args__ = (db.UniqueConstraint("date", "description", 'debit', 'credit'),) # must be tuple, don't remove comma

    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

    def getAmount(self):
        sign = 1
        # CC debit = -
        # CC credit = +
        # checking debit = -
        # checking credit = +
        # mm debit = -
        # mm credit = +
        if self.debit > 0.0:
            return -1*self.debit
        else:
            return self.credit


    '''
    def __init__(self, **kwargs):
        super(Entry, self).__init__(**kwargs)
        print('here')
    '''

    def displayTag(self):
        out = 'none'
        tag = Tag.query.filter_by(id=self.tag_id).first()
        if tag:
            out = '{}:{}'.format(tag.category,tag.subCategory)

        return out


class NameMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120))  # bank entered name
    name = db.Column(db.String(120))  # user entered name
    exact_match = db.Column(db.Boolean(), default=True)

    __table_args__ = (
        db.UniqueConstraint("description"),
    )

class AccountType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(120))
    subCategory = db.Column(db.String(120))

    entries = db.relationship('Entry', backref='category_assoc', lazy='dynamic')

    __table_args__ = (
    db.UniqueConstraint("category", "subCategory"),)  # must be tuple, don't remove comma

    def checkCategory(cat, sub=None):
        id = None

        print('addCategory:',cat,sub)
        # does cat currently exist
        catExists = db.session.query(db.exists().where(Category.name == cat)).scalar()
        print(cat, ':', catExists)

        # if exists, check sub
        if catExists:

            if sub:
                subExists = db.session.query(db.exists().where(Category.name == cat)).scalar()
                print(sub, ':', subExists)
            else:
                id = cat

        # Cat does not exist return None
        else:
            pass

    def catExistsByName(cat):
        print(cat)
        return Category.query.filter_by(name=cat).first()


    def existsById(cat=None, sub=None):
        exists = Category.query.filter_by(id=sub,parent_id=cat).first()
        print(exists)

    '''
    Expected input/Output:
    ('Bill') --> None, cat does not exist, add and will get id=1
    ('Bill') --> 1, cat does  exist
    ('Bill', 'Water') --> None or 1?, subCat does not exist, add and get id=2
    ('Bill', 'Water') --> 2?, subCat does exist, add and get id=2
    ('Bill', 'Electric')
    ('Finance', '401K') --> None, cat AND subCat don't exist, will need to ???
    
    not expected
    ('Water') -> with an expectation it would find an existing Bill:Water
    this would create a new Category Water
    '''
    def existsByName(cat, sub=None):
        id = None
        print('existsByName:', cat,sub)
        category = Category.query.filter_by(name=cat).first()
        subCategory = Category.query.filter_by(name=sub).first()
        print(category)
        print(subCategory)

        # category already exists, check subCat
        if category:
            # if a subCat name was passed in and subCat exists return its id
            if sub and subCategory:
                id = subCategory.id
            # else no subCat name was passed or
            else:
                pass

        # category does not exist, OK to add, return None
        else:
            pass

        return id



        #print('entries:', len(category.entries.all()))
        #print('{}:{} - {}:{}'.format(cat,category.id,sub,subCategory.id))

        #existing = Category.query.join(Category.entries).filter(Category.name == cat, Category.name == sub).first()
        #print(existing)
        #if existing != None:
        #    print('Exists')


        #exists = Category.query.filter_by(id=subCategory).filter_by(parent_id=category)
        #print(exists)
