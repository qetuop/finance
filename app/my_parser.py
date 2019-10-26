from datetime import datetime
from dateutil.parser import parse
from app.models import Entry,NameMapping
from config import Config

def parseData(db, fileName, accountType):
    with open('%s/%s'% (Config.UPLOAD_FOLDER,fileName)) as file:
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
                    print(nameMapping.name)
                    name = nameMapping.name

                entry = Entry(date=transDate, posted_date=postedDate, check_number=checkNumber, name=name,
                              description=description, debit=debit, credit=credit, account_type=accountType)
                try:
                    db.session.add(entry)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
                #    raise
                #finally:
                #    db.session.close()  # optional, depends on use case


