from datetime import datetime
from dateutil.parser import parse
from app.models import Entry,NameMapping, Tag
from config import Config


def parseData(db, fileName, accountType, parseExtra=False):
    with open(fileName) as file:
        data = file.readlines()[1:]
        for line in data:
            if line.strip():  # skip ws
                raw = line.strip()
                raw = raw.split(',')  # TODO only split on commas outsied of "'s
                raw = list(map(lambda x: x.replace('"', ''), raw))   #strip out "'s

                transDate = raw[0]
                transDate = datetime.strptime(transDate, '%m/%d/%Y')
                description = raw[2]
                postedDate = None
                checkNumber = None

                if accountType == 'Credit Card':
                    postedDate = raw[1]
                    postedDate = datetime.strptime(postedDate, '%m/%d/%Y')
                elif accountType in ['Money Market', 'Checking']:
                    checkNumber = raw[1]

                try:
                    debit = float(raw[3])
                except:
                    debit = 0.0
                try:
                    credit = float(raw[4])
                except:
                    credit = 0.0

                # try to map the desc to a name, else use desc for name
                name = description
                nameMapping = NameMapping.query.filter_by(description=description).first()
                if nameMapping:
                    name = nameMapping.name

                # set existing categories - assume all have already been set, can't have 2 entries with the same
                # description with different categories
                tag_id = (Tag.query.filter_by(category='UNCATEGORIZED').first()).id
                existingEntry = Entry.query.filter_by(description=description).first()
                if existingEntry:
                    if existingEntry.tag_id:
                        tag_id = existingEntry.tag_id

                # reading backupd up data, grab extra fields (name, tag) TODO: how does this meld with the nameMapping?
                if parseExtra:
                    name = raw[5]
                    tag = raw[6]
                    category = tag.split(':')[0]
                    subcategory = tag.split(':')[1]
                    #print(name,category,subcategory)
                    tag_id = (Tag.query.filter_by(category=category).filter_by(subCategory=subcategory).first()).id


                entry = Entry(date=transDate, posted_date=postedDate, check_number=checkNumber, name=name,
                              description=description, debit=debit, credit=credit, account_type=accountType,
                              tag_id=tag_id)
                try:
                    db.session.add(entry)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
                #    raise
                #finally:
                #    db.session.close()  # optional, depends on use case

def parseNameMappings(db, fileName):
    try:
        with open(fileName) as file:
            data = file.readlines()[1:]
            for line in data:
                if line.strip():  # skip ws
                    raw = line.strip() # strip newline chars
                    raw = raw.split(',')  # TODO only split on commas outsied of "'s
                    raw = list(map(lambda x: x.replace('"', ''), raw))  # strip out "'s

                    description = raw[0]
                    name = raw[1]
                    #print(description,name)

                    nameMapping = NameMapping(description=description, name=name)
                    try:
                        db.session.add(nameMapping)  # will fail if description already exists
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        db.session.rollback()
    except FileNotFoundError:
        print('File does not exist:', fileName)


