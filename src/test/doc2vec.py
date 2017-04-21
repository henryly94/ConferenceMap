#!/usr/bin/python
import os
import re
import sys
import MySQLdb as ms
import numpy as np
from sklearn.manifold import TSNE
from sklearn.preprocessing import scale

# Args
assert len(sys.argv) == 7, "Usage:\n\tpython doc2vec.py path_docvec path_confer_vec, path_vocab, path_vector, path_cluster, path_cluster_mean"
path_doc_vec, path_confer_vec, path_vocab, path_vector, path_cluster, path_cluster_mean = sys.argv[1:7]


# Options
class option:

    vec_dim = 5000


opt = option()


def log(func):
    def _insider(*args):
        print 'running', func.__name__
        ret = func(*args)
        print 'finishing', func.__name__
        return ret
    return _insider

@log
def load_vocab(path):
    vocab_words = []
    with open(path, 'r') as f:
        for line in f:
            try:
                word, count = line.strip().split(' ')
                vocab_words.append(word)
            except ValueError:
                pass
    vocab_size = len(vocab_words)
    return vocab_words, vocab_size
vocab = load_vocab(path_vocab)

@log
def load_vector(path):
    embs = []
    with open(path, 'r') as f:
        for line in f:
            try:
                word, vec_str = line.strip().split('\t')
                embs.append(map(float, vec_str.split(' ')))
            except ValueError as detail:
                print("ValueError in loading vector:", detail)
                pass
    return embs
embs = load_vector(path_vector)

@log
def load_clusters(path):    
    word2cluster = dict()
    file_list = os.listdir(path)
    for each in file_list:
        if each in ['.', '..']: continue
        with open(os.path.join(path, each), 'r') as f:
            for line in f:
                try:
                    cluster_index, word = line.strip().strip('()').split(',')
                    word2cluster[word] = int(cluster_index)
                
                except ValueError as detail:
                    print("ValueEroro in loading clusters: ", detail)
                    pass
    return word2cluster


word2cluster = load_clusters(path_cluster)
print len(word2cluster), list(word2cluster)[:3]
def read_doc():
    pass


multiple_space = re.compile(r'\s+')
illegal_char = re.compile(r'[^A-Za-z]')


def wash_doc(raw):
    # Wash dirty data    
    clean = multiple_space.sub(
            " ",
            illegal_char.sub(' ', raw)
            )
    return clean


def gen_doc_vec(doc):
    global word2cluster
    new_doc_vec = [0.0 for _ in xrange(opt.vec_dim)]
    for word in doc:
        new_doc_vec[word2cluster.get(word, 0)] += 100

    new_doc_vec_scaled = scale(new_doc_vec).tolist()

    return new_doc_vec_scaled

@log
def write_doc_vec(doc_vecs, path):
    assert len(doc_vecs) > 0
    delim = " "
    with open(path, 'w') as f:
        for vec in doc_vecs:
            f.write(delim.join(map(str, vec)))
            f.write('\n')
    



def main():
    host = '202.120.36.137'
    port = 6033
    user = 'eng'
    pw = 'eng'
    schema_1 = 'mag-new-160205'
    schema_2 = 'acemap-abstract'

    db_1 = ms.connect(host, user, pw, schema_1, port=port)
    db_2 = ms.connect(host, user, pw, schema_2, port=port)
    cursor_1 = db_1.cursor()
    cursor_2 = db_2.cursor()

    # sql = 'SELECT PaperID,Abstract from PaperAbstract LIMIT 100'
    sql_get_conference = 'select Y.ShortName, Y.ConferenceSeriesID, Count(X.OriginalPaperTitle) as PaperAmt from Papers as X, ConferenceSeries as Y where Y.ConferenceSeriesID =  X.ConferenceSeriesIDMappedToVenueName Group By X.ConferenceSeriesIDMappedToVenueName Order by PaperAmt DESC Limit 10;'

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

    doc_vecs = list()

    confer_vecs = list()

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
        

        # Conference vector
        base_confer_vec = np.array([0.0 for _ in opt.vec_dim])

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
            new_abstract = new_abstract[0][0]
            # print 'new_ab', new_abstract
            washed_abstract = wash_doc(new_abstract)

            new_doc_vec = [short_name, paperid] + gen_doc_vec(washed_abstract)

            doc_vecs.append(new_doc_vec)
            
            base_confer_vec += np.array(new_doc_vec)
        
        base_confer_vec /= float(paper_amt)
        confer_vecs.append(base_confer_vec.tolist())
            

    write_doc_vec(doc_vecs, path_doc_vec)
    
    write_doc_vec(confer_vecs, path_confer_vec)

    sys.stdout.write('\n')

    cursor_1.close()
    cursor_2.close()
    db_1.close()
    db_2.close()
    

    # Save Infos
    with open("infos", 'w') as f:
        for conferid in infos:
            s_n = infos[conferid]['short_name']
            p_a = infos[conferid]['paper_amt']
            
            f.write("%s %s\n" % (s_n,p_a))


if __name__ == "__main__":
    main()
