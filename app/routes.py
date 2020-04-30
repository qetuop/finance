from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_wtf.file import FileField, FileRequired
from app import app, db
from app.forms import EntryForm, AliasForm, CategoryForm
#from flask_login import current_user, login_user, logout_user, login_required
from app.models import Entry, Tag, NameMapping
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from .my_parser import parseData
from .my_writter import backupData
from .my_reader import restoreData
from config import Config

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
                print('file:',filename, form.accountType.data)
                flash('foo')
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
    form = AliasForm(obj=entry)

    if form.validate_on_submit():
        # The user pressed the "Submit" button
        if form.submit.data:
            print('submit new name:', form.name.data)
            #entries = Entry.query.filter_by(name=form.name.data).all()
            rows_changed = Entry.query.filter_by(name=origName).update(dict(name=form.name.data))
            print('rows_changed:',rows_changed)

            # add to NameMapping table
            # TODO: do this better?
            nameMapping = NameMapping.query.filter_by(description=entry.description).first()
            print("NameMapping:",nameMapping)
            if nameMapping is None:
                nameMapping = NameMapping(description=entry.description, name=form.name.data)
                db.session.add(nameMapping)

            else:
                rows_changed = NameMapping.query.filter_by(description=entry.description).update(dict(name=form.name.data))
                print('rc:', rows_changed)

            print('commit mapping')
            db.session.commit()

            return redirect(url_for('index'))
        # The user pressed the "Cancel" button
        else:
            return redirect(url_for('index'))

    return render_template('alias.html', form=form, entry=entry)

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
    entry = Entry.query.filter_by(id=id).first()
    print('entry:', entry.id,entry.name, entry.tag_id)
    entryTag = Tag.query.filter_by(id=entry.tag_id).first()
    print(entryTag.category, entryTag.subCategory)

    form = CategoryForm()


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
        print('form.submit.data:', form.name.data, form.category.data, form.subCategory.data)
        #if form.validate_on_submit():
            # The user pressed the "Submit" button
            #print('validate_on_submit')
        if form.submit.data:
            print('form.submit.data:', form.name.data, form.category.data, form.subCategory.data)
            rows_changed = Entry.query.filter_by(description=entry.description).update(dict(tag_id=form.subCategory.data))
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