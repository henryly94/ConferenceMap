#!/usr/bin/python
import threading

class SkipgramReader:
    """Self-Customed Skipgram Reader"""
    
    def __init__(self, batch_size, window_size, file_path, word2id):

        self.window_size = window_size
        self.file_path = file_path
        self.batch_size = batch_size
        self._word2id = word2id
        self.EOF = True
        self.batch_lock = threading.Lock()
        self.init_lock = threading.Lock()
        self.initial()

    def word_per_epoch(self):
        print("Scanning train set")
        cnt = 0
        while True:
            self.get_next_batch()
            if self.EOF:
                break
            cnt += self.batch_size

        self.initial()
        return cnt

    def get_next_word(self):
        word = ''
        if self.cur_char == '':
            return ''
        
        while self.cur_char in ' \n\t':
            self.cur_char = self.fd.read(1)
            if self.cur_char == '':
                return ''
        while self.cur_char not in ' \n\t':
            word += self.cur_char
            self.cur_char = self.fd.read(1)
            if self.cur_char == '':
                return ''
        return word

    def insert_next_word(self):
        if len(self.word_queue) >= 2 * self.window_size + 1:
            self.word_queue = self.word_queue[-(2*self.window_size):]
        
        new_word = self.get_next_word()
        if new_word == '':
            self.EOF = True
            self.fd.close()
            return False
        else:
            self.word_queue.append(new_word)
            return True
    
    
    def get_next_pair(self):
        if self.cur_pos +self.cur_off >= 2*self.window_size:
            if self.insert_next_word():
                self.cur_pos = self.window_size
                self.cur_off = -self.window_size
                return True, self.search_pair()
            else:
                return False, [0, 0]
        else:
            if self.cur_off < self.window_size:
                self.cur_off += 1
                if self.cur_off == 0: # jump through origin
                    self.cur_off += 1
            else:
                self.cur_pos += 1
                self.cur_off = max(-self.window_size, -self.cur_pos)
            return True, self.search_pair()

    def search_pair(self):
        a, b = self.word_queue[self.cur_pos], self.word_queue[self.cur_pos + self.cur_off]
        return [self.search(a), self.search(b)]

    def search(self, word):
        return self._word2id.get(word, 0)



    def get_next_batch(self):
        self.batch_lock.acquire()
        next_batch = []
        for i in xrange(self.batch_size):
            status, res = self.get_next_pair()
            if not status:
                next_batch += [[0,0] for _ in xrange(self.batch_size - i-1)] + [2,2]
                break
            next_batch.append(res)
           
        self.batch_lock.release()
        return self.EOF, next_batch

    def initial(self):
        self.init_lock.acquire()
        if self.EOF:
            self.fd = open(self.file_path, 'r')

            self.cur_char = ' '
            self.word_queue = []
            self.cur_pos = 0
            self.cur_off = 0
            
            for i in xrange(2*self.window_size+1):
                self.insert_next_word()

            self.EOF = False
        self.init_lock.release() 
