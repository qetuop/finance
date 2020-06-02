import math

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_wtf.file import FileField, FileRequired
from app import app, db
from app.forms import EntryForm, AliasForm, CategoryForm, SummaryForm
#from flask_login import current_user, login_user, logout_user, login_required
from app.models import Entry, Tag, NameMapping
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from .my_parser import parseData
from .my_writter import backupData
from .my_reader import restoreData
from config import Config
import sys
import os
from datetime import datetime, timedelta
import json
from .forms import PlainTextWidget

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():

    #parseData(db, 'cc_sample.csv', 'Credit Card')
    #parseData(db, 'mm_sample.csv', 'Money Market')
    #parseData(db, 'check_sample.csv', 'Checking')
    entries = Entry.query.all()
    #print(entries[0].description)
    #print(entries[1].description)

    form = EntryForm()

    accountList = [('0', 'Money Market'), ('1', 'Credit Card'),
                   ('2', 'Checking')]  # id must be a str? else validate_on_submit will be False? why or use coerce=int?
    form.accountType.choices = accountList

    if request.method == 'GET':
        print('GET')
    elif request.method == 'POST':
        print('POST')
        #if form.validate_on_submit():  # do i need this?
        if form.backup.data:
            print('EXPORT DATA:')
            backupData(db)

        elif form.restore.data:
            print('IMPORT DATA:')
            restoreData(db)

        elif form.submit.data:
            print('Upload DATA:')
            # do this instead?  https://flask-wtf.readthedocs.io/en/stable/form.html#module-flask_wtf.file

            # TODO create a route to handle the upload/parse
            # check if the post request has the file part
            if 'file' not in request.files:  # file or files?
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']

            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                # save the file from ?the browser's cache? to a known dir so that it can be read
                # the file object, werkzeug.FileStorage, does not have the full path or ?knows it?
                file.save(os.path.join(Config.UPLOAD_FOLDER, filename))

                print('file:',filename, form.accountType.data)
                filename = '%s/%s' % (Config.UPLOAD_FOLDER, filename)
                if int(form.accountType.data) == 0:
                    parseData(db, filename, 'Money Market')
                elif int(form.accountType.data) == 1:
                    parseData(db, filename, 'Credit Card')
                elif int(form.accountType.data) == 2:
                    parseData(db, filename, 'Checking')
                return redirect('/')

    return render_template('index.html', title='Home', form=form, entries=entries)

@app.route('/alias/<id>', methods=['GET', 'POST'])
def alias(id):
    entry = Entry.query.filter_by(id=id).first()
    origName = entry.name
    origDesc = entry.description
    form = AliasForm(obj=entry)

    #form.exactMatch.data = True

    # set to be "read only"
    #setattr(getattr(form, 'description'), 'widget', PlainTextWidget())

    '''
    fields = [val for val in form._fields]
    for fieldName in fields:
        fieldProp = getattr(form, fieldName)
        setattr(fieldProp, 'widget', PlainTextWidget())
    '''
    if form.validate_on_submit():
        # The user pressed the "Submit" button
        if form.submit.data:
            matchDesc = form.description.data
            newName   = form.name.data

            print('submit NEW name:{}, Orig desc:{}, match Desc:"{}"'.format(newName, origDesc, matchDesc))
            #entries = Entry.query.filter_by(name=form.name.data).all()

            # TODO: fix toggle -> have it populate the match field
            #exactMatch = form.exactMatch.data
            exactMatch = (matchDesc == origDesc)

            # update ALL entries whose NAME = this entry's NAME   TODO: is this what i want? entires with different descriptions
            # could then map to the same name and future changes to one would change them all
            #rows_changed = Entry.query.filter_by(name=origName).update(dict(name=form.name.data))

            # Or match to entries whose DESCRIPTION matches
            rows_changed = 0
            if exactMatch:
                rows_changed = Entry.query.filter_by(description=origDesc).update(dict(name=newName))
                db.session.commit()
            else:
                rows_changed = Entry.query.filter(Entry.description.ilike(r"%{}%".format(matchDesc)))\
                    .update(dict(name=newName), synchronize_session=False)
                # can also use  .update({"name":"second"}, synchronize_session=False)
                db.session.commit()

            print('rows_changed:',rows_changed)

            # add to NameMapping table
            # TODO: do this better?


            # Does it already exist
            nameMapping = NameMapping.query.filter_by(description=matchDesc).first()
            print("NameMapping:{}, exact match:{}".format(nameMapping, exactMatch))

            # add mapping if no row in table with this description
            if nameMapping is None:
                nameMapping = NameMapping(description=matchDesc, name=newName, exact_match=exactMatch)
                db.session.add(nameMapping)
            # else update existing mapping
            else:
                rows_changed = NameMapping.query.filter_by(description=matchDesc).update(dict(name=newName))
                print('rc:', rows_changed)

            print('commit mapping')
            db.session.commit()

            return redirect(url_for('index'))
        # The user pressed the "Cancel" button
        else:
            return redirect(url_for('index'))

    return render_template('alias.html', form=form, entry=entry)

