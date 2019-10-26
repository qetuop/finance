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
    print(db.session)
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
    parent_id = db.Column(db.Integer)  # 0 = top level cat, # = sub-cat
    entries = db.relationship('Entry', backref='category_assoc', lazy='dynamic')
