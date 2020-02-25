from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
from app import db
'''
entry_category = db.Table('entry_category',
                          db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'), nullable=False),
                          db.Column('category_id', db.Integer, db.ForeignKey('category.id'), nullable=False),
                          db.PrimaryKeyConstraint('entry_id', 'category_id'))
'''

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)  # transaction for CC
    posted_date = db.Column(db.DateTime)  # CC only
    check_number = db.Column(db.Integer)  # checking/MM
    name = db.Column(db.String(120))  # user entered name
    description = db.Column(db.String(120))  # bank entered name
    debit = db.Column(db.Float)
    credit = db.Column(db.Float)
    account_type = db.Column(db.String(120))

    __table_args__ = (db.UniqueConstraint("date", "description", 'debit', 'credit'),) # must be tuple, don't remove comma

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    '''
    def __init__(self, **kwargs):
        super(Entry, self).__init__(**kwargs)
        print('here')
    '''

    def getCategories(self):
        out = (None,None)
        category = Category.query.filter_by(id=self.category_id).first()
        if category:
            if category.parent_id:
                subCat = category
                category = Category.query.filter_by(id=subCat.parent_id).first()
                out = (category.name,subCat.name)
            else:
                out = (category.name,None)
        return out

    def getCategory(self):
        out = None
        category = Category.query.filter_by(id=self.category_id).first()
        if category:
            if category.parent_id:
                subCat = category
                category = Category.query.filter_by(id=subCat.parent_id).first()
                out = category.name
            else:
                out = category.name
        return out

    def getSubCategory(self):
        out = None
        category = Category.query.filter_by(id=self.category_id).first()
        if category:
            if category.parent_id:
                out = category.name
        return out

    def displayCategory(self):
        out = 'UNCATEGORIZED'
        category = Category.query.filter_by(id=self.category_id).first()
        if category:
            if category.parent_id:
                subCat = category
                category = Category.query.filter_by(id=subCat.parent_id).first()
                out = '{}:{}'.format(category.name,subCat.name)
            else:
                out = '{}'.format(category.name)

        return out


class NameMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120))  # bank entered name
    name = db.Column(db.String(120))  # user entered name
    __table_args__ = (
        db.UniqueConstraint("description", "name"),
    )


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    parent_id = db.Column(db.Integer, nullable=False)  # 0 = top level cat, # = sub-cat
    entries = db.relationship('Entry', backref='category_assoc', lazy='dynamic')

    __table_args__ = (
    db.UniqueConstraint("name", "parent_id"),)  # must be tuple, don't remove comma

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