# this is used to populate the subcategory dropdown
@app.route('/subcategory/<category>')
def subcategory(category):
    print('subcategory:', category)
    tags = Tag.query.filter_by(category=category).all()

    tagArray = []

    for tag in tags:
        tagObj = {}
        tagObj['id'] = str(tag.id)
        tagObj['subCategory'] = tag.subCategory
        tagArray.append(tagObj)

    return jsonify({'tags': tagArray})



# An entry will be passed in by id
# get list of all tags and create the two drop downs
# set the category DD to the entry's tag
# set the subCat to that Cat's items
@app.route('/tag/<id>', methods=['GET', 'POST'])
def tag(id):
    print("tag request:",request)


    entry = Entry.query.filter_by(id=id).first()
    print('entry:', entry.id,entry.name, entry.tag_id)
    entryTag = Tag.query.filter_by(id=entry.tag_id).first()

    # TODO: not sure how this happened, need to invistagate
    if entryTag == None:
        entryTag = Tag.query.filter_by(category='UNCATEGORIZED').first()

    print(entryTag.category, entryTag.subCategory)

    form = CategoryForm()
    form.description.data = entry.description


    tags = Tag.query.all()

    # create a unique list of categories
    tagList = [tag.category for tag in tags]
    tagList = list(set(tagList))
    tagList.sort()
    print('cat:',tagList)

    # TODO should i use the actual id? (value, label)
    #categoryList = list((map(lambda x: x.name, categories)))
    categoryList = [(tag, tag) for tag in tagList]    # id must be a str? else validate_on_submit will be False? why or use coerce=int?
    form.category.choices = categoryList

    # create the sub cat list for the entrie's tag
    tags = Tag.query.filter_by(id=entry.tag_id).all()
    print('tags:',tags)
    tagList = [tag.subCategory for tag in tags]
    tagList = list(set(tagList))
    tagList.sort()
    print('sub:',tagList)


    subCategoryList = [(tag, tag) for tag in tagList]
    print(subCategoryList)
    form.subCategory.choices = subCategoryList



    if request.method == 'GET':
        print('GET')
        print(form.category.data)
        form.category.data = entryTag.category
        form.subCategory.data = entryTag.subCategory

    elif request.method == 'POST':
        print('POST',form.submit.data, form.validate_on_submit())
        print('form.submit.data: Name:{}, Category:{}*, Sub:{}*, Desc:{}*'.format(form.name.data, form.category.data, form.subCategory.data, form.description.data))
        #if form.validate_on_submit():
            # The user pressed the "Submit" button
            #print('validate_on_submit')
        if form.submit.data:
            print('form.submit.data:', form.name.data, form.category.data, form.subCategory.data)
            rows_changed = Entry.query.filter_by(name=entry.name).update(dict(tag_id=form.subCategory.data))
            print(rows_changed)
            db.session.commit()

            return redirect(url_for('index'))

        # The user pressed the "Cancel" button
        else:
            return redirect(url_for('index'))
    '''
    # put down here or causes validate not to work
    print('entries id:',entry.category_id)
    subCat = Category.query.filter_by(id=entry.category_id).first()
    parCat = 0
    if subCat and (subCat.parent_id != 0):
        parCat = Category.query.filter_by(id=subCat.parent_id).first().id
    print('set drop down to:', parCat)
    form.category.default = parCat #7 # using number works with process()
    form.process()

    # https://youtu.be/I2dJuNwlIH0?t=69
    # https: // github.com / PrettyPrinted / dynamic_select_flask_wtf_javascript
    # form.subCategory.choices = [(subCat.id,subCat.name) for subCat in .....some DB query]
    '''
    return render_template('category.html', form=form, entry=entry)

@app.route('/summary', methods=['GET', 'POST'])
def summary():
    form = SummaryForm()
    return render_template('summary.html', form=form)

