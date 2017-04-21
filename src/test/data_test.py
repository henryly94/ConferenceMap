#!/usr/bin/python
import sys
import MySQLdb as ms

host = 'localhost'

user = 'eng'
pw = 'eng'
schema_1 = 'mag-new-160205'
schema_2 = 'acemap-abstract'

db_1 = ms.connect(host, user, pw, schema_1)
db_2 = ms.connect(host, user, pw, schema_2)
cursor_1 = db_1.cursor()
cursor_2 = db_2.cursor()

# sql = 'SELECT PaperID,Abstract from PaperAbstract LIMIT 100'
sql_get_conference = 'select Y.ShortName, Y.ConferenceSeriesID, Count(X.OriginalPaperTitle) as PaperAmt from Papers as X, ConferenceSeries as Y where Y.ConferenceSeriesID =  X.ConferenceSeriesIDMappedToVenueName Group By X.ConferenceSeriesIDMappedToVenueName Order by PaperAmt DESC Limit 1000;'

sql_get_papers = "SELECT PaperID, OriginalPaperTitle FROM Papers WHERE ConferenceSeriesIDMappedToVenueName='%s'"

sql_get_abstract = """select PaperAbstract.Abstract
    from IdId 
    join PaperAbstract
    on IdId.PaperID = PaperAbstract.PaperID                
    where IdId.MagPaperID = '%s'"""

infos = dict()

exist = cursor_1.execute(sql_get_conference)

conference_ids = cursor_1.fetchall()

# conference_ids = conference_ids[100:]
exist = len(conference_ids)

# conference_ids | infos | paper

with open('test_train.in', 'a') as f:
    for i in xrange(exist):
        confers = '%d / %d | ' % (i+1, exist)
        rec = conference_ids[i]
        assert len(rec) == 3
        short_name, conferid, paperamt = rec
        infos[conferid] = dict()
        infos[conferid]['short_name'] = short_name
        infos[conferid]['paper_amt'] = paperamt
        
        paper_amt = cursor_1.execute(sql_get_papers % conferid)
        
        papers = cursor_1.fetchall()

        for j in xrange(paper_amt):
            sys.stdout.write(confers + '%d / %d\r' % (j+1, paper_amt))
            sys.stdout.flush()
            paper_rec = papers[j]
            assert len(paper_rec) == 2
            paperid, papertitle = paper_rec
            cursor_2.execute(sql_get_abstract % paperid)

            new_abstract = cursor_2.fetchall()
            if len(new_abstract) == 0:
                continue
            new_abstract = new_abstract[0]

            f.write(new_abstract[0])
            f.write('\n')       
sys.stdout.write('\n')

cursor_1.close()
cursor_2.close()
db_1.close()
db_2.close()
