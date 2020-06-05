from datetime import datetime
from dateutil.parser import parse
from app.models import Entry,NameMapping, Tag, TagNameMapping
from config import Config
from  distutils import util

def parseData(db, fileName, accountType):
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

                # NAME MAPPING

                # try to map the desc to a name, else use desc for name
                name = description
                print("\ntyring to map:", description)

                # First try for an exact match, if found continue to next
                nameMapping = NameMapping.query.filter_by(description=description).filter(NameMapping.exact_match == True).first()

                if nameMapping:
                    name = nameMapping.name
                    print("exact found: this desc:{}, mapping's desc:{}, mapping's name:{}".format(description,
                                                                                                   nameMapping.description,
                                                                                                   nameMapping.name))

                # search all partial mappings
                else:
                    nameMappings = NameMapping.query.filter_by(exact_match=False)
                    for partialMatch in nameMappings:

                        search = partialMatch.description
                        print("search:", search)

                        '''
                        # this is wrong, keeping as example how to do a search
                        #nameMapping = NameMapping.query.filter(NameMapping.description.ilike(r"%{}%".format(search))).filter(NameMapping.exact_match == False).first()
                        
                        can something like (but not this) work? ilike is a sqlalch thing?
                        nameMapping = NameMapping.query.filter(search.ilike(r"%{}%".format(nameMapping.description))).filter(NameMapping.exact_match == False).first()
                        if nameMapping:
                            print("A: partial found", nameMapping.description, nameMapping.name)
                        '''
                        if search in description:
                            print("B: partial found for search: ", search)
                            name = partialMatch.name
                        else:
                            print("NO MATCH FOUND, using search: ", search)

                # TAGS / CATEGORIES

                # default
                tag_id = (Tag.query.filter_by(category='UNCATEGORIZED').first()).id

                # search TagNameMapping for existing Name:tag
                tagNameMapping = TagNameMapping.query.filter_by(name=name).first()
                print(TagNameMapping.query.first())
                print("TAG SEARCH: name={}, found = {}".format(name,tagNameMapping))
                if tagNameMapping:
                    print("tagNameMapping:", tagNameMapping.name, tagNameMapping.tag)
                    (category,subCategory) = tagNameMapping.tag.split(':')
                    existsingId = (Tag.query.filter_by(category=category, subCategory=subCategory)).first().id
                    print('existsingId:',existsingId)
                    if existsingId:
                        tag_id = existsingId


                '''
                existingEntry = Entry.query.filter_by(description=description).first()
                if existingEntry:
                    if existingEntry.tag_id:
                        tag_id = existingEntry.tag_id
                '''
                '''
                # reading backupd up data, grab extra fields (name, tag) TODO: how does this meld with the nameMapping?
                if parseExtra:
                    name = raw[5]
                    tag = raw[6]
                    category = tag.split(':')[0]
                    subcategory = tag.split(':')[1]
                    #print(name,category,subcategory)
                    tag_id = (Tag.query.filter_by(category=category).filter_by(subCategory=subcategory).first()).id
                '''

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
    print('parseNameMappings')
    try:
        with open(fileName) as file:
            data = file.readlines()[1:]
            for line in data:
                if line.strip():  # skip ws
                    #raw = line.strip() # strip newline chars
                    #raw = raw.split(',')  # TODO only split on commas outsied of "'s
                    raw = [x.strip().replace('"', '') for x in line.split(',')] # this should remove spaces after a comma and replace " with space
                    #raw = list(map(lambda x: x.replace('"', ''), raw))  # strip out "'s   TODO: this is messed up by spaces after commas "foo", "bar"  != "foo","bar"
                    print(raw)
                    description = raw[0]
                    name = raw[1]
                    exact_match = bool(util.strtobool(raw[2]))

                    nameMapping = NameMapping(description=description, name=name, exact_match=exact_match)
                    try:
                        db.session.add(nameMapping)  # will fail if description already exists
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        db.session.rollback()
    except FileNotFoundError:
        print('File does not exist:', fileName)

def parseTagNameMappings(db, fileName):
    print('parseTagNameMappings')
    try:
        with open(fileName) as file:
            data = file.readlines()[1:]
            for line in data:
                if line.strip():  # skip ws
                    #raw = line.strip() # strip newline chars
                    #raw = raw.split(',')  # TODO only split on commas outsied of "'s
                    raw = [x.strip().replace('"', '') for x in line.split(',')] # this should remove spaces after a comma and replace " with space
                    #raw = list(map(lambda x: x.replace('"', ''), raw))  # strip out "'s   TODO: this is messed up by spaces after commas "foo", "bar"  != "foo","bar"
                    print(raw)
                    name = raw[0]
                    tag = raw[1]

                    tagNameMapping = TagNameMapping(name=name, tag=tag)

                    try:
                        db.session.add(tagNameMapping)  # will fail if already exists
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        db.session.rollback()
    except FileNotFoundError:
        print('File does not exist:', fileName)