'''
# create a dictonary of totals/?avgs? for each cat/subcat of a given date range
 { "period':30,
   "categories": {
        "Bills": {"total":100, "Electric": 40, "Water":60},
        "Entertainent": {total":200, "Resteraut": 120, "Netflix": 80}
    }
 }
 use a tuple instead "Water":(total, Daily, weekly, monthly, yearly)
'''
def getTotals(startDate, endDate):
    amountsDict = {}
    DAY = 1
    WEEK = 7
    MONTH = 30
    YEAR = 365

    period = (endDate - startDate).days + 1;
    amountsDict['period'] = period

    # fill in the tags from the DB
    tags = Tag.query.all()

    # create a unique list of categories - TODO: better way to do this?  Don't use the taglist from setup.py
    tagList = [tag.category for tag in tags]
    tagList = list(set(tagList))
    tagList.sort()
    amountsDict['categories'] = {}

    for category in tagList:
        subcats = Tag.query.filter_by(category=category)
        subcatDict = {tag.subCategory:(0,0,0,0,0) for tag in subcats}
        subcatDict['aggregate'] = (0,0,0,0,0)
        amountsDict['categories'][category] = subcatDict

    #print(amountsDict)
    #print(amountsDict['categories']['Bill']['Car Insurance'])

    entries = Entry.query.filter(Entry.date <= endDate).filter(Entry.date >= startDate)\
                          .filter((Entry.credit != 0) | (Entry.debit != 0)).all()
    total = 0
    for entry in entries:

        # sub cat values
        tmpAmount = abs(entry.getAmount())
        prevAmount = amountsDict['categories'][entry.getCategory()][entry.getSubCategory()]
        newAmount = tmpAmount + prevAmount[0]

        # (total, Daily, weekly, monthly, yearly)
        vals = (newAmount, round(newAmount/period*DAY,2), round(newAmount/period*WEEK,2), round(newAmount/period*MONTH,2), round(newAmount/period*YEAR),2)
        amountsDict['categories'][entry.getCategory()][entry.getSubCategory()] = vals

        # Category Aggregate (ex: All Bills)
        prevAmount = amountsDict['categories'][entry.getCategory()]['aggregate']  # the total agg of the tuple
        newAmount = tmpAmount + prevAmount[0]
        vals = (newAmount, round(newAmount/period*DAY,2), round(newAmount/period*WEEK,2), round(newAmount/period*MONTH,2), round(newAmount/period*YEAR),2)
        amountsDict['categories'][entry.getCategory()]['aggregate'] = vals

    # TODO: remove 0 amount entries

    return amountsDict


@app.route('/summary_table', methods=['GET', 'POST'])
def summary_table(data=None):
    print("summary", request.method, request.args, data)
    amountsDict = {}

    print(request)
    start = request.args.get('start')
    end = request.args.get('end')

    if start == None:
        startDate = datetime.today() - timedelta(days=30)
        endDate =  datetime.today()
    else:
        #print('start:', start)
        #print('end:', end)
        # TODO: verify this
        startDate = datetime.fromtimestamp(int(start)/1000)
        endDate = datetime.fromtimestamp(int(end)/1000)

    amountsDict = getTotals(startDate,endDate)


    # get start, end date for range from datepicker - if none provided use today/-31days
    #startDate = request.args.get('start', datetime.today() - timedelta(days=31))
    #endDate = request.args.get('end', datetime.today())
    print(startDate.date(),'---',endDate.date())
    '''
    # get current date
    #endDate = datetime.now()
    #startDate = datetime.today() - timedelta(days=range)

    # get all Entries from last XX days
    entries = Entry.query.filter(Entry.date <= endDate).filter(Entry.date  >= startDate).all()
    #print(entries)

    # get categories
    tags = Tag.query.all()

    # create a unique list of categories
    tagList = [tag.category for tag in tags]
    tagList = list(set(tagList))
    tagList.sort()
    #print('cat:', tagList)

    # create dict of category : [<entry>]
    tagEntryDict = dict.fromkeys(tagList,[])
    for category in tagList:
        tagEntryDict[category] = Entry.query\
                                      .join(Tag)\
                                      .filter_by(category=category)\
                                      .filter(Entry.date <= endDate).filter(Entry.date >= startDate)\
                                      .all()

    print('tagEntryDict:',tagEntryDict)

    # sum up the amounts
    # quick hack data storage
    data = {}
    for category in tagEntryDict.keys():
        amount = 0.0
        for entry in tagEntryDict[category]:
            amount += abs(entry.getAmount())       # may need abs values for charts

        print(category,tagEntryDict[category], amount)

        # don't need to display zero values
        if amount > 0:
            data[category] = amount

    '''
    form = SummaryForm()


    return render_template('summary_table.html', form=form, data=amountsDict)  # the base.html references the form object, always pass one?
    #return render_template('summary_table.html', form=form, data=data)  # the base.html references the form object, always pass one?