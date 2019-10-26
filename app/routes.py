from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import EntryForm, AliasForm, CategoryForm
#from flask_login import current_user, login_user, logout_user, login_required
from app.models import Entry, Category
from werkzeug.urls import url_parse
from .my_parser import parseData




@app.route('/')
@app.route('/index')
def index():

    #parseData(db, 'cc_sample.csv', 'Credit Card')
    #parseData(db, 'mm_sample.csv', 'Money Market')
    #parseData(db, 'check_sample.csv', 'Checking')
    entries = Entry.query.all()
    #print(entries[0].description)
    #print(entries[1].description)

    form = EntryForm()
    return render_template('index.html', title='Home', form=form, entries=entries)

@app.route('/alias/<id>', methods=['GET', 'POST'])
def alias(id):
    entry = Entry.query.filter_by(id=id).first()
    origName = entry.name
    form = AliasForm(obj=entry)

    if form.validate_on_submit():
        # The user pressed the "Submit" button
        if form.submit.data:
            print('submit', form.name.data)
            #entries = Entry.query.filter_by(name=form.name.data).all()
            rows_changed = Entry.query.filter_by(name=origName).update(dict(name=form.name.data))
            print(rows_changed)
            db.session.commit()
            return redirect(url_for('index'))
        # The user pressed the "Cancel" button
        else:
            return redirect(url_for('index'))

    return render_template('alias.html', form=form, entry=entry)

@app.route('/category/<id>', methods=['GET', 'POST'])
def category(id):
    entry = Entry.query.filter_by(id=id).first()
    form = CategoryForm()

    (cat,sub) = entry.getCategories()
    form.category.data = cat
    form.subCatagory.data = sub
    #form.category.

    if form.validate_on_submit():
        # The user pressed the "Submit" button
        if form.submit.data:
            print('submit', form.name.data)
            #rows_changed = Entry.query.filter_by(name=origName).update(dict(name=form.name.data))
            #print(rows_changed)
            #db.session.commit()
            return redirect(url_for('index'))
        # The user pressed the "Cancel" button
        else:
            return redirect(url_for('index'))

    return render_template('category.html', form=form, entry=entry)